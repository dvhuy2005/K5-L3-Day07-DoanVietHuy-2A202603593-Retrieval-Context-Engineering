from pathlib import Path
import chromadb
from fastembed import TextEmbedding

class Lab6Retriever:
    def __init__(self, day6_root: Path):
        index_path = day6_root / ".cache" / "chroma"

        if not (index_path / "chroma.sqlite3").is_file():
            raise FileNotFoundError(f"Không thấy kho Chroma: {index_path}")

        client = chromadb.PersistentClient(path=str(index_path))
        self.collection = client.get_collection(
            "lab6_paragraph", embedding_function=None
        )
        info = self.collection.metadata or {}
        self.model_name = info["model_name"]
        self.dimensions = info["dimensions"]

        cache_path = day6_root / ".cache" / "fastembed"
        self.embedder = TextEmbedding(
            model_name=self.model_name,
            cache_dir=str(cache_path),
        )

    def search(self, query: str, *, filters: dict | None, top_k: int) -> list[dict]:
        if not query.strip() or top_k < 1:
            raise ValueError("Câu tìm kiếm hoặc top_k không hợp lệ")

        vector = next(iter(self.embedder.query_embed(query))).tolist()
        if len(vector) != self.dimensions:
            raise ValueError("Vector câu hỏi không khớp với kho dữ liệu")

        results = self.collection.query(
            query_embeddings=[vector],
            n_results=min(top_k, self.collection.count()),
            where=filters or None,
            include=["documents", "metadatas", "distances"],
        )

        chunks = []
        for chunk_id, text, meta, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            chunks.append({
                "id": chunk_id,
                "text": text,
                "source_id": meta["document_id"],
                "source": meta["source"],
                "page": meta["page"],
                "metadata": {"section": meta["section"]},
                "score": 1.0 - float(distance),
            })
        return chunks
