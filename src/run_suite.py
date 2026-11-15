"""Run the fixed Gemini baseline/selected dev and test suite with a temporary key."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from .retrieval import ROOT


CONFIGS = [
    ("dev", "baseline", 3, 800),
    ("dev", "selected", 10, 3000),
    ("test", "baseline", 3, 800),
    ("test", "selected", 10, 3000),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6-root", required=True, type=Path)
    parser.add_argument("--model", default="gemini-3.5-flash-lite")
    parser.add_argument("--timeout", type=float, default=35)
    parser.add_argument("--stage", choices=("dev", "test", "all"), default="all")
    args = parser.parse_args()

    # Use the user's normal local Temp, not the sandbox's redirected TEMP.
    key_path = Path.home() / "AppData" / "Local" / "Temp" / "lab7-gemini-key.tmp"
    if not key_path.is_file():
        parser.error(f"Temporary key file is missing: {key_path}")
    key = key_path.read_text(encoding="utf-8").strip()
    if not key:
        parser.error("Temporary key file is empty")
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = key
    summary = []
    try:
        for split, label, top_k, budget in CONFIGS:
            if args.stage != "all" and split != args.stage:
                continue
            output = ROOT / "results" / f"agent_{split}_{label}"
            print(f"Running {split}/{label} (top_k={top_k}, budget={budget})", flush=True)
            command = [
                sys.executable,
                "-X",
                "utf8",
                "-m",
                "src.run_live",
                "--day6-root",
                str(args.day6_root),
                "--split",
                split,
                "--method",
                "dense",
                "--top-k",
                str(top_k),
                "--budget",
                str(budget),
                "--model",
                args.model,
                "--timeout",
                str(args.timeout),
                "--output",
                str(output),
                "--resume",
            ]
            for recovery_attempt in range(3):
                result = subprocess.run(command, cwd=ROOT, env=env, check=False)
                if result.returncode == 0:
                    break
                trace_path = output / "traces.json"
                traces = json.loads(trace_path.read_text(encoding="utf-8")) if trace_path.is_file() else []
                last_error = traces[-1].get("error", "") if traces and traces[-1].get("status") == "error" else ""
                recoverable = any(
                    phrase in last_error for phrase in ("HTTP 429", "HTTP 503", "timed out", "connection failed")
                )
                if not recoverable or recovery_attempt == 2:
                    break
                delay = 20 * (recovery_attempt + 1)
                print(f"Transient provider error; resuming in {delay} seconds.", flush=True)
                time.sleep(delay)
            run_summary_path = output / "summary.json"
            if run_summary_path.is_file():
                summary.append(json.loads(run_summary_path.read_text(encoding="utf-8")))
            suite_path = ROOT / "results" / "agent_suite_summary.json"
            suite_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if result.returncode != 0:
                print(f"Stopped after {split}/{label} error; completed cases can be resumed.", file=sys.stderr)
                return 1
        return 0
    finally:
        env.pop("GEMINI_API_KEY", None)
        key = ""
        key_path.unlink(missing_ok=True)
        print("Removed the temporary key file.", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
