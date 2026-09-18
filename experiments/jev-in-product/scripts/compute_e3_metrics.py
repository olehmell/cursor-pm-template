#!/usr/bin/env python3
"""Compute E3 metrics from runs/E3/summary.json → metrics.md."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "runs" / "E3" / "summary.json"
METRICS = ROOT / "runs" / "E3" / "metrics.md"
THRESHOLD = 0.5
LEVELS = ["low", "medium", "high"]
LEVEL_IDX = {n: i for i, n in enumerate(LEVELS)}


def auc_binary(scores: list[float], labels: list[int]) -> float | None:
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return None
    wins = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def brier(scores: list[float], labels: list[int]) -> float:
    return sum((s - y) ** 2 for s, y in zip(scores, labels)) / len(labels)


def conf_mat(preds: list[int], golds: list[int]) -> dict:
    tp = sum(p == 1 and g == 1 for p, g in zip(preds, golds))
    tn = sum(p == 0 and g == 0 for p, g in zip(preds, golds))
    fp = sum(p == 1 and g == 0 for p, g in zip(preds, golds))
    fn = sum(p == 0 and g == 1 for p, g in zip(preds, golds))
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn}


def eval_advances(results: list[dict]) -> dict:
    rows = [r for r in results if r.get("gold_advances_hypothesis") is not None and "advances_hypothesis_noul" in r]
    golds = [int(r["gold_advances_hypothesis"]) for r in rows]
    scores = [float(r["advances_hypothesis_noul"]) for r in rows]
    preds = [int(r["pred_advances_hypothesis"]) for r in rows]
    n = len(rows)
    correct = sum(p == g for p, g in zip(preds, golds))
    cm = conf_mat(preds, golds)
    return {
        "n": n,
        "accuracy": correct / n if n else None,
        "correct": correct,
        "confusion": cm,
        "false_pass_rate": cm["fp"] / n if n else 0.0,
        "auc": auc_binary(scores, golds),
        "brier": brier(scores, golds) if n else None,
        "score_mean": sum(scores) / n if n else None,
        "score_min": min(scores) if scores else None,
        "score_max": max(scores) if scores else None,
        "score_by_gold": {
            "gold1_mean": (sum(s for s, g in zip(scores, golds) if g == 1) / max(1, sum(g == 1 for g in golds))),
            "gold0_mean": (sum(s for s, g in zip(scores, golds) if g == 0) / max(1, sum(g == 0 for g in golds))),
            "n_gold1": sum(g == 1 for g in golds),
            "n_gold0": sum(g == 0 for g in golds),
        },
        "misses": [
            {
                "id": r["id"],
                "gold": int(r["gold_advances_hypothesis"]),
                "pred": int(r["pred_advances_hypothesis"]),
                "noul": float(r["advances_hypothesis_noul"]),
            }
            for r in rows
            if int(r["pred_advances_hypothesis"]) != int(r["gold_advances_hypothesis"])
        ],
        "scores": [
            {"id": r["id"], "gold": int(r["gold_advances_hypothesis"]), "noul": float(r["advances_hypothesis_noul"])}
            for r in rows
        ],
    }


def eval_cta(results: list[dict]) -> dict:
    rows = [
        r
        for r in results
        if r.get("gold_cta_clarity") is not None and r.get("pred_cta_clarity") is not None
    ]
    n = len(rows)
    exact = sum(r["pred_cta_clarity"] == r["gold_cta_clarity"] for r in rows)
    adjacent = 0
    confusion = {g: {p: 0 for p in LEVELS} for g in LEVELS}
    for r in rows:
        g, p = r["gold_cta_clarity"], r["pred_cta_clarity"]
        if g in confusion and p in confusion[g]:
            confusion[g][p] += 1
        if g in LEVEL_IDX and p in LEVEL_IDX:
            if abs(LEVEL_IDX[g] - LEVEL_IDX[p]) <= 1:
                adjacent += 1
    # continuous score means by gold if available
    by_gold_scores: dict[str, list[float]] = {k: [] for k in LEVELS}
    for r in rows:
        if r.get("cta_clarity_score") is not None and r["gold_cta_clarity"] in by_gold_scores:
            by_gold_scores[r["gold_cta_clarity"]].append(float(r["cta_clarity_score"]))
    return {
        "n": n,
        "exact": exact,
        "exact_accuracy": exact / n if n else None,
        "adjacent": adjacent,
        "adjacent_accuracy": adjacent / n if n else None,
        "confusion": confusion,
        "pred_dist": {k: sum(1 for r in rows if r["pred_cta_clarity"] == k) for k in LEVELS},
        "gold_dist": {k: sum(1 for r in rows if r["gold_cta_clarity"] == k) for k in LEVELS},
        "score_mean_by_gold": {
            k: (sum(v) / len(v) if v else None) for k, v in by_gold_scores.items()
        },
        "misses": [
            {
                "id": r["id"],
                "gold": r["gold_cta_clarity"],
                "pred": r["pred_cta_clarity"],
                "score": r.get("cta_clarity_score"),
            }
            for r in rows
            if r["pred_cta_clarity"] != r["gold_cta_clarity"]
        ],
        "rows": [
            {
                "id": r["id"],
                "gold": r["gold_cta_clarity"],
                "pred": r["pred_cta_clarity"],
                "score": r.get("cta_clarity_score"),
            }
            for r in rows
        ],
    }


def fmt_pct(x: float | None) -> str:
    if x is None:
        return "n/a"
    return f"{100 * x:.1f}%"


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    results = summary["results"]
    failures = summary.get("failures") or []
    adv = eval_advances(results)
    cta = eval_cta(results)
    summary["metrics"] = {
        "threshold": THRESHOLD,
        "advances_hypothesis": {k: v for k, v in adv.items() if k != "scores"},
        "cta_clarity": {k: v for k, v in cta.items() if k != "rows"},
        "n_items": summary["n"],
        "n_ok": len(results),
        "n_fail": len(failures),
        "model": summary.get("model"),
        "model_resolved": next((r.get("model_resolved") for r in results if r.get("model_resolved")), None),
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# E3 metrics — prototype critique (live Jev)",
        "",
        f"- Dataset: `{summary['dataset']}` (N={summary['n']})",
        f"- Model: `{summary.get('model')}` → `{summary['metrics']['model_resolved']}`",
        f"- Hypothesis: {summary.get('hypothesis', '')}",
        f"- Threshold: noul ≥ {THRESHOLD} → advances yes (1)",
        f"- API ok / fail: {len(results)} / {len(failures)}",
        "",
        "## advances_hypothesis",
        "",
        f"| Metric | Value |",
        f"| --- | --- |",
        f"| N (labeled) | {adv['n']} |",
        f"| Accuracy @0.5 | {adv['correct']}/{adv['n']} = **{fmt_pct(adv['accuracy'])}** |",
        f"| Confusion (tp/tn/fp/fn) | {adv['confusion']['tp']}/{adv['confusion']['tn']}/{adv['confusion']['fp']}/{adv['confusion']['fn']} |",
        f"| False pass rate (fp/N) | **{fmt_pct(adv['false_pass_rate'])}** |",
        f"| ROC-AUC (noul vs gold) | {adv['auc'] if adv['auc'] is None else round(adv['auc'], 3)} |",
        f"| Brier score | {adv['brier'] if adv['brier'] is None else round(adv['brier'], 3)} |",
        f"| Score mean (all / gold1 / gold0) | {adv['score_mean']:.3f} / {adv['score_by_gold']['gold1_mean']:.3f} / {adv['score_by_gold']['gold0_mean']:.3f} |",
        f"| Score range | [{adv['score_min']:.3f}, {adv['score_max']:.3f}] |",
        "",
        "### Misses",
        "",
    ]
    if adv["misses"]:
        for m in adv["misses"]:
            lines.append(f"- `{m['id']}`: gold={m['gold']} pred={m['pred']} noul={m['noul']:.3f}")
    else:
        lines.append("- none")

    lines += [
        "",
        "## cta_clarity",
        "",
        f"| Metric | Value |",
        f"| --- | --- |",
        f"| N (labeled) | {cta['n']} |",
        f"| Exact match | {cta['exact']}/{cta['n']} = **{fmt_pct(cta['exact_accuracy'])}** |",
        f"| Adjacent (±1 level) | {cta['adjacent']}/{cta['n']} = **{fmt_pct(cta['adjacent_accuracy'])}** |",
        f"| Gold dist (low/med/high) | {cta['gold_dist']['low']}/{cta['gold_dist']['medium']}/{cta['gold_dist']['high']} |",
        f"| Pred dist (low/med/high) | {cta['pred_dist']['low']}/{cta['pred_dist']['medium']}/{cta['pred_dist']['high']} |",
        f"| Mean continuous score by gold | low={cta['score_mean_by_gold']['low']}; med={cta['score_mean_by_gold']['medium']}; high={cta['score_mean_by_gold']['high']} |",
        "",
        "### Confusion (rows = gold, cols = pred)",
        "",
        "| gold \\ pred | low | medium | high |",
        "| --- | ---: | ---: | ---: |",
    ]
    for g in LEVELS:
        lines.append(
            f"| {g} | {cta['confusion'][g]['low']} | {cta['confusion'][g]['medium']} | {cta['confusion'][g]['high']} |"
        )

    lines += ["", "### Misses", ""]
    if cta["misses"]:
        for m in cta["misses"]:
            lines.append(f"- `{m['id']}`: gold={m['gold']} pred={m['pred']} score={m['score']}")
    else:
        lines.append("- none")

    lines += [
        "",
        "## Calibration notes",
        "",
        "- advances_hypothesis false-pass (fp) is dangerous for redesign triage: Jev says screen advances when gold says it does not.",
        "- cta_clarity uses argmax over score-level probabilities (same as E1 severity).",
        "- Rubric frozen in `datasets/e3_rubric.md` before API calls.",
        "",
        "## Score distributions",
        "",
        "### advances_hypothesis",
        "",
    ]
    for s in adv["scores"]:
        lines.append(f"- `{s['id']}`: gold={s['gold']} noul={s['noul']:.3f}")
    lines += ["", "### cta_clarity", ""]
    for s in cta["rows"]:
        lines.append(f"- `{s['id']}`: gold={s['gold']} pred={s['pred']} score={s['score']}")

    METRICS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {METRICS}")
    print(json.dumps(summary["metrics"], indent=2))


if __name__ == "__main__":
    main()
