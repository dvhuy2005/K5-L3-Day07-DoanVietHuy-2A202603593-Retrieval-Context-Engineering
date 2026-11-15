"""Run the real Gemini retrieval agent on one question or a benchmark split."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from starter.agentic import run_agent

from .gemini_controller import GeminiController
from .retrieval import ROOT, load_chunks, make_searcher


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6-root", required=True, type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--question")
    group.add_argument("--split", choices=("dev", "test"))
    parser.add_argument("--method", choices=("dense", "tfidf", "hybrid_rrf"), default="dense")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--budget", type=int, default=3000)
    parser.add_argument("--max-searches", type=int, default=4)
    parser.add_argument("--model", default="gemini-3.5-flash-lite")
    parser.add_argument("--timeout", type=float, default=35)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "agent_live")
    parser.add_argument("--resume", action="store_true", help="Continue a partial run with the same configuration")
    args = parser.parse_args()

    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is missing in this terminal; set it before running Gemini.", file=sys.stderr)
        return 2

    chunks = load_chunks()
    searcher = make_searcher(args.method, args.day6_root, chunks)
    if args.question:
        cases = [{"id": "manual", "question": args.question, "filter": None}]
    else:
        benchmark = json.loads((ROOT / "data" / "benchmark_day7.json").read_text(encoding="utf-8"))
        # The controller receives only question text and the user-supplied filter;
        # expected answer and gold evidence are never included in its input.
        cases = [
            {"id": item["id"], "question": item["question"], "filter": item.get("filter")}
            for item in benchmark
            if item["split"] == args.split
        ]

    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    traces = []
    if args.resume and (output / "traces.json").is_file():
        previous = json.loads((output / "traces.json").read_text(encoding="utf-8"))
        for trace in previous:
            if trace.get("status") == "error":
                continue
            if (trace.get("method"), trace.get("top_k"), trace.get("budget_chars"), trace.get("model")) != (
                args.method, args.top_k, args.budget, args.model
            ):
                raise ValueError("Cannot resume traces from another configuration")
            traces.append(trace)
    done = {trace["query_id"] for trace in traces}
    if len(done) != len(traces) or not done.issubset({case["id"] for case in cases}):
        raise ValueError("Cannot resume traces with duplicate or unrelated query IDs")
    errors = 0
    for case in cases:
        if case["id"] in done:
            continue
        controller = GeminiController(model=args.model, timeout_seconds=args.timeout)
        started = time.perf_counter()
        try:
            result = run_agent(
                case["question"],
                controller,
                searcher,
                filters=case["filter"],
                max_searches=args.max_searches,
                top_k=args.top_k,
                budget=args.budget,
                prefer_latest=True,
            )
        except (RuntimeError, ValueError, OSError) as exc:
            errors += 1
            result = {
                "status": "error",
                "answer": "",
                "citations": [],
                "events": [],
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        finally:
            controller.close()
        last_search = next((e for e in reversed(result.get("events", [])) if e.get("event") == "search"), {})
        traces.append(
            {
                "query_id": case["id"],
                "question": case["question"],
                "method": args.method,
                "top_k": args.top_k,
                "budget_chars": args.budget,
                "model": args.model,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                **result,
                "final_context": last_search.get("context", ""),
                "model_calls": controller.calls,
                "http_attempts": controller.http_attempts,
            }
        )
        save_json(output / "traces.json", traces)
        print(f"{case['id']}: {result['status']}")
        if args.question and result.get("answer"):
            print(result["answer"])
        if errors:
            print("Stopping after the first provider error; no quality score is assigned.", file=sys.stderr)
            break

    summary = {
        "method": args.method,
        "split": args.split or "manual",
        "model": args.model,
        "requested_cases": len(cases),
        "attempted_cases": len(traces),
        "answered": sum(t["status"] == "answered" for t in traces),
        "abstained": sum(t["status"] == "abstain" for t in traces),
        "provider_or_tool_errors": errors,
        "model_calls": sum(len(t["model_calls"]) for t in traces),
        "input_tokens_reported": sum(
            call["usage"].get("promptTokenCount", 0)
            for trace in traces
            for call in trace["model_calls"]
        ),
        "output_tokens_reported": sum(
            call["usage"].get("candidatesTokenCount", 0)
            for trace in traces
            for call in trace["model_calls"]
        ),
        "api_cost_usd": None,
        "complete": len(traces) == len(cases) and errors == 0,
    }
    save_json(output / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
