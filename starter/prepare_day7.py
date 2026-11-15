"""Export the Day 6 paragraph index and freeze a fresh Day 7 benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import chromadb


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = "nist-ai-600-1"

# New held-out test questions. None of these appeared in the Day 6 benchmark.
# Evidence strings are checked against the exported Chroma chunks before writing.
NEW_TEST = [
    {
        "id": "d7-t01",
        "question": "Theo GV-1.7-001, tổ chức cần chuẩn bị khả năng nào cho hệ thống AI tạo sinh?",
        "expected_answer": "Có quy trình để vô hiệu hóa hệ thống khi cần.",
        "page": 21,
        "evidence": "GV-1.7-001 Protocols are put in place to ensure GAI systems are able to be deactivated when necessary.",
    },
    {
        "id": "d7-t02",
        "question": "Chức năng giám sát tổ chức nên bao phủ những giai đoạn nào của vòng đời AI tạo sinh?",
        "expected_answer": "Từ xác định bài toán và chuỗi cung ứng tới khi ngừng hệ thống.",
        "page": 23,
        "evidence": "across the GAI lifecycle, from problem formulation and supply chains to system decommission.",
    },
    {
        "id": "d7-t03",
        "question": "GV-5.1-001 yêu cầu phân bổ những gì cho việc tiếp nhận phản hồi và khắc phục?",
        "expected_answer": "Thời gian và nguồn lực.",
        "page": 24,
        "evidence": "GV-5.1-001 Allocate time and resources for outreach, feedback, and recourse processes in GAI system development.",
    },
    {
        "id": "d7-t04",
        "question": "Khi rủi ro vượt ngưỡng chấp nhận, MS-2.6-003 yêu cầu làm gì với mô hình đã tinh chỉnh?",
        "expected_answer": "Đánh giá lại các tính năng an toàn của mô hình.",
        "page": 36,
        "evidence": "MS-2.6-003 Re-evaluate safety features of fine-tuned models when the negative risk exceeds organizational risk tolerance.",
    },
    {
        "id": "d7-t05",
        "question": "MG-3.2-008 đề xuất dùng cách gì để xem lại nội dung được AI tạo ra khi phù hợp?",
        "expected_answer": "Dùng hệ thống kiểm duyệt bởi con người.",
        "page": 48,
        "evidence": "MG-3.2-008 Use human moderation systems where appropriate to review generated content",
    },
]

NO_EVIDENCE = [
    {
        "id": "d7-d16",
        "split": "dev",
        "question": "NIST AI 600-1 nêu tên bệnh viện nào ở Việt Nam đã triển khai kiểm soát confabulation?",
        "absence_reason": "Tài liệu là hồ sơ quản lý rủi ro, không phải danh sách triển khai tại bệnh viện Việt Nam.",
        "absence_check": "Vietnam",
    },
    {
        "id": "d7-d17",
        "split": "dev",
        "question": "Theo NIST AI 600-1, lệ phí bắt buộc bằng USD để được chứng nhận tuân thủ là bao nhiêu?",
        "absence_reason": "Tài liệu không quy định chương trình chứng nhận hay bảng lệ phí tuân thủ.",
        "absence_check": "certification fee",
    },
    {
        "id": "d7-t06",
        "split": "test",
        "question": "NIST AI 600-1 cho biết tỷ lệ confabulation của Gemini 3.8 Flash vào năm 2026 là bao nhiêu?",
        "absence_reason": "Tài liệu xuất bản năm 2024, không thể báo cáo phép đo model ra năm 2026.",
        "absence_check": "Gemini 3.8 Flash",
    },
    {
        "id": "d7-t07",
        "split": "test",
        "question": "NIST AI 600-1 đã chứng nhận sản phẩm AI nào đạt chuẩn vào năm 2026?",
        "absence_reason": "Tài liệu là profile rủi ro, không phải danh sách sản phẩm được chứng nhận năm 2026.",
        "absence_check": "certified products",
    },
]


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6-root", required=True, type=Path)
    args = parser.parse_args()
    day6 = args.day6_root.expanduser().resolve()
    index_path = day6 / ".cache" / "chroma" / "chroma.sqlite3"
    if not index_path.is_file():
        parser.error(f"Day 6 Chroma index not found: {index_path}")

    collection = chromadb.PersistentClient(path=str(index_path.parent)).get_collection(
        "lab6_paragraph", embedding_function=None
    )
    raw = collection.get(include=["documents", "metadatas"])
    chunks = []
    for chunk_id, text, meta in zip(raw["ids"], raw["documents"], raw["metadatas"]):
        chunks.append(
            {
                "id": chunk_id,
                "text": text,
                "source_id": meta["document_id"],
                "source": meta["source"],
                "page": meta["page"],
                "metadata": {"section": meta["section"]},
            }
        )
    chunks.sort(key=lambda chunk: chunk["id"])
    if len(chunks) != len({chunk["id"] for chunk in chunks}):
        raise ValueError("Duplicate chunk IDs")

    old = json.loads((day6 / "benchmark" / "gold_questions.json").read_text(encoding="utf-8"))
    questions = []
    for item in old:
        if item["split"] != "dev":
            continue  # Day 6 test was inspected; it must not be reused as held-out test.
        converted = {
            "id": item["id"],
            "split": "dev",
            "question": item["question"],
            "answerable": True,
            "expected_answer": item["expected_answer"],
            "gold": [
                {
                    "source_id": item["gold_source_id"],
                    "page": item["gold_page"],
                    "evidence": item["evidence_quote"],
                }
            ],
        }
        if "filter" in item:
            converted["filter"] = item["filter"]
        questions.append(converted)

    for item in NEW_TEST:
        questions.append(
            {
                "id": item["id"],
                "split": "test",
                "question": item["question"],
                "answerable": True,
                "expected_answer": item["expected_answer"],
                "gold": [
                    {
                        "source_id": SOURCE_ID,
                        "page": item["page"],
                        "evidence": item["evidence"],
                    }
                ],
            }
        )
    for item in NO_EVIDENCE:
        questions.append(
            {
                "id": item["id"],
                "split": item["split"],
                "question": item["question"],
                "answerable": False,
                "expected_behavior": "search_and_abstain",
                "absence_reason": item["absence_reason"],
            }
        )
        if any(item["absence_check"].casefold() in chunk["text"].casefold() for chunk in chunks):
            raise ValueError(f"Absence check phrase unexpectedly appears: {item['id']}")

    if len(questions) != 24 or len({q["id"] for q in questions}) != 24:
        raise ValueError("Expected exactly 24 unique questions")
    for split, answerable, expected in (
        ("dev", True, 15),
        ("dev", False, 2),
        ("test", True, 5),
        ("test", False, 2),
    ):
        actual = sum(q["split"] == split and q["answerable"] is answerable for q in questions)
        if actual != expected:
            raise ValueError(f"{split}/{answerable}: {actual} instead of {expected}")
    for q in questions:
        if not q["answerable"]:
            continue
        for gold in q["gold"]:
            if not any(
                c["source_id"] == gold["source_id"]
                and c["page"] == gold["page"]
                and gold["evidence"] in c["text"]
                for c in chunks
            ):
                raise ValueError(f"Evidence is not wholly contained in a chunk: {q['id']}")

    write_json(ROOT / "data" / "nist_chunks.json", chunks)
    write_json(ROOT / "data" / "benchmark_day7.json", questions)
    print(f"Exported {len(chunks)} chunks and {len(questions)} questions (17 dev, 7 test).")


if __name__ == "__main__":
    main()
