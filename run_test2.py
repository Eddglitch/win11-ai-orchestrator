import sys
from unittest.mock import patch, MagicMock
mock_requests = MagicMock()
sys.modules['requests'] = mock_requests

from core.rag.reranker import OllamaReranker
reranker = OllamaReranker()
reranker.score_relevance("test", "test")
print("Sys modules post called:", mock_requests.post.called)
