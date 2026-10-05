import os
import requests
from typing import List, Dict


class OllamaReranker:
    """
    Motor de Re-ranking Semántico optimizado para GPU (NVIDIA RTX 4060).
    Utiliza un modelo local (qwen2.5-coder) para evaluar la relevancia
    de los fragmentos recuperados de la base vectorial.
    """

    def __init__(self, model: str = "qwen2.5-coder:7b"):
        self.model = model
        self.endpoint = os.getenv(
            "OLLAMA_ENDPOINT", "http://localhost:11434/api/generate"
        )

    def score_relevance(self, query: str, context: str) -> float:
        """
        Evalúa la relevancia de un contexto respecto a una consulta.
        Retorna un puntaje de 0.0 a 1.0.
        """
        prompt = f"""
        Query: {query}
        Context: {context}
        
        Evalúa del 0 al 10 qué tan útil es el contexto para responder la consulta.
        Responde SOLO con un número.
        """

        payload = {"model": self.model, "prompt": prompt, "stream": False}

        try:
            response = requests.post(self.endpoint, json=payload, timeout=30)
            score_text = response.json().get("response", "0").strip()
            # Sanitización de salida del modelo local
            score = float("".join(c for c in score_text if c.isdigit() or c == "."))
            return score / 10.0
        except Exception as e:
            print(f"Error en re-ranking local: {e}")
            return 0.5  # Valor neutral en caso de fallo

    def rerank(self, query: str, documents: List[Dict], top_n: int = 3) -> List[Dict]:
        """
        Ordena los documentos recuperados por relevancia semántica real.
        """
        scored_docs = []
        for doc in documents:
            score = self.score_relevance(query, doc.get("content", ""))
            doc["rerank_score"] = score
            scored_docs.append(doc)

        # Ordenar descendente por el nuevo score de re-ranking
        return sorted(scored_docs, key=lambda x: x["rerank_score"], reverse=True)[
            :top_n
        ]
