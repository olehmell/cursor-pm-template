#!/usr/bin/env python3
"""Stability (reproducibility) study: K identical Jev requests per sampled item."""

from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

# Reuse builders from sibling scripts
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_e1_jev import build_payload as e1_build, call_jev, map_severity  # noqa: E402
from run_e2_jev import build_payload as e2_build, load_company_snippets  # noqa: E402
from run_e3_jev import build_payload as e3_build, map_cta  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
K = 5
NOUL_STABLE_RANGE = 0.10
NOUL_STABLE_STD = 0.05
LEVEL_ORDER = {"low": 1, "medium": 2, "high": 3}
ADJACENT = {(1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 2), (3, 3)}

RAW = ROOT / "runs" / "stability" / "raw"
OUT_METRICS = ROOT / "runs" / "stability" / "metrics.md"
OUT_SUMMARY = ROOT / "runs" / "stability" / "summary.json"
SAMPLE_MANIFEST = ROOT / "runs" / "stability" / "sample_manifest.json"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def pick_e1(rows: list[dict], summary: dict) -> list[dict]:
    """12 passages: mix themes/severities; include theme misses."""
    by_id = {r["id"]: r for r in rows}
    results = {r["id"]: r for r in summary["results"]}
    theme_misses = [
        rid for rid, r in results.items() if r["pred_theme"] != r["gold_theme"]
    ]
    # Stratified picks
    want = [
        # theme misses (diverse)
        "e1-006",  # trust→setup
        "e1-008",  # trust→setup, low conf
        "e1-018",  # other→notifications
        "e1-027",  # setup→other
        # hits across themes + sevs
        "e1-001",  # notifications / high (sev miss)
        "e1-003",  # multi_pet / low (exact)
        "e1-007",  # setup_friction / medium (exact)
        "e1-010",  # other / low
        "e1-015",  # trust_data / high
        "e1-016",  # setup_friction / high (exact both)
        "e1-024",  # trust_data / medium
        "e1-025",  # notifications / medium
    ]
    selected = []
    for rid in want:
        if rid in by_id:
            selected.append(by_id[rid])
    # fill if any missing
    if len(selected) < 12:
        for r in rows:
            if r["id"] not in {x["id"] for x in selected}:
                selected.append(r)
            if len(selected) >= 12:
                break
    return selected[:12]


def pick_e2(rows: list[dict]) -> list[dict]:
    """10 items: mix mvp_scoped / metric_measurable (and gold 0/1)."""
    by_id = {r["id"]: r for r in rows}
    want = [
        # mvp scope mix
        "e2-001",  # mvp gold1
        "e2-010",  # mvp gold0
        "e2-017",  # mvp gold1
        "e2-021",  # mvp gold0 near-miss noul 0.46
        "e2-022",  # mvp gold1 borderline 0.56
        # metric mix + miss
        "e2-002",  # metric gold1
        "e2-003",  # metric gold0
        "e2-008",  # metric miss gold1 pred0
        "e2-011",  # metric gold1 mid noul
        "e2-025",  # metric gold0 synthetic
    ]
    return [by_id[i] for i in want if i in by_id][:10]


def pick_e3(rows: list[dict]) -> list[dict]:
    """8 items: mix advances_hypothesis + CTA clarity."""
    by_id = {r["id"]: r for r in rows}
    want = [
        "e3-001",  # adv1 + cta high
        "e3-006",  # adv1 + cta medium
        "e3-008",  # adv0 + cta medium
        "e3-009",  # adv0 + cta high (neg)
        "e3-013",  # adv0 + cta low
        "e3-015",  # adv1 + cta low
        "e3-017",  # adv miss (fn)
        "e3-019",  # adv miss (fn)
    ]
    return [by_id[i] for i in want if i in by_id][:8]


def extract_e1(resp: dict) -> dict:
    answers = resp.get("answers") or {}
    theme_a = answers.get("theme") or {}
    sev_a = answers.get("activation_severity") or {}
    return {
        "theme": theme_a.get("choice"),
        "severity": map_severity(sev_a) if sev_a else None,
        "severity_score": sev_a.get("score"),
        "theme_confidence": theme_a.get("confidence"),
        "severity_confidence": sev_a.get("confidence"),
    }


