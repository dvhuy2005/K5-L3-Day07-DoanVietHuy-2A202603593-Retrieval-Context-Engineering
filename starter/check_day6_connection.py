"""Read the Day 6 dense index and try one real question (Lab 7, step 1)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


COLLECTION = "lab6_paragraph"


def find_day6_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()

    workspace = Path(__file__).resolve().parents[3]
    candidates = [
        path
        for path in (workspace / "Lab6").iterdir()
        if path.is_dir()
        and (path / ".cache" / "chroma" / "chroma.sqlite3").is_file()
        and (path / "data" / "manifest.json").is_file()
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Found {len(candidates)} usable Day 6 folders under {workspace / 'Lab6'}; "
            "pass --day6-root explicitly."
        )
    return candidates[0]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="A question to search for in the Day 6 NIST index")
    parser.add_argument("--day6-root", type=Path, help="Path to the completed Day 6 repo")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to show (default: 3)")
    args = parser.parse_args()

    if not args.question.strip():
        parser.error("question must not be empty")
    if args.top_k < 1:
        parser.error("--top-k must be positive")

    try:
        import chromadb
        from fastembed import TextEmbedding

        day6 = find_day6_root(args.day6_root)
        index_path = day6 / ".cache" / "chroma"
        cache_path = day6 / ".cache" / "fastembed"
        if not (index_path / "chroma.sqlite3").is_file():
            raise FileNotFoundError(f"Day 6 Chroma index is missing: {index_path}")
        if not cache_path.is_dir():
            raise FileNotFoundError(f"Day 6 embedding cache is missing: {cache_path}")

        client = chromadb.PersistentClient(path=str(index_path))
        collection = client.get_collection(COLLECTION, embedding_function=None)
        count = collection.count()
        if count == 0:
            raise ValueError(f"Collection {COLLECTION} is empty")

        metadata = collection.metadata or {}
        model_name = metadata.get("model_name")
        dimensions = metadata.get("dimensions")
        if not isinstance(model_name, str) or not isinstance(dimensions, int):
            raise ValueError("Day 6 collection does not record its embedding model and dimensions")

        model = TextEmbedding(model_name=model_name, cache_dir=str(cache_path))
        vector = next(iter(model.query_embed(args.question))).tolist()
        if len(vector) != dimensions:
            raise ValueError(f"Query vector has {len(vector)} dimensions; index requires {dimensions}")

        result = collection.query(
            query_embeddings=[vector],
            n_results=min(args.top_k, count),
            include=["documents", "metadatas", "distances"],
        )
        print(f"Day 6: {day6}")
        print(f"Collection: {COLLECTION} ({count} chunks)")
        print(f"Embedding: {model_name} ({dimensions} dimensions)")
        print(f"Question: {args.question}\n")
        for rank, (chunk_id, document, meta, distance) in enumerate(
            zip(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0],
            ),
            start=1,
        ):
            print(f"[{rank}] ID: {chunk_id}")
            print(f"    Source: {meta.get('source', '?')} | page: {meta.get('page', '?')}")
            print(f"    Cosine similarity: {1.0 - float(distance):.3f}")
            print(f"    Text: {document}\n")
        return 0
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Connection check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
