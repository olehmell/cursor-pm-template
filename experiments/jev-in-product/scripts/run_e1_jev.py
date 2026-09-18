#!/usr/bin/env python3
"""Run TypeSafe Jev on E1 interview passages. Requires TYPESAFE_API_KEY."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "datasets" / "e1_interview_passages.jsonl"
RAW_DIR = ROOT / "runs" / "E1" / "raw"
SUMMARY = ROOT / "runs" / "E1" / "summary.json"

ACTIVATION_DEF = (
    "User completes feeding-plan setup within 7 days of first open "
    "(schedule, portions, reminders for one or more pets)."
)

THEME_CRITERIA = {
    "setup_friction": (
        "Difficulty starting or configuring care routines, apps, documents, "
        "feeding schedules, onboarding checklists, or first-weeks adaptation."
    ),
    "notifications": (
        "Forgetting doses/vaccines/walks; need for reminders, calendars, "
        "push signals, or periodic check-ins."
    ),
    "multi_pet": (
        "Balancing or differentiating care across two or more animals "
        "(time split, shared feeding times, different needs)."
    ),
    "trust_data": (
        "Distrust or uncertainty about information sources "
        "(Google horror, conflicting sites, shady labels, unreliable apps, "
        "fragmented clinic records)."
    ),
    "other": (
        "Does not clearly fit the four themes above "
        "(community, travel, gadgets, SOS clinic search, pure emotion, etc.)."
    ),
}

SEVERITY_LEVELS = [
    "low — mild annoyance; unlikely to stop feeding-plan setup within 7 days",
    "medium — noticeable friction; may delay setup but a motivated user can finish in a week",
    "high — strong barrier that plausibly prevents completing feeding-plan setup within 7 days",
]


def build_payload(passage: str) -> dict:
    state = {
        "passage": passage,
        "activation_definition": ACTIVATION_DEF,
        "context": "PetCare interview excerpt for product activation analysis",
    }
    return {
        "state": state,
        "model": MODEL,
        "questions": {
            "theme": {
                "type": "choice",
                "instructions": (
                    "Which primary theme best describes this interview passage "
                    "for product activation analysis? Prefer the theme most "
                    "relevant to whether the user would finish feeding-plan "
                    "setup within 7 days. Use other if none clearly fit."
                ),
                "criteria": THEME_CRITERIA,
            },
            "activation_severity": {
                "type": "score",
                "instructions": (
                    "How severe is the barrier in this passage relative to "
                    "completing feeding-plan setup within 7 days? "
                    "Score activation impact, not overall life severity."
                ),
                "criteria": SEVERITY_LEVELS,
            },
        },
    }


def call_jev(api_key: str, payload: dict, retries: int = 5) -> dict:
    body = json.dumps(payload).encode("utf-8")
    delay = 1.0
    last_err = None
    for attempt in range(retries):
        req = urllib.request.Request(
            API_URL,
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            last_err = f"HTTP {e.code}: {err_body[:500]}"
            if e.code in (429, 529) and attempt < retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 30)
                continue
            raise RuntimeError(last_err) from e
        except Exception as e:
            last_err = str(e)
            if attempt < retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 30)
                continue
            raise
    raise RuntimeError(last_err or "unknown error")


def map_severity(score_answer: dict) -> str:
    """Map probability-weighted score to low|medium|high via nearest level."""
    legend = score_answer.get("legend") or {}
    # Prefer argmax over continuous score for discrete labels
    probs = score_answer.get("probabilities") or {}
    if probs:
        best_idx = max(probs.items(), key=lambda kv: kv[1])[0]
        label = legend.get(str(best_idx), legend.get(best_idx, ""))
    else:
        score = float(score_answer.get("score", 0))
        rounded = int(round(score))
        label = legend.get(str(rounded), "")
    label_l = label.lower()
    for name in ("low", "medium", "high"):
        if label_l.startswith(name) or f" {name}" in label_l or label_l == name:
            return name
    # Fallback: continuous score bands 0,1,2
    score = float(score_answer.get("score", 1))
    if score < 0.5:
        return "low"
    if score < 1.5:
        return "medium"
    return "high"


def main() -> int:
    api_key = os.environ.get("TYPESAFE_API_KEY", "")
    print(f"TYPESAFE_API_KEY length: {len(api_key)}", flush=True)
    if not api_key:
        print("ERROR: TYPESAFE_API_KEY missing — aborting, no fake results.", file=sys.stderr)
        return 2

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    with DATASET.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    summary = {
        "model": MODEL,
        "dataset": str(DATASET.relative_to(ROOT)),
        "n": len(rows),
        "results": [],
        "failures": [],
    }

    for i, row in enumerate(rows):
        pid = row["id"]
        print(f"[{i+1}/{len(rows)}] {pid} …", flush=True)
        payload = build_payload(row["passage"])
        raw_path = RAW_DIR / f"{pid}.json"
        try:
            resp = call_jev(api_key, payload)
            raw_path.write_text(
                json.dumps({"request_meta": {"id": pid}, "response": resp}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            answers = resp.get("answers") or {}
            theme_a = answers.get("theme") or {}
            sev_a = answers.get("activation_severity") or {}
            pred_theme = theme_a.get("choice")
            pred_sev = map_severity(sev_a) if sev_a else None
            entry = {
                "id": pid,
                "gold_theme": row["gold_theme"],
                "gold_severity": row["gold_severity"],
                "pred_theme": pred_theme,
                "pred_severity": pred_sev,
                "theme_confidence": theme_a.get("confidence"),
                "severity_score": sev_a.get("score"),
                "severity_confidence": sev_a.get("confidence"),
                "theme_probabilities": theme_a.get("probabilities"),
                "severity_probabilities": sev_a.get("probabilities"),
                "severity_legend": sev_a.get("legend"),
                "usage": resp.get("usage"),
                "raw_file": str(raw_path.relative_to(ROOT)),
            }
            summary["results"].append(entry)
            print(
                f"  theme={pred_theme} (gold={row['gold_theme']}) "
                f"sev={pred_sev} (gold={row['gold_severity']})",
                flush=True,
            )
        except Exception as e:
            msg = str(e)
            print(f"  FAIL: {msg}", flush=True)
            summary["failures"].append({"id": pid, "error": msg})
            raw_path.write_text(
                json.dumps({"request_meta": {"id": pid}, "error": msg}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        time.sleep(0.4)  # polite pacing

    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {SUMMARY} — ok={len(summary['results'])} fail={len(summary['failures'])}", flush=True)
    return 0 if not summary["failures"] else 1


if __name__ == "__main__":
    sys.exit(main())
