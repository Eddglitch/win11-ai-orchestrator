import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock requests before importing the module that uses it
mock_requests = MagicMock()
sys.modules["requests"] = mock_requests

from core.rag.reranker import OllamaReranker

class TestOllamaReranker(unittest.TestCase):
    def setUp(self):
        # Reset mock before each test
        mock_requests.reset_mock()
        mock_requests.post.side_effect = None
        self.reranker = OllamaReranker()

    def test_score_relevance_success(self):
        # Mock response from requests.post
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "8.5"}
        mock_requests.post.return_value = mock_response

        score = self.reranker.score_relevance("test query", "test context")

        self.assertEqual(score, 0.85)
        mock_requests.post.assert_called_once()
        # Verify the keyword 'json' in requests.post still works (it's a kwarg, not using the json module)
        args, kwargs = mock_requests.post.call_args
        self.assertIn('json', kwargs)
        self.assertEqual(kwargs['json']['prompt'].strip(), """Query: test query
        Context: test context

        Evalúa del 0 al 10 qué tan útil es el contexto para responder la consulta.
        Responde SOLO con un número.""".strip())

    def test_rerank(self):
        # Mock responses for multiple documents
        mock_response1 = MagicMock()
        mock_response1.json.return_value = {"response": "9.0"}
        mock_response2 = MagicMock()
        mock_response2.json.return_value = {"response": "4.0"}

        mock_requests.post.side_effect = [mock_response1, mock_response2]

        docs = [
            {"content": "good content", "id": 1},
            {"content": "bad content", "id": 2}
        ]

        reranked = self.reranker.rerank("query", docs, top_n=2)

        self.assertEqual(len(reranked), 2)
        self.assertEqual(reranked[0]["id"], 1)
        self.assertEqual(reranked[0]["rerank_score"], 0.9)
        self.assertEqual(reranked[1]["id"], 2)
        self.assertEqual(reranked[1]["rerank_score"], 0.4)

if __name__ == "__main__":
    unittest.main()
