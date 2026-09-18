#!/usr/bin/env python3
"""Run TypeSafe Jev (noul) on E2 PRD sections. Requires TYPESAFE_API_KEY."""

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
DATASET = ROOT / "datasets" / "e2_prd_sections.jsonl"
RAW_DIR = ROOT / "runs" / "E2" / "raw"
SUMMARY = ROOT / "runs" / "E2" / "summary.json"
COMPANY = ROOT.parents[1] / "company-context" / "COMPANY.md"
PRODUCT = ROOT.parents[1] / "company-context" / "PRODUCT.md"

METRIC_CONTEXT = (
    "PetCare COMPANY/PRODUCT metric bar (frozen for E2): "
    "Activation = completes feeding-plan setup within 7 days of first open "
    "(schedule, portions, reminders for one or more pets). "
    "North Star ≈ Weekly Active Households with Updated Stock or Confirmed Refill. "
    "Health metrics include 4-week retention, notification opt-in and open-after-notification, "
    "Order-food CTA click-through. A measurable metric names the metric, defines the event "
    "(who/what/when or numerator/denominator), and preferably states baseline/target. "
    "Vague survey vibes or undefined 'happiness' fail this bar."
)

MVP_CRITERIA = {
    "true": (
        "Section tightly gates an MVP/V1 slice: explicit in-scope and/or out-of-scope, "
        "core value loop, deferred features, or hypothesis with validation criteria for a minimal prototype."
    ),
    "false": (
        "Vision/hub/roadmap quarter goals, risk/staffing notes, unbounded feature laundry lists, "
        "or success-story prose that do not define a shippable MVP boundary."
    ),
}

METRIC_CRITERIA = {
    "true": (
        "Named success metric with operational definition (event or numerator/denominator) "
        "and preferably a target/baseline; could be instrumented like COMPANY/PRODUCT metrics."
    ),
    "false": (
        "Vague qualitative vibes, open feedback questions, impact %-deltas without measurement method, "
        "or a metric name+target with no who/what/when definition in the text."
    ),
}


def load_company_snippets() -> str:
    bits = []
    for path, label in ((COMPANY, "COMPANY.md"), (PRODUCT, "PRODUCT.md")):
        if path.exists():
            text = path.read_text(encoding="utf-8")
            # Keep request payload bounded
            bits.append(f"[{label} excerpt]\n{text[:2500]}")
    return "\n\n".join(bits) if bits else METRIC_CONTEXT


def build_payload(row: dict, company_blob: str) -> dict:
    state = {
        "section_title": row.get("section_title") or "",
        "prd_section": row["text"],
        "item_type": row.get("item_type"),
        "source_file": row.get("source_file"),
        "metric_bar": METRIC_CONTEXT,
        "company_product_context": company_blob[:4000],
        "task": "PRD review gate before stakeholder review",
    }
    questions: dict = {}
    if row.get("gold_mvp_scoped") is not None:
        questions["mvp_scoped"] = {
            "type": "noul",
            "instructions": (
                "Is `prd_section` MVP-scoped for PetCare — a tight shippable V1/prototype gate "
                "with clear product boundaries, not vision or unbounded roadmap? "
                "Evaluate the section text itself."
            ),
            "criteria": MVP_CRITERIA,
        }
    if row.get("gold_metric_measurable") is not None:
        questions["metric_measurable"] = {
            "type": "noul",
            "instructions": (
                "Is the success metric in `prd_section` measurable against the PetCare "
                "`metric_bar` / COMPANY-PRODUCT style (named metric + operational definition, "
                "preferably with target)? Evaluate the text as written."
            ),
            "criteria": METRIC_CRITERIA,
        }
    if not questions:
        raise ValueError(f"{row['id']}: no applicable questions")
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
    company_blob = load_company_snippets()
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
        "results": [],
        "failures": [],
    }

    for i, row in enumerate(rows):
        pid = row["id"]
        print(f"[{i+1}/{len(rows)}] {pid} …", flush=True)
        payload = build_payload(row, company_blob)
        raw_path = RAW_DIR / f"{pid}.json"
        try:
            resp = call_jev(api_key, payload)
            raw_path.write_text(
                json.dumps(
                    {"request_meta": {"id": pid, "questions": list(payload["questions"].keys())},
                     "response": resp},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            answers = resp.get("answers") or {}
            entry = {
                "id": pid,
                "item_type": row.get("item_type"),
                "synthetic": bool(row.get("synthetic")),
                "gold_mvp_scoped": row.get("gold_mvp_scoped"),
                "gold_metric_measurable": row.get("gold_metric_measurable"),
                "usage": resp.get("usage"),
                "model_resolved": resp.get("model"),
                "raw_file": str(raw_path.relative_to(ROOT)),
            }
            if "mvp_scoped" in answers:
                noul = float(answers["mvp_scoped"].get("noul"))
                entry["mvp_scoped_noul"] = noul
                entry["pred_mvp_scoped"] = 1 if noul >= 0.5 else 0
            if "metric_measurable" in answers:
                noul = float(answers["metric_measurable"].get("noul"))
                entry["metric_measurable_noul"] = noul
                entry["pred_metric_measurable"] = 1 if noul >= 0.5 else 0
            summary["results"].append(entry)
            bits = []
            if "mvp_scoped_noul" in entry:
                bits.append(
                    f"mvp noul={entry['mvp_scoped_noul']:.3f}→{entry['pred_mvp_scoped']} "
                    f"(gold={row['gold_mvp_scoped']})"
                )
            if "metric_measurable_noul" in entry:
                bits.append(
                    f"metric noul={entry['metric_measurable_noul']:.3f}→{entry['pred_metric_measurable']} "
                    f"(gold={row['gold_metric_measurable']})"
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
