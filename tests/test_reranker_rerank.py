import unittest
from unittest.mock import patch, MagicMock
from core.rag.reranker import OllamaReranker

class TestRerankerRerank(unittest.TestCase):
    def setUp(self):
        self.reranker = OllamaReranker()

    def test_rerank_sorts_and_truncates(self):
        # Mock score_relevance to return deterministic scores
        def mock_score_relevance(query, context):
            context_lower = context.lower()
            if "high" in context_lower:
                return 0.9
            elif "medium" in context_lower:
                return 0.5
            elif "low" in context_lower:
                return 0.1
            return 0.0

        self.reranker.score_relevance = MagicMock(side_effect=mock_score_relevance)

        documents = [
            {"id": 1, "content": "This is a low relevance document."},
            {"id": 2, "content": "This has medium relevance."},
            {"id": 3, "content": "Another low one."},
            {"id": 4, "content": "High relevance document!"},
            {"id": 5, "content": "Also medium relevance."},
        ]

        # Call rerank with top_n = 3
        result = self.reranker.rerank("query", documents, top_n=3)

        # Ensure correct number of documents are returned
        self.assertEqual(len(result), 3)

        # Ensure they are sorted by score descending
        self.assertEqual(result[0]["id"], 4) # high -> 0.9
        self.assertTrue(result[1]["id"] in [2, 5]) # medium -> 0.5
        self.assertTrue(result[2]["id"] in [2, 5]) # medium -> 0.5

        # Check that score_relevance was called 5 times
        self.assertEqual(self.reranker.score_relevance.call_count, 5)

        # Check rerank_score attribute is added correctly
        self.assertEqual(result[0]["rerank_score"], 0.9)
        self.assertEqual(result[1]["rerank_score"], 0.5)

    def test_rerank_with_empty_documents(self):
        self.reranker.score_relevance = MagicMock(return_value=0.5)
        result = self.reranker.rerank("query", [], top_n=3)
        self.assertEqual(result, [])
        self.reranker.score_relevance.assert_not_called()

    def test_rerank_preserves_other_keys(self):
        self.reranker.score_relevance = MagicMock(return_value=0.8)
        documents = [{"content": "test", "extra": "value"}]
        result = self.reranker.rerank("query", documents)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["extra"], "value")
        self.assertEqual(result[0]["rerank_score"], 0.8)

if __name__ == "__main__":
    unittest.main()
