import unittest
from unittest.mock import patch, MagicMock
import os

from core.rag.reranker import OllamaReranker

class TestRerankerSecurity(unittest.TestCase):
    @patch("core.rag.reranker.requests.post")
    def test_ssrf_mitigation_allows_localhost(self, mock_post):
        # Should allow localhost
        os.environ['OLLAMA_ENDPOINT'] = "http://localhost:11434/api/generate"
        reranker = OllamaReranker()

        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "8"}
        mock_post.return_value = mock_response

        score = reranker.score_relevance("query", "context")
        self.assertGreater(score, 0)
        self.assertTrue(mock_post.called)

    @patch("core.rag.reranker.requests.post")
    def test_ssrf_mitigation_allows_127_0_0_1(self, mock_post):
        # Should allow 127.0.0.1
        os.environ['OLLAMA_ENDPOINT'] = "http://127.0.0.1:11434/api/generate"
        reranker = OllamaReranker()

        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "8"}
        mock_post.return_value = mock_response

        score = reranker.score_relevance("query", "context")
        self.assertGreater(score, 0)
        self.assertTrue(mock_post.called)

    @patch("core.rag.reranker.requests.post")
    def test_ssrf_mitigation_blocks_external(self, mock_post):
        # Should block external IPs/domains
        os.environ['OLLAMA_ENDPOINT'] = "http://169.254.169.254/latest/meta-data/"

        with self.assertRaises(ValueError) as context:
            reranker = OllamaReranker()

        self.assertIn("Invalid endpoint", str(context.exception))
        self.assertFalse(mock_post.called)

    @patch("core.rag.reranker.requests.post")
    def test_ssrf_mitigation_blocks_domain(self, mock_post):
        # Should block random domains
        os.environ['OLLAMA_ENDPOINT'] = "http://malicious.com/api/generate"

        with self.assertRaises(ValueError) as context:
            reranker = OllamaReranker()

        self.assertIn("Invalid endpoint", str(context.exception))
        self.assertFalse(mock_post.called)

if __name__ == '__main__':
    unittest.main()
