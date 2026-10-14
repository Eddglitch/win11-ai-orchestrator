def run():
    with open('tests/test_reranker_security.py', 'r') as f:
        content = f.read()
    content = content.replace('args, kwargs = mock_requests.post.call_args', 'self.assertTrue(mock_requests.post.called, "requests.post was not called")\n        args, kwargs = mock_requests.post.call_args')
    with open('tests/test_reranker_security.py', 'w') as f:
        f.write(content)
run()
