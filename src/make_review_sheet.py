"""Prepare an honest human review sheet from a completed Gemini trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .retrieval import ROOT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traces", type=Path, required=True)
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    benchmark = {
        q["id"]: q
        for q in json.loads((ROOT / "data" / "benchmark_day7.json").read_text(encoding="utf-8"))
        if q["split"] == args.split
    }
    traces = json.loads(args.traces.read_text(encoding="utf-8"))
    if len(traces) != len(benchmark) or len({t["query_id"] for t in traces}) != len(traces):
        raise ValueError("Agent trace is incomplete or has duplicate query IDs")
    lines = [
        f"# Review {args.split}: read the cited chunks before assigning labels",
        "",
        "Do not infer citation support from a matching ID alone. Mark each factual "
        "claim against the actual chunk text and the full question.",
        "",
    ]
    labels = []
    for trace in traces:
        qid = trace["query_id"]
        if qid not in benchmark:
            raise ValueError(f"Trace {qid} is not part of the requested split")
        q = benchmark[qid]
        lines += [
            f"## {qid}",
            "",
            f"- Question: {q['question']}",
            f"- Answerable: {q['answerable']}",
            f"- Status: {trace['status']}",
            f"- Agent answer: {trace.get('answer') or '(empty)'}",
            f"- Citations: {trace.get('citations', [])}",
            f"- Expected answer: {q.get('expected_answer', '(abstain)')}",
            f"- Gold evidence: {q.get('gold', q.get('absence_reason'))}",
            f"- Final context IDs: {next((e.get('context_ids', []) for e in reversed(trace.get('events', [])) if e.get('event') == 'search'), [])}",
            "- Reviewer notes: [fill]",
            "- Citation support per citation: [fill true/false after reading]",
            "- Answer grade 0/1/2 or abstention correctness: [fill]",
            "",
        ]
        if trace["status"] == "error":
            continue
        label = {"query_id": qid, "citation_support": [None] * len(trace.get("citations", []))}
        if q["answerable"]:
            label["answer_grade"] = None
        else:
            label["abstention_correct"] = None
        labels.append(label)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    labels_path = args.output.with_name("reviews_template.json")
    labels_path.write_text(json.dumps(labels, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output} and {labels_path}; labels remain blank until reviewed.")


if __name__ == "__main__":
    main()
