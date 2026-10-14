from core.rag.reranker import OllamaReranker

reranker = OllamaReranker()
print(reranker.score_relevance("test query", "test context"))
