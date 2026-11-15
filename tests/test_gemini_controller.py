"""Offline contract checks for Gemini response parsing; no API calls."""

import unittest
from unittest.mock import patch

from starter.agentic import run_agent
from src.gemini_controller import GeminiController


class GeminiParsingTests(unittest.TestCase):
    def test_function_call_becomes_search_action(self):
        response = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "thinking text"},
                            {"functionCall": {"name": "search", "args": {"query": "confabulation risks"}}},
                        ]
                    }
                }
            ]
        }
        self.assertEqual(
            GeminiController.normalize_response(response),
            {"action": "search", "query": "confabulation risks"},
        )

    def test_final_answer_keeps_exact_citation_ids(self):
        response = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Có rủi ro [nist-ai-600-1-p010-para-001-000]. "
                                "Cần kiểm tra [nist-ai-600-1-p010-para-001-000]."
                            }
                        ]
                    }
                }
            ]
        }
        result = GeminiController.normalize_response(response)
        self.assertEqual(result["action"], "answer")
        self.assertEqual(result["citations"], ["nist-ai-600-1-p010-para-001-000"])

    def test_missing_candidate_is_an_error(self):
        with self.assertRaises(ValueError):
            GeminiController.normalize_response({"candidates": []})

    def test_missing_search_argument_uses_question_and_records_warning(self):
        response = {"candidates": [{"content": {"parts": [{"functionCall": {"name": "search", "args": {}}}]}}]}
        result = GeminiController.normalize_response(response, fallback_query="NIST confabulation?")
        self.assertEqual(result["query"], "NIST confabulation?")
        self.assertIn("omitted", result["warning"])

    def test_controller_searches_then_answers_with_context(self):
        class Response:
            status_code = 200

            def __init__(self, part):
                self.part = part

            def json(self):
                return {"candidates": [{"content": {"parts": [self.part]}}]}

        class Retriever:
            def search(self, query, *, filters, top_k):
                self.query = query
                return [{
                    "id": "chunk-1",
                    "text": "The document describes confabulation.",
                    "source_id": "doc",
                    "source": "doc.pdf",
                    "page": 1,
                    "metadata": {},
                    "score": 0.8,
                }]

        responses = iter([
            Response({"functionCall": {"name": "search", "args": {"query": "confabulation"}}}),
            Response({"text": "Đó là confabulation [chunk-1]."}),
        ])
        bodies = []

        def fake_post(url, *, headers, json):
            bodies.append(json)
            self.assertNotIn("fake-key", str(json))
            return next(responses)

        controller = GeminiController(api_key="fake-key", min_interval_seconds=0)
        retriever = Retriever()
        try:
            with patch.object(controller.client, "post", side_effect=fake_post):
                result = run_agent("Hiện tượng này là gì?", controller, retriever)
        finally:
            controller.close()
        self.assertEqual(result["status"], "answered")
        self.assertEqual(retriever.query, "confabulation")
        self.assertEqual(result["citations"], ["chunk-1"])
        self.assertEqual([b["toolConfig"]["functionCallingConfig"]["mode"] for b in bodies], ["ANY", "AUTO"])

    def test_retry_after_transient_503(self):
        class Response:
            def __init__(self, status):
                self.status_code = status

            def json(self):
                return {"candidates": [{"content": {"parts": [
                    {"functionCall": {"name": "search", "args": {"query": "NIST"}}}
                ]}}]}

        controller = GeminiController(api_key="fake-key", min_interval_seconds=0)
        try:
            with patch.object(controller.client, "post", side_effect=[Response(503), Response(200)]):
                with patch("src.gemini_controller.time.sleep"):
                    action = controller.decide("NIST?", [])
        finally:
            controller.close()
        self.assertEqual(action["query"], "NIST")
        self.assertEqual([a["status"] for a in controller.http_attempts], [503, 200])


if __name__ == "__main__":
    unittest.main()
