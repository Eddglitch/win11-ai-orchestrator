# win11-ai-orchestrator - Memoria del Ecosistema

## 🧠 Filosofía: Memoria Espacial y Contexto Modular
Este ecosistema utiliza una estructura de **Memoria Recursiva (Niveles 0-4)**. Cada directorio es un universo autocontenido con su propio archivo `GEMINI.md`.

### Estructura de Memoria
* **Nivel 0 (Global):** Configuración maestra y protocolos de seguridad.
* **Nivel 1 (Ecosistema):** Estructura macro de carpetas (`Config`, `Projects`, `Tools`).
* **Nivel 2 (Índice):** Catálogo de proyectos activos y sus dependencias.
* **Nivel 3 (Historia):** Bitácora de decisiones arquitectónicas y contextos pasados.
* **Nivel 4 (Operativa):** Detalles técnicos específicos del código actual.

## 🛡️ Mandatos de Desarrollo (Templates)
Todo nuevo proyecto en este orquestador DEBE seguir estos axiomas:
1. **Encapsulamiento:** Prohibido dependencias cruzadas sin interfaces.
2. **Modularidad:** Uso de **Lazy Loading** en PowerShell para mantener eficiencia.
3. **Hermetismo:** Los datos temporales viven y mueren dentro de la carpeta del proyecto.

## 🚀 Cómo Replicar este Sistema
1. Configura `$env:DEV_HOME` en tu perfil de PowerShell.
2. Clona la estructura de `core/powershell` en tu directorio de configuración.
3. Inicia un nuevo proyecto usando la plantilla `templates/new_project_gemini.md`.

---
**Firmado:** win11-ai-orchestrator (AI Framework)
