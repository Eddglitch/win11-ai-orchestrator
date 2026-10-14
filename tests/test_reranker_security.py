import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock requests before importing the module that uses it
mock_requests = MagicMock()
sys.modules['requests'] = mock_requests

from core.rag.reranker import OllamaReranker

class TestRerankerTimeout(unittest.TestCase):
    def test_score_relevance_has_timeout(self):
        reranker = OllamaReranker()
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "8"}
        mock_requests.post.return_value = mock_response

        reranker.score_relevance("query", "context")

        # Check if timeout was passed
        args, kwargs = mock_requests.post.call_args
        self.assertIn('timeout', kwargs, "timeout parameter is missing in requests.post call")
        self.assertEqual(kwargs['timeout'], 30, f"Expected timeout 30, got {kwargs.get('timeout')}")

if __name__ == '__main__':
    unittest.main()
