# RAG-System: Arquitectura de Contexto Avanzado

## 🚀 La Diferencia: Re-ranking Semántico Local
A diferencia de los sistemas RAG convencionales que solo usan búsqueda por similitud de coseno, el **Win11 AI Orchestrator** implementa una etapa de **Re-ranking Semántico** utilizando **Ollama** con el modelo **qwen2.5-coder**.

### Flujo de Datos Inteligente
1. **Recuperación (Vector Search):** ChromaDB extrae los *top-K* fragmentos (k=10-20) basados en embeddings.
2. **Filtrado (Semantic Scoring):** El motor local Ollama (acelerado por GPU) evalúa la relevancia real de cada fragmento respecto a la consulta.
3. **Refinamiento:** Solo los *top-N* fragmentos (n=3-5) más relevantes pasan a la ventana de contexto del LLM.

## 🏗️ Pipeline de Ingesta Modular
El sistema no ingesta archivos de forma ciega; sigue un protocolo de **"Limpieza Profunda"**:
*   **Segmentación por Lógica:** El chunking respeta los límites de funciones, clases y bloques de código.
*   **Inyección de Metadata Jerárquica:** Cada fragmento conoce su nivel de importancia (0-4) en el ecosistema.
*   **Normalización de Ecosistema:** Las rutas se almacenan de forma relativa para mantener la portabilidad.

## ⚡ Rendimiento y Hardware
El sistema está diseñado para la estación de trabajo **Acer Predator Helios Neo**:
*   **GPU:** NVIDIA RTX 4060 (8GB VRAM).
*   **Inferencia:** ~30-50 tokens/seg en re-ranking local.
*   **Latencia:** < 2s para recuperar y priorizar contexto complejo.

---
*Dedicación técnica volcada en cada línea de código.*
