"""Dense, lexical TF-IDF, and reciprocal-rank fusion on the same Day 6 chunks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from starter.baseline import TfidfIndex
from starter.lab6_retriever import Lab6Retriever


ROOT = Path(__file__).resolve().parents[1]


def load_chunks(path: Path = ROOT / "data" / "nist_chunks.json") -> list[dict[str, Any]]:
    chunks = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(chunks, list) or not chunks:
        raise ValueError(f"No exported chunks in {path}; run starter/prepare_day7.py first")
    return chunks


def accepts_filter(chunk: dict[str, Any], filters: dict[str, Any] | None) -> bool:
    if not filters:
        return True
    if set(filters) != {"section"} or not isinstance(filters["section"], str):
        raise ValueError("Only an explicit section filter is supported")
    return chunk.get("metadata", {}).get("section") == filters["section"]


class DenseSearch:
    name = "dense"

    def __init__(self, day6_root: Path):
        self.retriever = Lab6Retriever(day6_root)

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        return [
            {**hit, "strategy": self.name}
            for hit in self.retriever.search(query, filters=filters, top_k=top_k)
        ]


class TfidfSearch:
    name = "tfidf"

    def __init__(self, chunks: list[dict[str, Any]]):
        self.chunks = chunks
        self.index = TfidfIndex(chunks)

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        if top_k < 1 or not query.strip():
            raise ValueError("query and top_k must be valid")
        if filters:
            # Search all ranked candidates before filtering so a valid filtered hit is
            # not lost simply because it was outside the unfiltered top-k.
            ranked = self.index.search(query, top_k=len(self.chunks))
            return [hit for hit in ranked if accepts_filter(hit, filters)][:top_k]
        return self.index.search(query, top_k=top_k)


class HybridSearch:
    name = "hybrid_rrf"

    def __init__(self, dense: DenseSearch, lexical: TfidfSearch, candidate_k: int = 20, rrf_k: int = 60):
        self.dense = dense
        self.lexical = lexical
        self.candidate_k = candidate_k
        self.rrf_k = rrf_k

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        rank_lists = [
            self.dense.search(query, filters=filters, top_k=max(top_k, self.candidate_k)),
            self.lexical.search(query, filters=filters, top_k=max(top_k, self.candidate_k)),
        ]
        scores: dict[str, float] = {}
        chunks: dict[str, dict[str, Any]] = {}
        for ranking in rank_lists:
            for rank, chunk in enumerate(ranking, start=1):
                cid = chunk["id"]
                scores[cid] = scores.get(cid, 0.0) + 1.0 / (self.rrf_k + rank)
                chunks[cid] = chunk
        ordered = sorted(scores, key=lambda cid: (-scores[cid], cid))[:top_k]
        return [{**chunks[cid], "score": scores[cid], "strategy": self.name} for cid in ordered]


def make_searcher(method: str, day6_root: Path, chunks: list[dict[str, Any]]):
    if method == "dense":
        return DenseSearch(day6_root)
    if method == "tfidf":
        return TfidfSearch(chunks)
    if method == "hybrid_rrf":
        return HybridSearch(DenseSearch(day6_root), TfidfSearch(chunks))
    raise ValueError(f"Unknown retrieval method: {method}")
