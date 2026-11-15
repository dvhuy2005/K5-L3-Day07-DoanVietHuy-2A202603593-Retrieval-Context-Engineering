"""Measure retrieval and packed context on a frozen Day 7 benchmark split."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

from starter.baseline import pack_context

from .retrieval import ROOT, load_chunks, make_searcher


def has_evidence(chunk: dict, gold: list[dict]) -> bool:
    return any(
        chunk["source_id"] == item["source_id"]
        and chunk["page"] == item["page"]
        and item["evidence"] in chunk["text"]
        for item in gold
    )


def evaluate(method: str, split: str, day6_root: Path, top_k: int, budget: int) -> tuple[dict, list[dict]]:
    if top_k < 3 or budget < 1:
        raise ValueError("top_k must be >= 3 and budget must be positive")
    chunks = load_chunks()
    questions = json.loads((ROOT / "data" / "benchmark_day7.json").read_text(encoding="utf-8"))
    selected = [q for q in questions if q["split"] == split]
    if not selected:
        raise ValueError(f"No questions for {split}")
    searcher = make_searcher(method, day6_root, chunks)
    traces = []
    for q in selected:
        started = time.perf_counter()
        # The filter, when present, is explicitly supplied by the benchmark query.
        # Gold answer/page/evidence never enters the searcher.
        results = searcher.search(q["question"], filters=q.get("filter"), top_k=top_k)
        context, ids = pack_context(results, budget=budget)
        elapsed_ms = (time.perf_counter() - started) * 1000
        gold = q.get("gold", [])
        marked = [{**item, "hit": has_evidence(item, gold) if q["answerable"] else None} for item in results]
        traces.append(
            {
                "query_id": q["id"],
                "split": split,
                "question": q["question"],
                "answerable": q["answerable"],
                "method": method,
                "top_k": top_k,
                "budget_chars": budget,
                "filter": q.get("filter"),
                "results": marked,
                "context": context,
                "context_ids": ids,
                "elapsed_ms": round(elapsed_ms, 2),
                "hit1": bool(marked and marked[0]["hit"]) if q["answerable"] else None,
                "hit3": any(item["hit"] for item in marked[:3]) if q["answerable"] else None,
                "context_hit": any(item["hit"] and item["id"] in ids for item in marked)
                if q["answerable"]
                else None,
            }
        )
    answerable = [trace for trace in traces if trace["answerable"]]
    n = len(answerable)
    summary = {
        "method": method,
        "split": split,
        "top_k": top_k,
        "budget_chars": budget,
        "answerable": n,
        "unanswerable": len(traces) - n,
        "hit_at_1": {"n": sum(t["hit1"] for t in answerable), "N": n},
        "evidence_hit_at_3": {"n": sum(t["hit3"] for t in answerable), "N": n},
        "context_evidence_rate": {"n": sum(t["context_hit"] for t in answerable), "N": n},
        "median_search_and_pack_ms": round(statistics.median(t["elapsed_ms"] for t in traces), 2),
        "local_retrieval_api_cost_usd": 0,
    }
    return summary, traces


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6-root", required=True, type=Path)
    parser.add_argument("--split", required=True, choices=("dev", "test"))
    parser.add_argument("--method", required=True, choices=("dense", "tfidf", "hybrid_rrf"))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--budget", type=int, default=800)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    summary, traces = evaluate(args.method, args.split, args.day6_root, args.top_k, args.budget)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "traces.json").write_text(json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
