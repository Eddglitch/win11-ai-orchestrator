import os
import re
from typing import List, Dict

class IngestionPipeline:
    """
    Pipeline de ingesta avanzado para el Orquestador.
    Encargado de transformar archivos brutos en fragmentos de conocimiento estructurado.
    """

    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.dev_home = os.getenv("DEV_HOME", ".")

    def clean_content(self, text: str, extension: str) -> str:
        """
        Limpia el contenido según el lenguaje (sanitización de ruido).
        """
        if extension in ['.py', '.js', '.ts', '.ps1']:
            # Normalización de espacios y remoción de comentarios excesivos
            text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()

    def get_metadata(self, file_path: str) -> Dict:
        """
        Extrae la 'Memoria Espacial' del archivo (Niveles de importancia).
        """
        # Sanitización de rutas locales en metadata
        relative_path = os.path.relpath(file_path, start=self.dev_home)
        
        return {
            "source": relative_path,
            "ecosystem": "win11-ai-orchestrator",
            "importance": self._infer_importance(file_path)
        }

    def _infer_importance(self, path: str) -> int:
        """
        Infiere la importancia del archivo según su ubicación en la jerarquía.
        (Niveles 0-4 de la Memoria Espacial).
        """
        if "GEMINI.md" in path: return 0 # Nivel Global
        if "core/" in path: return 1     # Nivel Ecosistema
        return 3 # Nivel Operativo

    def create_chunks(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Divide el texto en fragmentos lógicos manteniendo el solapamiento.
        """
        # Lógica de chunking semántico simplificada
        chunks = []
        if not text:
            return chunks
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk_content = text[i:i + self.chunk_size]
            chunks.append({
                "content": chunk_content,
                "metadata": metadata,
                "length": len(chunk_content)
            })
            if i + self.chunk_size >= len(text):
                break
        return chunks
