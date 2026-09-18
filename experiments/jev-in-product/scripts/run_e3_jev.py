#!/usr/bin/env python3
"""Run TypeSafe Jev on E3 prototype screens. Requires TYPESAFE_API_KEY."""

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
DATASET = ROOT / "datasets" / "e3_screens.jsonl"
RAW_DIR = ROOT / "runs" / "E3" / "raw"
SUMMARY = ROOT / "runs" / "E3" / "summary.json"

HYPOTHESIS = (
    "Users want to store pet medical documents in the app via photo upload "
    "(PetID Digital Vet Passport MVP)."
)

ADVANCE_CRITERIA = {
    "true": (
        "Screen meaningfully advances storing pet medical docs via photo upload: "
        "invite capture, preview/confirm upload, upload progress/success, empty state "
        "prompting document upload, gallery of stored docs, or viewer of stored medical photos."
    ),
    "false": (
        "Unrelated surface (feeding, community, clinic map, profile/privacy, marketing), "
        "delete-only confirmation that removes docs, text-date entry without photo upload, "
        "or copy that never enables medical-doc photo storage."
    ),
}

CTA_LEVELS = [
    "low — vague primary label (Next/Continue/OK), competing equal CTAs, or upload action buried",
    "medium — primary exists but icon-only, slightly ambiguous, or secondary-styled yet discoverable",
    "high — one clear primary with action label matching the intended next step; visually dominant",
]


def map_cta(score_answer: dict) -> str:
    legend = score_answer.get("legend") or {}
    probs = score_answer.get("probabilities") or {}
    if probs:
        best_idx = max(probs.items(), key=lambda kv: kv[1])[0]
        label = legend.get(str(best_idx), legend.get(best_idx, ""))
    else:
        score = float(score_answer.get("score", 0))
        label = legend.get(str(int(round(score))), "")
    label_l = label.lower()
    for name in ("low", "medium", "high"):
        if label_l.startswith(name) or f" {name}" in label_l or label_l == name:
            return name
    score = float(score_answer.get("score", 1))
    if score < 0.5:
        return "low"
    if score < 1.5:
        return "medium"
    return "high"


def build_payload(row: dict) -> dict:
    state = {
        "hypothesis": HYPOTHESIS,
        "screen_id": row.get("screen_id") or "",
        "screen_description": row["screen_description"],
        "primary_cta_label": row.get("primary_cta"),
        "has_primary_cta": bool(row.get("has_primary_cta")),
        "task": "Prototype critique before user testing — redesign priority",
    }
    questions: dict = {
        "advances_hypothesis": {
            "type": "noul",
            "instructions": (
                "Given `hypothesis` and `screen_description`, does this screen meaningfully "
                "advance testing or delivering photo upload of pet medical documents? "
                "Evaluate the screen as described."
            ),
            "criteria": ADVANCE_CRITERIA,
        }
    }
    if row.get("gold_cta_clarity") is not None and row.get("has_primary_cta"):
        questions["cta_clarity"] = {
            "type": "score",
            "instructions": (
                "How clear is the primary CTA on this screen for a user trying to complete "
                "photo upload / storage of a pet medical document? "
                "Score the primary control described (label, prominence, competition). "
                "If the screen is not about upload, still score clarity of the stated primary CTA."
            ),
            "criteria": CTA_LEVELS,
        }
    return {"state": state, "model": MODEL, "questions": questions}


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
        "threshold": 0.5,
        "hypothesis": HYPOTHESIS,
        "results": [],
        "failures": [],
    }

    for i, row in enumerate(rows):
        pid = row["id"]
        print(f"[{i+1}/{len(rows)}] {pid} …", flush=True)
        payload = build_payload(row)
        raw_path = RAW_DIR / f"{pid}.json"
        try:
            resp = call_jev(api_key, payload)
            raw_path.write_text(
                json.dumps(
                    {
                        "request_meta": {
                            "id": pid,
                            "questions": list(payload["questions"].keys()),
                        },
                        "response": resp,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            answers = resp.get("answers") or {}
            entry = {
                "id": pid,
                "screen_id": row.get("screen_id"),
                "synthetic": bool(row.get("synthetic")),
                "gold_advances_hypothesis": row.get("gold_advances_hypothesis"),
                "gold_cta_clarity": row.get("gold_cta_clarity"),
                "usage": resp.get("usage"),
                "model_resolved": resp.get("model"),
                "raw_file": str(raw_path.relative_to(ROOT)),
            }
            if "advances_hypothesis" in answers:
                noul = float(answers["advances_hypothesis"].get("noul"))
                entry["advances_hypothesis_noul"] = noul
                entry["pred_advances_hypothesis"] = 1 if noul >= 0.5 else 0
            if "cta_clarity" in answers:
                cta_a = answers["cta_clarity"]
                entry["cta_clarity_score"] = cta_a.get("score")
                entry["cta_clarity_confidence"] = cta_a.get("confidence")
                entry["cta_clarity_probabilities"] = cta_a.get("probabilities")
                entry["cta_clarity_legend"] = cta_a.get("legend")
                entry["pred_cta_clarity"] = map_cta(cta_a)
            summary["results"].append(entry)
            bits = []
            if "advances_hypothesis_noul" in entry:
                bits.append(
                    f"adv noul={entry['advances_hypothesis_noul']:.3f}→{entry['pred_advances_hypothesis']} "
                    f"(gold={row['gold_advances_hypothesis']})"
                )
            if "pred_cta_clarity" in entry:
                bits.append(
                    f"cta={entry['pred_cta_clarity']} (gold={row['gold_cta_clarity']})"
                )
            print("  " + "; ".join(bits), flush=True)
        except Exception as e:
            msg = str(e)
            print(f"  FAIL: {msg}", flush=True)
            summary["failures"].append({"id": pid, "error": msg})
            raw_path.write_text(
                json.dumps({"request_meta": {"id": pid}, "error": msg}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        time.sleep(0.4)

    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Wrote {SUMMARY} — ok={len(summary['results'])} fail={len(summary['failures'])}",
        flush=True,
    )
    return 0 if not summary["failures"] else 1


if __name__ == "__main__":
    sys.exit(main())