def extract_e2(resp: dict) -> dict:
    answers = resp.get("answers") or {}
    out = {}
    if "mvp_scoped" in answers:
        noul = float(answers["mvp_scoped"].get("noul"))
        out["mvp_scoped_noul"] = noul
        out["mvp_scoped"] = 1 if noul >= 0.5 else 0
    if "metric_measurable" in answers:
        noul = float(answers["metric_measurable"].get("noul"))
        out["metric_measurable_noul"] = noul
        out["metric_measurable"] = 1 if noul >= 0.5 else 0
    return out


def extract_e3(resp: dict) -> dict:
    answers = resp.get("answers") or {}
    out = {}
    if "advances_hypothesis" in answers:
        noul = float(answers["advances_hypothesis"].get("noul"))
        out["advances_hypothesis_noul"] = noul
        out["advances_hypothesis"] = 1 if noul >= 0.5 else 0
    if "cta_clarity" in answers:
        cta = answers["cta_clarity"]
        out["cta_clarity"] = map_cta(cta)
        out["cta_clarity_score"] = cta.get("score")
    return out


def mode_stats(values: list) -> dict:
    vals = [v for v in values if v is not None]
    if not vals:
        return {"mode": None, "mode_agreement": None, "unique_count": 0, "n": 0}
    c = Counter(vals)
    mode, count = c.most_common(1)[0]
    # tie-break: lexicographic for determinism
    tied = [k for k, v in c.items() if v == count]
    if len(tied) > 1:
        mode = sorted(tied, key=lambda x: str(x))[0]
    return {
        "mode": mode,
        "mode_agreement": count / len(vals),
        "unique_count": len(c),
        "n": len(vals),
        "counts": dict(c),
    }


def noul_stats(values: list[float]) -> dict:
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return {"mean": None, "std": None, "range": None, "stable": None, "n": 0}
    mean = sum(vals) / len(vals)
    if len(vals) == 1:
        std = 0.0
    else:
        var = sum((x - mean) ** 2 for x in vals) / (len(vals) - 1)
        std = math.sqrt(var)
    rng = max(vals) - min(vals)
    return {
        "mean": round(mean, 6),
        "std": round(std, 6),
        "range": round(rng, 6),
        "min": min(vals),
        "max": max(vals),
        "values": vals,
        "stable": rng <= NOUL_STABLE_RANGE and std <= NOUL_STABLE_STD,
        "n": len(vals),
    }


def score_level_stats(labels: list) -> dict:
    ms = mode_stats(labels)
    vals = [v for v in labels if v is not None]
    if not vals or ms["mode"] is None:
        return {**ms, "frac_exact": None, "frac_within_adjacent": None, "level_variance": None}
    mode = ms["mode"]
    exact = sum(1 for v in vals if v == mode) / len(vals)
    mode_n = LEVEL_ORDER.get(mode)
    adj = 0
    nums = []
    for v in vals:
        n = LEVEL_ORDER.get(v)
        if n is not None:
            nums.append(n)
        if mode_n is not None and n is not None and (mode_n, n) in ADJACENT:
            adj += 1
    adj_frac = adj / len(vals) if vals else None
    if len(nums) > 1:
        m = sum(nums) / len(nums)
        var = sum((x - m) ** 2 for x in nums) / (len(nums) - 1)
    else:
        var = 0.0
    return {
        **ms,
        "frac_exact": exact,
        "frac_within_adjacent": adj_frac,
        "level_variance": round(var, 6),
    }


def discrete_tuple(extracted: dict, keys: list[str]) -> tuple:
    return tuple(extracted.get(k) for k in keys)


