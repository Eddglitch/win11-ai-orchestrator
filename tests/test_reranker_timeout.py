import unittest
from unittest.mock import patch, MagicMock
import sys

# Mocking requests because it's not installed in the environment
mock_requests = MagicMock()
sys.modules["requests"] = mock_requests

from core.rag.reranker import OllamaReranker

class TestOllamaReranker(unittest.TestCase):
    def setUp(self):
        self.reranker = OllamaReranker()

    @patch("core.rag.reranker.requests.post")
    def test_score_relevance_timeout(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "8"}
        mock_post.return_value = mock_response

        # Call the method
        query = "test query"
        context = "test context"
        score = self.reranker.score_relevance(query, context)

        # Check if score is correct
        self.assertEqual(score, 0.8)

        # Verify that post was called with timeout=30
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs.get('timeout'), 30)

if __name__ == "__main__":
    unittest.main()
