#!/usr/bin/env python3
"""Compute E2 metrics from runs/E2/summary.json → metrics.md (+ enrich summary)."""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "runs" / "E2" / "summary.json"
METRICS = ROOT / "runs" / "E2" / "metrics.md"
THRESHOLD = 0.5


def auc_binary(scores: list[float], labels: list[int]) -> float | None:
    """Mann–Whitney / ROC AUC for binary labels. None if one class only."""
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return None
    # Wilcoxon-Mann-Whitney
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


def eval_task(results: list[dict], gold_key: str, noul_key: str, pred_key: str) -> dict:
    rows = [r for r in results if r.get(gold_key) is not None and noul_key in r]
    golds = [int(r[gold_key]) for r in rows]
    scores = [float(r[noul_key]) for r in rows]
    preds = [int(r[pred_key]) for r in rows]
    n = len(rows)
    correct = sum(p == g for p, g in zip(preds, golds))
    cm = conf_mat(preds, golds)
    false_pass = cm["fp"] / n if n else 0.0  # dangerous for shipping
    return {
        "n": n,
        "accuracy": correct / n if n else None,
        "correct": correct,
        "confusion": cm,
        "false_pass_rate": false_pass,
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
                "gold": int(r[gold_key]),
                "pred": int(r[pred_key]),
                "noul": float(r[noul_key]),
            }
            for r in rows
            if int(r[pred_key]) != int(r[gold_key])
        ],
        "scores": [{"id": r["id"], "gold": int(r[gold_key]), "noul": float(r[noul_key])} for r in rows],
    }


def fmt_pct(x: float | None) -> str:
    if x is None:
        return "n/a"
    return f"{100 * x:.1f}%"


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    results = summary["results"]
    failures = summary.get("failures") or []
    mvp = eval_task(results, "gold_mvp_scoped", "mvp_scoped_noul", "pred_mvp_scoped")
    metric = eval_task(
        results, "gold_metric_measurable", "metric_measurable_noul", "pred_metric_measurable"
    )
    summary["metrics"] = {
        "threshold": THRESHOLD,
        "mvp_scoped": {k: v for k, v in mvp.items() if k != "scores"},
        "metric_measurable": {k: v for k, v in metric.items() if k != "scores"},
        "n_items": summary["n"],
        "n_ok": len(results),
        "n_fail": len(failures),
        "model": summary.get("model"),
        "model_resolved": next((r.get("model_resolved") for r in results if r.get("model_resolved")), None),
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# E2 metrics — PRD review gates (live Jev)",
        "",
        f"- Dataset: `{summary['dataset']}` (N={summary['n']})",
        f"- Model: `{summary.get('model')}` → `{summary['metrics']['model_resolved']}`",
        f"- Threshold: noul ≥ {THRESHOLD} → yes (1)",
        f"- API ok / fail: {len(results)} / {len(failures)}",
        "",
        "## mvp_scoped",
        "",
        f"| Metric | Value |",
        f"| --- | --- |",
        f"| N (labeled) | {mvp['n']} |",
        f"| Accuracy @0.5 | {mvp['correct']}/{mvp['n']} = **{fmt_pct(mvp['accuracy'])}** |",
        f"| Confusion (tp/tn/fp/fn) | {mvp['confusion']['tp']}/{mvp['confusion']['tn']}/{mvp['confusion']['fp']}/{mvp['confusion']['fn']} |",
        f"| False pass rate (fp/N) | **{fmt_pct(mvp['false_pass_rate'])}** |",
        f"| ROC-AUC (noul vs gold) | {mvp['auc'] if mvp['auc'] is None else round(mvp['auc'], 3)} |",
        f"| Brier score | {mvp['brier'] if mvp['brier'] is None else round(mvp['brier'], 3)} |",
        f"| Score mean (all / gold1 / gold0) | {mvp['score_mean']:.3f} / {mvp['score_by_gold']['gold1_mean']:.3f} / {mvp['score_by_gold']['gold0_mean']:.3f} |",
        f"| Score range | [{mvp['score_min']:.3f}, {mvp['score_max']:.3f}] |",
        "",
        "### Misses",
        "",
    ]
    if mvp["misses"]:
        for m in mvp["misses"]:
            lines.append(f"- `{m['id']}`: gold={m['gold']} pred={m['pred']} noul={m['noul']:.3f}")
    else:
        lines.append("- none")

    lines += [
        "",
        "## metric_measurable",
        "",
        f"| Metric | Value |",
        f"| --- | --- |",
        f"| N (labeled) | {metric['n']} |",
        f"| Accuracy @0.5 | {metric['correct']}/{metric['n']} = **{fmt_pct(metric['accuracy'])}** |",
        f"| Confusion (tp/tn/fp/fn) | {metric['confusion']['tp']}/{metric['confusion']['tn']}/{metric['confusion']['fp']}/{metric['confusion']['fn']} |",
        f"| False pass rate (fp/N) | **{fmt_pct(metric['false_pass_rate'])}** |",
        f"| ROC-AUC (noul vs gold) | {metric['auc'] if metric['auc'] is None else round(metric['auc'], 3)} |",
        f"| Brier score | {metric['brier'] if metric['brier'] is None else round(metric['brier'], 3)} |",
        f"| Score mean (all / gold1 / gold0) | {metric['score_mean']:.3f} / {metric['score_by_gold']['gold1_mean']:.3f} / {metric['score_by_gold']['gold0_mean']:.3f} |",
        f"| Score range | [{metric['score_min']:.3f}, {metric['score_max']:.3f}] |",
        "",
        "### Misses",
        "",
    ]
    if metric["misses"]:
        for m in metric["misses"]:
            lines.append(f"- `{m['id']}`: gold={m['gold']} pred={m['pred']} noul={m['noul']:.3f}")
    else:
        lines.append("- none")

    lines += [
        "",
        "## Calibration notes",
        "",
        "- Compare mean noul on gold=1 vs gold=0; separation indicates usable ranking even when @0.5 accuracy is modest.",
        "- False pass (fp) is the dangerous error for shipping: Jev says yes when gold is no.",
        "- Rubric frozen in `datasets/e2_rubric.md` before API calls.",
        "",
        "## Score distributions (id, gold, noul)",
        "",
        "### mvp_scoped",
        "",
    ]
    for s in mvp["scores"]:
        lines.append(f"- `{s['id']}`: gold={s['gold']} noul={s['noul']:.3f}")
    lines += ["", "### metric_measurable", ""]
    for s in metric["scores"]:
        lines.append(f"- `{s['id']}`: gold={s['gold']} noul={s['noul']:.3f}")

    METRICS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {METRICS}")
    print(json.dumps(summary["metrics"], indent=2))


if __name__ == "__main__":
    main()
