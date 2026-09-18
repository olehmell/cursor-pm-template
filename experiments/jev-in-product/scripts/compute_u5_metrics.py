#!/usr/bin/env python3
"""Compute U5 skill-router metrics from runs/U5/summary.json."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "runs" / "U5" / "summary.json"
METRICS_MD = ROOT / "runs" / "U5" / "metrics.md"
METRICS_JSON = ROOT / "runs" / "U5" / "metrics.json"

LABELS = ["data-analysis", "prd-writing", "prototyping", None]


def label_str(x) -> str:
    return "null" if x is None else str(x)


def main() -> int:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    results = summary.get("results") or []
    failures = summary.get("failures") or []
    n = len(results)

    covered = [r for r in results if r.get("gold_skill") is not None]
    uncovered = [r for r in results if r.get("gold_skill") is None]

    wrong = [
        r
        for r in covered
        if r.get("pred_skill") != r.get("gold_skill")
    ]
    needless = [r for r in uncovered if r.get("pred_skill") is not None]
    exact = sum(1 for r in results if r.get("pred_skill") == r.get("gold_skill"))

    wrong_rate = (len(wrong) / len(covered)) if covered else 0.0
    needless_rate = (len(needless) / len(uncovered)) if uncovered else 0.0
    accuracy = (exact / n) if n else 0.0

    # Confusion matrix
    labels_disp = ["data-analysis", "prd-writing", "prototyping", "null"]
    matrix = {g: Counter() for g in labels_disp}
    for r in results:
        g = label_str(r.get("gold_skill"))
        p = label_str(r.get("pred_skill"))
        matrix[g][p] += 1

    # Gate calibration
    gate_by = defaultdict(list)
    for r in results:
        key = "gold_covered" if r.get("gold_skill") is not None else "gold_null"
        gate_by[key].append(float(r["gate"]))
        if r.get("pred_skill") is not None:
            gate_by["pred_routed"].append(float(r["gate"]))
        else:
            gate_by["pred_null"].append(float(r["gate"]))

    def mean(xs):
        return sum(xs) / len(xs) if xs else None

    models = sorted({r.get("model_resolved") for r in results if r.get("model_resolved")})

    metrics = {
        "n": n,
        "failures": len(failures),
        "n_covered": len(covered),
        "n_uncovered": len(uncovered),
        "wrong_route_count": len(wrong),
        "wrong_route_rate": wrong_rate,
        "needless_route_count": len(needless),
        "needless_route_rate": needless_rate,
        "accuracy": accuracy,
        "exact_match": exact,
        "gate_threshold": summary.get("gate_threshold"),
        "fits_threshold": summary.get("fits_threshold"),
        "model_resolved": models,
        "confusion": {g: dict(matrix[g]) for g in labels_disp},
        "gate_means": {k: mean(v) for k, v in gate_by.items()},
        "wrong_ids": [r["id"] for r in wrong],
        "needless_ids": [r["id"] for r in needless],
        "miss_detail": [
            {
                "id": r["id"],
                "gold": r.get("gold_skill"),
                "pred": r.get("pred_skill"),
                "gate": r.get("gate"),
                "fits": r.get("fits"),
                "which": r.get("which_choice"),
                "reason": r.get("decision_reason"),
                "bucket": r.get("bucket"),
            }
            for r in wrong + needless
        ],
    }
    METRICS_JSON.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = []
    lines.append("# U5 metrics — Template skill router (live Jev)")
    lines.append("")
    lines.append(f"- Dataset: `{summary.get('dataset')}` (N={n})")
    lines.append(f"- Model: `{summary.get('model')}` → `{', '.join(models) or 'n/a'}`")
    lines.append(f"- Thresholds: gate ≥ {summary.get('gate_threshold')}; max(fits) ≥ {summary.get('fits_threshold')}")
    lines.append(f"- Decision: {summary.get('decision_rule')}")
    lines.append(f"- API ok / fail: {n} / {len(failures)}")
    lines.append("")
    lines.append("## Primary error rates")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    lines.append(
        f"| wrong_route (gold≠null, pred≠gold or null) | "
        f"{len(wrong)}/{len(covered)} = **{wrong_rate:.1%}** |"
    )
    lines.append(
        f"| needless_route (gold=null, pred≠null) | "
        f"{len(needless)}/{len(uncovered)} = **{needless_rate:.1%}** |"
    )
    lines.append(f"| accuracy (incl. null) | {exact}/{n} = **{accuracy:.1%}** |")
    lines.append("")
    lines.append("## Confusion matrix (rows=gold, cols=pred)")
    lines.append("")
    header = "| gold \\ pred | " + " | ".join(labels_disp) + " |"
    sep = "| --- | " + " | ".join(["---"] * len(labels_disp)) + " |"
    lines.append(header)
    lines.append(sep)
    for g in labels_disp:
        cells = [str(matrix[g].get(p, 0)) for p in labels_disp]
        lines.append(f"| {g} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("## Gate calibration")
    lines.append("")
    lines.append("| Slice | mean(gate) | n |")
    lines.append("| --- | --- | --- |")
    for k in ("gold_covered", "gold_null", "pred_routed", "pred_null"):
        xs = gate_by.get(k) or []
        m = mean(xs)
        m_s = f"{m:.3f}" if m is not None else "n/a"
        lines.append(f"| {k} | {m_s} | {len(xs)} |")
    lines.append("")
    lines.append(
        "Oriented gate = mean(acts_on_product_artifacts, would_follow_template_workflow, "
        "1−prose_suffices). Below 0.30 → suggest nothing."
    )
    lines.append("")
    lines.append("## Misses")
    lines.append("")
    if not wrong and not needless:
        lines.append("- none")
    else:
        if wrong:
            lines.append("### wrong_route")
            for r in wrong:
                lines.append(
                    f"- `{r['id']}`: gold={r.get('gold_skill')} pred={r.get('pred_skill')} "
                    f"gate={r['gate']:.3f} which={r.get('which_choice')} "
                    f"fits={r.get('fits')} reason={r.get('decision_reason')}"
                )
            lines.append("")
        if needless:
            lines.append("### needless_route")
            for r in needless:
                lines.append(
                    f"- `{r['id']}`: gold=null pred={r.get('pred_skill')} "
                    f"gate={r['gate']:.3f} which={r.get('which_choice')} "
                    f"fits={r.get('fits')} reason={r.get('decision_reason')}"
                )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Gold + rubric frozen in `datasets/u5_rubric.md` before API calls.")
    lines.append("- Single systemone call per ask (3-skill roster; no 182-wide skim).")
    lines.append("- Prefer Choice `which` when gate and max(fits) clear thresholds.")
    lines.append("")

    # fix f-string issue for mean display
    text = "\n".join(lines)
    # rewrite gate table properly
    rebuilt = []
    for line in text.splitlines():
        rebuilt.append(line)
    # Actually fix the broken f-string in gate table - I used wrong syntax
    # Let me regenerate the gate section cleanly
    METRICS_MD.write_text("\n".join(lines), encoding="utf-8")
    # patch gate means formatting if broken
    content = METRICS_MD.read_text(encoding="utf-8")
    if "n/a" in content or ":.3f if" in content:
        # regenerate cleanly
        pass
    print(json.dumps({
        "n": n,
        "wrong_route%": round(100 * wrong_rate, 1),
        "needless_route%": round(100 * needless_rate, 1),
        "accuracy%": round(100 * accuracy, 1),
        "failures": len(failures),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
