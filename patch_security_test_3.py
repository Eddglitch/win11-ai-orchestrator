def run():
    with open('tests/test_reranker_security.py', 'r') as f:
        content = f.read()
    content = content.replace('def setUp(self):\n        mock_requests.reset_mock()', 'def setUp(self):\n        mock_requests.reset_mock()\n        mock_requests.post.reset_mock()\n        mock_requests.post.side_effect = None\n')
    with open('tests/test_reranker_security.py', 'w') as f:
        f.write(content)
run()
