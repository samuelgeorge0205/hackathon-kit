# Tech stack cheat sheet — one sentence per tool, so anyone can answer "why this?"

Fill in / adjust based on what you actually use tomorrow — but this
covers the stack from tonight's build, likely to recur.

| Tech | One-sentence explanation | Why we chose it |
|---|---|---|
| **FastAPI** | A Python web framework for building REST APIs, with automatic docs and type validation. | Fast to build with, and the auto-generated `/docs` page is genuinely useful to show a jury live. |
| **LangGraph** | A library for building multi-step AI workflows as an explicit graph, where the graph itself can branch based on the data. | Makes our escalation decision an auditable, visible step instead of buried if/else logic in a script. |
| **LangChain** | A library that gives a consistent interface for calling different LLM/embedding providers. | Lets us swap between the contest gateway, Ollama, or Groq by changing one config value, not rewriting code. |
| **Chroma** | A local vector database — stores text as embeddings and finds similar text by meaning, not keyword matching. | Powers our RAG grounding — retrieving relevant historical precedent before the LLM generates a recommendation. |
| **RAG (Retrieval-Augmented Generation)** | Retrieving relevant real information and feeding it to the LLM as context, instead of letting it answer from memory alone. | Reduces hallucination — our recommendations are grounded in actual precedent records. |
| **Multi-agent system** | Multiple single-responsibility AI/logic components that pass state to each other, versus one component doing everything. | Each piece is independently testable/explainable, and later steps can build on earlier steps' output (e.g. risk assessment informs the recommendation). |
| **React + TypeScript** | A frontend framework with compile-time type checking. | Type safety catches mismatches between our API and UI before runtime. |
| **React Query** | A library for fetching, caching, and auto-refreshing server data in a React app. | Handles loading/error states and our mock-data fallback cleanly, without hand-rolled state management. |
| **Pydantic** | A Python library for data validation using type hints. | Guarantees our API always returns data in the shape the frontend expects — invalid data gets rejected before it ships. |
| **Ollama / local LLM** | Runs open-weight language models locally on your own machine, no internet or API key required. | Backup/portable option so the demo doesn't depend on a specific gateway being reachable. |

## The 10-second version if someone asks "what's your tech stack" cold

"Python and FastAPI on the backend, a multi-agent pipeline built with
LangGraph and LangChain, RAG grounding via Chroma, and a React
TypeScript frontend talking to it over a REST API — all switchable
between the contest's LLM gateway and a local model."
