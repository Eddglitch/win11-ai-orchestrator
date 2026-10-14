import unittest
from unittest.mock import patch

from core.rag.reranker import OllamaReranker

class TestOllamaRerankerException(unittest.TestCase):
    def setUp(self):
        self.reranker = OllamaReranker()

    @patch("core.rag.reranker.requests.post")
    def test_score_relevance_exception_fallback(self, mock_post):
        # Configure the mock to raise an exception
        mock_post.side_effect = Exception("Simulated network failure")

        # Call the method
        query = "test query"
        context = "test context"
        score = self.reranker.score_relevance(query, context)

        # Check if score defaults to 0.5 when an exception occurs
        self.assertEqual(score, 0.5)

        # Verify that post was called
        mock_post.assert_called_once()

if __name__ == "__main__":
    unittest.main()
