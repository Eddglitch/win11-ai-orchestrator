import sys
from unittest.mock import MagicMock

# Mock requests module
mock_requests = MagicMock()
sys.modules['requests'] = mock_requests

from core.rag.reranker import OllamaReranker

def test_reranker_timeout():
    reranker = OllamaReranker()

    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": "8"}
    mock_requests.post.return_value = mock_response

    # Call the method
    score = reranker.score_relevance("test query", "test context")

    # Check if timeout was passed
    if mock_requests.post.called:
        args, kwargs = mock_requests.post.call_args
        if 'timeout' in kwargs:
            print(f"SUCCESS: timeout={kwargs['timeout']} was passed to requests.post")
        else:
            print("FAILURE: timeout was NOT passed to requests.post")
            sys.exit(1)
    else:
        print("FAILURE: requests.post was not called")
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_reranker_timeout()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