def analyze_item(exp: str, item_id: str, runs: list[dict]) -> dict:
    ok = [r for r in runs if r.get("ok")]
    fail = [r for r in runs if not r.get("ok")]
    extracted = [r["extracted"] for r in ok]
    out = {
        "id": item_id,
        "exp": exp,
        "n_ok": len(ok),
        "n_fail": len(fail),
        "failures": [{"run": r["run"], "error": r.get("error")} for r in fail],
    }
    if exp == "E1":
        themes = [e.get("theme") for e in extracted]
        sevs = [e.get("severity") for e in extracted]
        out["theme"] = mode_stats(themes)
        out["severity"] = score_level_stats(sevs)
        keys = ["theme", "severity"]
    elif exp == "E2":
        # whichever questions present
        if any("mvp_scoped" in e for e in extracted):
            out["mvp_scoped"] = mode_stats([e.get("mvp_scoped") for e in extracted])
            out["mvp_scoped_noul"] = noul_stats([e.get("mvp_scoped_noul") for e in extracted])
            keys = ["mvp_scoped"]
        else:
            out["metric_measurable"] = mode_stats([e.get("metric_measurable") for e in extracted])
            out["metric_measurable_noul"] = noul_stats(
                [e.get("metric_measurable_noul") for e in extracted]
            )
            keys = ["metric_measurable"]
    else:  # E3
        out["advances_hypothesis"] = mode_stats([e.get("advances_hypothesis") for e in extracted])
        out["advances_hypothesis_noul"] = noul_stats(
            [e.get("advances_hypothesis_noul") for e in extracted]
        )
        cta_present = [e for e in extracted if e.get("cta_clarity") is not None]
        if cta_present:
            out["cta_clarity"] = score_level_stats([e.get("cta_clarity") for e in cta_present])
            keys = ["advances_hypothesis", "cta_clarity"]
        else:
            keys = ["advances_hypothesis"]
    # perfect / nearly identical discrete answers across ok runs
    if extracted:
        tuples = [discrete_tuple(e, keys) for e in extracted]
        # only count if all ok runs have all keys non-None
        complete = [t for t in tuples if all(x is not None for x in t)]
        if len(complete) == K:
            c = Counter(complete)
            top = c.most_common(1)[0][1]
            out["perfect_5of5"] = top == K
            out["at_least_4of5"] = top >= 4
            out["discrete_mode_count"] = top
            out["discrete_keys"] = keys
            out["discrete_unique"] = len(c)
        else:
            out["perfect_5of5"] = False
            out["at_least_4of5"] = False
            out["discrete_mode_count"] = max(Counter(complete).values()) if complete else 0
            out["discrete_keys"] = keys
            out["incomplete_ok"] = len(complete)
    return out


def aggregate(items: list[dict]) -> dict:
    with_discrete = [i for i in items if i.get("n_ok") == K]
    n = len(with_discrete)
    perfect = sum(1 for i in with_discrete if i.get("perfect_5of5"))
    ge4 = sum(1 for i in with_discrete if i.get("at_least_4of5"))

    def avg_mode_agree(field: str) -> float | None:
        vals = []
        for i in items:
            block = i.get(field)
            if isinstance(block, dict) and block.get("mode_agreement") is not None:
                vals.append(block["mode_agreement"])
        return round(sum(vals) / len(vals), 4) if vals else None

    noul_fields = []
    for i in items:
        for k, v in i.items():
            if k.endswith("_noul") and isinstance(v, dict) and v.get("stable") is not None:
                noul_fields.append(v)

    return {
        "n_items_full_k": n,
        "n_items_total": len(items),
        "pct_perfect_5of5": round(100 * perfect / n, 1) if n else None,
        "pct_at_least_4of5": round(100 * ge4 / n, 1) if n else None,
        "n_perfect_5of5": perfect,
        "n_at_least_4of5": ge4,
        "mean_theme_mode_agreement": avg_mode_agree("theme"),
        "mean_severity_mode_agreement": avg_mode_agree("severity"),
        "mean_mvp_mode_agreement": avg_mode_agree("mvp_scoped"),
        "mean_metric_mode_agreement": avg_mode_agree("metric_measurable"),
        "mean_advances_mode_agreement": avg_mode_agree("advances_hypothesis"),
        "mean_cta_mode_agreement": avg_mode_agree("cta_clarity"),
        "noul_stable_count": sum(1 for v in noul_fields if v["stable"]),
        "noul_total": len(noul_fields),
        "noul_stable_pct": round(100 * sum(1 for v in noul_fields if v["stable"]) / len(noul_fields), 1)
        if noul_fields
        else None,
        "thresholds": {
            "noul_stable_range_le": NOUL_STABLE_RANGE,
            "noul_stable_std_le": NOUL_STABLE_STD,
            "K": K,
        },
    }


