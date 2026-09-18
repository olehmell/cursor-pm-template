#!/usr/bin/env python3
"""U5 Template skill router — one systemone call per PM ask (Choice + gate + fits).

Requires TYPESAFE_API_KEY. Prints key length only; never prints the key.
"""

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
DATASET = ROOT / "datasets" / "u5_pm_asks.jsonl"
ROSTER_PATH = ROOT / "datasets" / "u5_skill_roster.json"
RAW_DIR = ROOT / "runs" / "U5" / "raw"
SUMMARY = ROOT / "runs" / "U5" / "summary.json"

GATE_THRESHOLD = 0.30
FITS_THRESHOLD = 0.30

CHOICE_INSTRUCTIONS = (
    "Which of these template skills, if any, is the right one to load to help with "
    "the PM's latest request in this Cursor product-management template?"
)

GATE_QUESTIONS = {
    "acts_on_product_artifacts": (
        "Is the assistant being asked to produce or analyze product artifacts "
        "(interviews, metrics reports, PRDs, prototypes/screens), rather than only "
        "to chat, explain a concept, or handle unrelated tasks?"
    ),
    "would_follow_template_workflow": (
        "Would a careful PM answering this follow a documented template workflow "
        "(usecase README/AGENTS with prescribed steps, templates, or screen scaffolds), "
        "rather than answering from general PM knowledge alone?"
    ),
    "prose_suffices": (
        "Could a knowledgeable generalist fully satisfy this request in prose, with "
        "no template skills, no usecase folders, and no product artifacts to create "
        "or analyze?"
    ),
}
INVERTED = {"prose_suffices"}


def load_roster() -> list[dict]:
    return json.loads(ROSTER_PATH.read_text(encoding="utf-8"))


def build_payload(ask: str, roster: list[dict]) -> dict:
    state = {
        "request": ask,
        "context": (
            "Cursor PM template with three usecase skills: data-analysis, prd-writing, "
            "prototyping. Suggest at most one skill to load for this turn."
        ),
    }
    questions: dict = {
        "which": {
            "type": "choice",
            "instructions": CHOICE_INSTRUCTIONS,
            "criteria": {s["name"]: s["description"] for s in roster},
        }
    }
    for key, text in GATE_QUESTIONS.items():
        questions[f"gate::{key}"] = {"type": "noul", "instructions": text}
    for s in roster:
        name = s["name"]
        questions[f"fits::{name}"] = {
            "type": "noul",
            "instructions": (
                f"Does the skill '{name}' do the specific thing the PM's request asks "
                f"for? It is described as: {s['description_full']}"
            ),
        }
    return {"state": state, "model": MODEL, "questions": questions}


def decide(answers: dict) -> dict:
    """Apply U5 decision rule. Prefer Choice `which` when fits clear the threshold."""
    gate_vals = {}
    for key in GATE_QUESTIONS:
        ans = answers.get(f"gate::{key}") or {}
        gate_vals[key] = float(ans["noul"])
    oriented = [(1.0 - v) if k in INVERTED else v for k, v in gate_vals.items()]
    gate = sum(oriented) / len(oriented)

    fits = {}
    for key, ans in answers.items():
        if key.startswith("fits::"):
            fits[key.removeprefix("fits::")] = float(ans["noul"])

    which_ans = answers.get("which") or {}
    choice = which_ans.get("choice")
    probs = which_ans.get("probabilities") or {}
    conf = which_ans.get("confidence")

    pred = None
    reason = "gate_below"
    if gate < GATE_THRESHOLD:
        reason = "gate_below"
        pred = None
    elif not fits or max(fits.values()) < FITS_THRESHOLD:
        reason = "fits_below"
        pred = None
    else:
        # Prefer Choice when at least one fit is above threshold.
        pred = choice
        reason = "choice_winner"
        # Safety: if Choice missing, fall back to highest fits.
        if not pred:
            pred = max(fits, key=fits.get)
            reason = "fits_argmax_fallback"

    return {
        "gate": gate,
        "gate_values": gate_vals,
        "fits": fits,
        "which_choice": choice,
        "which_probabilities": probs,
        "which_confidence": conf,
        "pred_skill": pred,
        "decision_reason": reason,
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


def main() -> int:
    api_key = os.environ.get("TYPESAFE_API_KEY", "")
    print(f"TYPESAFE_API_KEY length: {len(api_key)}", flush=True)
    if not api_key:
        print("ERROR: TYPESAFE_API_KEY missing — aborting, no fake results.", file=sys.stderr)
        return 2

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    roster = load_roster()
    rows = []
    with DATASET.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    summary = {
        "model": MODEL,
        "dataset": str(DATASET.relative_to(ROOT)),
        "roster": str(ROSTER_PATH.relative_to(ROOT)),
        "n": len(rows),
        "gate_threshold": GATE_THRESHOLD,
        "fits_threshold": FITS_THRESHOLD,
        "decision_rule": (
            "gate=mean(oriented gate nouls); if gate<0.30 → null; "
            "elif max(fits)<0.30 → null; else winner=Choice which"
        ),
        "results": [],
        "failures": [],
    }

    for i, row in enumerate(rows):
        pid = row["id"]
        ask = row["ask"]
        gold = row.get("gold_skill")  # may be null
        print(f"[{i+1}/{len(rows)}] {pid} …", flush=True)
        payload = build_payload(ask, roster)
        raw_path = RAW_DIR / f"{pid}.json"
        try:
            resp = call_jev(api_key, payload)
            answers = resp.get("answers") or {}
            decision = decide(answers)
            raw_path.write_text(
                json.dumps(
                    {
                        "request_meta": {
                            "id": pid,
                            "ask": ask,
                            "gold_skill": gold,
                            "questions": list(payload["questions"].keys()),
                        },
                        "decision": decision,
                        "response": resp,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            entry = {
                "id": pid,
                "bucket": row.get("bucket"),
                "gold_skill": gold,
                "pred_skill": decision["pred_skill"],
                "gate": decision["gate"],
                "gate_values": decision["gate_values"],
                "fits": decision["fits"],
                "which_choice": decision["which_choice"],
                "which_probabilities": decision["which_probabilities"],
                "which_confidence": decision["which_confidence"],
                "decision_reason": decision["decision_reason"],
                "usage": resp.get("usage"),
                "model_resolved": resp.get("model"),
                "raw_file": str(raw_path.relative_to(ROOT)),
            }
            summary["results"].append(entry)
            print(
                f"  gate={decision['gate']:.3f} pred={decision['pred_skill']!r} "
                f"gold={gold!r} reason={decision['decision_reason']} "
                f"which={decision['which_choice']}",
                flush=True,
            )
        except Exception as e:
            msg = str(e)
            print(f"  FAIL: {msg}", flush=True)
            summary["failures"].append({"id": pid, "error": msg})
            raw_path.write_text(
                json.dumps(
                    {"request_meta": {"id": pid, "ask": ask, "gold_skill": gold}, "error": msg},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        time.sleep(0.35)

    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Wrote {SUMMARY} — ok={len(summary['results'])} fail={len(summary['failures'])}",
        flush=True,
    )
    return 0 if not summary["failures"] else 1


if __name__ == "__main__":
    sys.exit(main())
