import unittest
from tests.test_reranker_security import TestRerankerTimeout
import sys

# Need to run it directly to see why mock_requests.post isn't called
def main():
    test = TestRerankerTimeout('test_score_relevance_has_timeout')
    test.setUp()

    from core.rag.reranker import OllamaReranker
    reranker = OllamaReranker()
    print("Endpoint:", reranker.endpoint)

    import requests
    print("Requests post type:", type(requests.post))
    print("Is it MagicMock:", isinstance(requests.post, unittest.mock.MagicMock))

    reranker.score_relevance("test", "test")

    import sys
    mock = sys.modules['requests']
    print("Sys modules post called:", mock.post.called)

if __name__ == '__main__':
    main()