def write_metrics_md(summary: dict) -> str:
    lines = []
    lines.append("# Jev stability study (reproducibility)")
    lines.append("")
    lines.append(f"**K** = {K} identical requests per item (same state+questions).")
    lines.append(f"**Model:** `{summary['model']}` → resolved per-response.")
    lines.append(f"**Sample:** E1={summary['sample_sizes']['E1']}, "
                 f"E2={summary['sample_sizes']['E2']}, E3={summary['sample_sizes']['E3']} "
                 f"(total {summary['sample_sizes']['total']} items, "
                 f"{summary['sample_sizes']['total'] * K} planned API calls).")
    lines.append(f"**API failures:** {summary['api_failure_count']} "
                 f"(rate-limit hits noted: {summary.get('rate_limit_hits', 0)}).")
    lines.append("")
    lines.append("## Stability thresholds (documented)")
    lines.append("")
    lines.append(f"- Noul **stable** if range (max−min) ≤ **{NOUL_STABLE_RANGE}** "
                 f"and sample std ≤ **{NOUL_STABLE_STD}**.")
    lines.append("- Discrete perfect = all K runs identical on the item's discrete answer keys.")
    lines.append("- ≥4/5 = mode of the discrete tuple appears in at least 4 of K runs.")
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    agg = summary["aggregate"]
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Items with full K={K} ok | {agg['n_items_full_k']} / {agg['n_items_total']} |")
    lines.append(f"| % perfect 5/5 identical discrete | **{agg['pct_perfect_5of5']}%** "
                 f"({agg['n_perfect_5of5']}/{agg['n_items_full_k']}) |")
    lines.append(f"| % ≥4/5 discrete | **{agg['pct_at_least_4of5']}%** "
                 f"({agg['n_at_least_4of5']}/{agg['n_items_full_k']}) |")
    lines.append(f"| Noul fields stable (range≤{NOUL_STABLE_RANGE}, std≤{NOUL_STABLE_STD}) | "
                 f"**{agg['noul_stable_pct']}%** ({agg['noul_stable_count']}/{agg['noul_total']}) |")
    for label, key in [
        ("E1 theme mean mode-agreement", "mean_theme_mode_agreement"),
        ("E1 severity mean mode-agreement", "mean_severity_mode_agreement"),
        ("E2 mvp_scoped mean mode-agreement", "mean_mvp_mode_agreement"),
        ("E2 metric_measurable mean mode-agreement", "mean_metric_mode_agreement"),
        ("E3 advances_hypothesis mean mode-agreement", "mean_advances_mode_agreement"),
        ("E3 cta_clarity mean mode-agreement", "mean_cta_mode_agreement"),
    ]:
        v = agg.get(key)
        if v is not None:
            lines.append(f"| {label} | {v:.3f} |")
    lines.append("")

    for exp in ("E1", "E2", "E3"):
        items = [i for i in summary["items"] if i["exp"] == exp]
        lines.append(f"## {exp} per-item")
        lines.append("")
        if exp == "E1":
            lines.append("| id | theme mode | theme agree | theme #uniq | sev mode | sev agree | "
                         "sev exact | sev adj | perfect 5/5 | ≥4/5 |")
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
            for i in items:
                t, s = i.get("theme") or {}, i.get("severity") or {}
                lines.append(
                    f"| {i['id']} | {t.get('mode')} | {t.get('mode_agreement')} | {t.get('unique_count')} | "
                    f"{s.get('mode')} | {s.get('mode_agreement')} | {s.get('frac_exact')} | "
                    f"{s.get('frac_within_adjacent')} | {i.get('perfect_5of5')} | {i.get('at_least_4of5')} |"
                )
        elif exp == "E2":
            lines.append("| id | discrete key | mode | agree | #uniq | noul mean | noul std | "
                         "noul range | noul stable | perfect 5/5 | ≥4/5 |")
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
            for i in items:
                if "mvp_scoped" in i:
                    d, n = i["mvp_scoped"], i["mvp_scoped_noul"]
                    key = "mvp_scoped"
                else:
                    d, n = i["metric_measurable"], i["metric_measurable_noul"]
                    key = "metric_measurable"
                lines.append(
                    f"| {i['id']} | {key} | {d.get('mode')} | {d.get('mode_agreement')} | "
                    f"{d.get('unique_count')} | {n.get('mean')} | {n.get('std')} | {n.get('range')} | "
                    f"{n.get('stable')} | {i.get('perfect_5of5')} | {i.get('at_least_4of5')} |"
                )
        else:
            lines.append("| id | adv mode | adv agree | noul mean | noul std | noul range | "
                         "noul stable | cta mode | cta agree | perfect 5/5 | ≥4/5 |")
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
            for i in items:
                a = i.get("advances_hypothesis") or {}
                n = i.get("advances_hypothesis_noul") or {}
                c = i.get("cta_clarity") or {}
                lines.append(
                    f"| {i['id']} | {a.get('mode')} | {a.get('mode_agreement')} | "
                    f"{n.get('mean')} | {n.get('std')} | {n.get('range')} | {n.get('stable')} | "
                    f"{c.get('mode', '—')} | {c.get('mode_agreement', '—')} | "
                    f"{i.get('perfect_5of5')} | {i.get('at_least_4of5')} |"
                )
        lines.append("")

    unstable = [
        i for i in summary["items"]
        if i.get("n_ok") == K and (not i.get("at_least_4of5") or i.get("discrete_unique", 1) > 2)
    ]
    # also flag noul unstable
    noul_unstable = []
    for i in summary["items"]:
        for k, v in i.items():
            if k.endswith("_noul") and isinstance(v, dict) and v.get("stable") is False:
                noul_unstable.append((i["id"], k, v))

    lines.append("## Notable unstable items")
    lines.append("")
    if not unstable and not noul_unstable:
        lines.append("None under the documented thresholds (all items ≥4/5 discrete and noul-stable).")
    else:
        if unstable:
            lines.append("### Discrete flip / low agreement")
            for i in unstable:
                lines.append(
                    f"- `{i['id']}` ({i['exp']}): discrete_mode_count={i.get('discrete_mode_count')}, "
                    f"unique={i.get('discrete_unique')}, keys={i.get('discrete_keys')}"
                )
        if noul_unstable:
            lines.append("### Noul not stable (range>0.10 or std>0.05)")
            for iid, k, v in noul_unstable:
                lines.append(
                    f"- `{iid}` `{k}`: mean={v.get('mean')}, std={v.get('std')}, "
                    f"range={v.get('range')}, values={v.get('values')}"
                )
    lines.append("")
    lines.append("## Sample IDs")
    lines.append("")
    for exp, ids in summary["sample_ids"].items():
        lines.append(f"- **{exp}:** {', '.join(ids)}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    api_key = os.environ.get("TYPESAFE_API_KEY", "")
    print(f"TYPESAFE_API_KEY length: {len(api_key)}", flush=True)
    if not api_key:
        print("ERROR: TYPESAFE_API_KEY missing", file=sys.stderr)
        return 2

    e1_rows = load_jsonl(ROOT / "datasets" / "e1_interview_passages.jsonl")
    e2_rows = load_jsonl(ROOT / "datasets" / "e2_prd_sections.jsonl")
    e3_rows = load_jsonl(ROOT / "datasets" / "e3_screens.jsonl")
    e1_summary = json.loads((ROOT / "runs" / "E1" / "summary.json").read_text(encoding="utf-8"))

    e1_sample = pick_e1(e1_rows, e1_summary)
    e2_sample = pick_e2(e2_rows)
    e3_sample = pick_e3(e3_rows)
    company_blob = load_company_snippets()

    manifest = {
        "K": K,
        "E1": [r["id"] for r in e1_sample],
        "E2": [r["id"] for r in e2_sample],
        "E3": [r["id"] for r in e3_sample],
        "notes": {
            "E1": "mix themes/severities; includes theme misses e1-006,008,018,027",
            "E2": "5 mvp_scoped + 5 metric_measurable; includes miss e2-008 and near e2-021/022",
            "E3": "mix adv 0/1 and CTA levels; includes misses e3-017,019",
        },
    }
    (ROOT / "runs" / "stability").mkdir(parents=True, exist_ok=True)
    SAMPLE_MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Sample: E1={len(e1_sample)} E2={len(e2_sample)} E3={len(e3_sample)}", flush=True)

    jobs = []
    for r in e1_sample:
        jobs.append(("E1", r, e1_build(r["passage"]), extract_e1))
    for r in e2_sample:
        jobs.append(("E2", r, e2_build(r, company_blob), extract_e2))
    for r in e3_sample:
        jobs.append(("E3", r, e3_build(r), extract_e3))

    api_failures = 0
    rate_limit_hits = 0
    item_runs: dict[str, list] = defaultdict(list)

    total_calls = len(jobs) * K
    call_i = 0
    for exp, row, payload, extractor in jobs:
        pid = row["id"]
        raw_dir = RAW / exp
        raw_dir.mkdir(parents=True, exist_ok=True)
        for run_n in range(1, K + 1):
            call_i += 1
            raw_path = raw_dir / f"{pid}_r{run_n}.json"
            print(f"[{call_i}/{total_calls}] {exp}/{pid} r{run_n} …", flush=True)
            # skip if already have successful raw (resume)
            if raw_path.exists():
                try:
                    prev = json.loads(raw_path.read_text(encoding="utf-8"))
                    if "response" in prev and "answers" in (prev.get("response") or {}):
                        extracted = extractor(prev["response"])
                        item_runs[f"{exp}:{pid}"].append(
                            {"run": run_n, "ok": True, "extracted": extracted, "raw": str(raw_path)}
                        )
                        print(f"  resume ok {extracted}", flush=True)
                        continue
                except Exception:
                    pass
            try:
                resp = call_jev(api_key, payload)
                raw_path.write_text(
                    json.dumps(
                        {
                            "request_meta": {
                                "id": pid,
                                "exp": exp,
                                "run": run_n,
                                "K": K,
                                "questions": list(payload["questions"].keys()),
                            },
                            "response": resp,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                extracted = extractor(resp)
                item_runs[f"{exp}:{pid}"].append(
                    {"run": run_n, "ok": True, "extracted": extracted, "raw": str(raw_path)}
                )
                print(f"  ok {extracted}", flush=True)
            except Exception as e:
                msg = str(e)
                api_failures += 1
                if "429" in msg or "rate" in msg.lower():
                    rate_limit_hits += 1
                print(f"  FAIL: {msg}", flush=True)
                raw_path.write_text(
                    json.dumps(
                        {"request_meta": {"id": pid, "exp": exp, "run": run_n}, "error": msg},
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                item_runs[f"{exp}:{pid}"].append(
                    {"run": run_n, "ok": False, "error": msg, "extracted": {}}
                )
            time.sleep(0.5)

    items = []
    for exp, row, _, _ in jobs:
        key = f"{exp}:{row['id']}"
        items.append(analyze_item(exp, row["id"], item_runs[key]))

    agg_all = aggregate(items)
    # per-exp aggregates
    by_exp = {}
    for exp in ("E1", "E2", "E3"):
        by_exp[exp] = aggregate([i for i in items if i["exp"] == exp])

    summary = {
        "model": "jev-latest",
        "K": K,
        "sample_sizes": {
            "E1": len(e1_sample),
            "E2": len(e2_sample),
            "E3": len(e3_sample),
            "total": len(e1_sample) + len(e2_sample) + len(e3_sample),
        },
        "sample_ids": {
            "E1": [r["id"] for r in e1_sample],
            "E2": [r["id"] for r in e2_sample],
            "E3": [r["id"] for r in e3_sample],
        },
        "api_failure_count": api_failures,
        "rate_limit_hits": rate_limit_hits,
        "thresholds": {
            "noul_stable_range_le": NOUL_STABLE_RANGE,
            "noul_stable_std_le": NOUL_STABLE_STD,
        },
        "aggregate": agg_all,
        "aggregate_by_exp": by_exp,
        "items": items,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_METRICS.write_text(write_metrics_md(summary), encoding="utf-8")
    print(f"Wrote {OUT_SUMMARY} and {OUT_METRICS}", flush=True)
    print(
        f"Aggregate: perfect={agg_all['pct_perfect_5of5']}% "
        f">=4/5={agg_all['pct_at_least_4of5']}% "
        f"noul_stable={agg_all['noul_stable_pct']}% "
        f"api_fail={api_failures}",
        flush=True,
    )
    return 0 if api_failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
