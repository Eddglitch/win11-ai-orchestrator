def run():
    with open('tests/test_reranker_security.py', 'r') as f:
        content = f.read()
    content = content.replace('class TestRerankerTimeout(unittest.TestCase):', 'class TestRerankerTimeout(unittest.TestCase):\n    def setUp(self):\n        mock_requests.reset_mock()')
    with open('tests/test_reranker_security.py', 'w') as f:
        f.write(content)
run()
