"""
Centralized configuration for the SCOUT AI backend.

Single source of truth for LLM/embedding providers, keys, data paths, and
API settings. Every other module (agents/, api/) imports from here instead
of hardcoding values.

--- Switching models/providers ---

Set ONE variable to switch everything:

    SCOUT_LLM_PROVIDER=ollama        # chat model provider
    SCOUT_EMBEDDING_PROVIDER=ollama  # embedding provider (defaults to
                                      # SCOUT_LLM_PROVIDER if unset)

Built-in profiles are in PROVIDERS below: contest, ollama, groq, openai.
Chat and embeddings can use DIFFERENT providers -- e.g. Groq (fast, free
tier, no embeddings) for chat + Ollama (local) for embeddings:

    SCOUT_LLM_PROVIDER=groq
    SCOUT_EMBEDDING_PROVIDER=ollama
    SCOUT_GROQ_API_KEY=gsk_...

To use a different MODEL within the same provider (e.g. Ollama's qwen2.5
instead of llama3.2) without changing provider, set the specific override:

    SCOUT_LLM_PROVIDER=ollama
    SCOUT_CHAT_MODEL=qwen2.5

Any SCOUT_GATEWAY_URL / SCOUT_CHAT_MODEL / SCOUT_API_KEY / SCOUT_VERIFY_SSL
set explicitly always wins over the provider's default -- profiles are
just sensible starting points, not a cage.

Run `uv run python config.py` any time to print exactly what's resolved
(with the key masked) -- the fastest way to confirm a switch took effect
before you spend a request on it.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads backend/.env if present; safe no-op otherwise

# ---------------------------------------------------------------------------
# Named provider profiles. Add a new one here and it's immediately
# selectable via SCOUT_LLM_PROVIDER / SCOUT_EMBEDDING_PROVIDER -- no other
# code changes needed.
# ---------------------------------------------------------------------------
PROVIDERS = {
    "contest": {
        "gateway_url": "https://genailab.tcs.in",
        "chat_model": "azure_ai/genailab-maas-DeepSeek-V3-0324",
        "embedding_model": "azure/genailab-maas-text-embedding-3-large",
        # event-scoped key, kept as a working default for the contest lab only
        "api_key": os.getenv("SCOUT_CONTEST_API_KEY", "sk-92oRc9dRnbaZF6OvqmvfrA"),
        "verify_ssl": False,  # corporate proxy breaks normal cert verification
        "supports_embeddings": True,
    },
    "ollama": {
        "gateway_url": "http://localhost:11434/v1",
        "chat_model": "llama3.2",
        "embedding_model": "nomic-embed-text",
        "api_key": "ollama",  # any non-empty string works, Ollama doesn't check it
        "verify_ssl": True,
        "supports_embeddings": True,
    },
    "groq": {
        "gateway_url": "https://api.groq.com/openai/v1",
        "chat_model": "llama-3.3-70b-versatile",
        "embedding_model": None,
        "api_key": os.getenv("SCOUT_GROQ_API_KEY", ""),
        "verify_ssl": True,
        "supports_embeddings": False,  # Groq serves no embedding endpoint
    },
    "openai": {
        "gateway_url": "https://api.openai.com/v1",
        "chat_model": "gpt-4o-mini",
        "embedding_model": "text-embedding-3-small",
        "api_key": os.getenv("SCOUT_OPENAI_API_KEY", ""),
        "verify_ssl": True,
        "supports_embeddings": True,
    },
}


def _resolve_profile(name: str, var_name: str) -> dict:
    if name not in PROVIDERS:
        raise ValueError(
            f"Unknown provider '{name}' for {var_name}. "
            f"Available: {', '.join(PROVIDERS)}"
        )
    return PROVIDERS[name]


LLM_PROVIDER = os.getenv("SCOUT_LLM_PROVIDER", "contest")
EMBEDDING_PROVIDER = os.getenv("SCOUT_EMBEDDING_PROVIDER", LLM_PROVIDER)

_chat = _resolve_profile(LLM_PROVIDER, "SCOUT_LLM_PROVIDER")
_embed = _resolve_profile(EMBEDDING_PROVIDER, "SCOUT_EMBEDDING_PROVIDER")

if not _embed["supports_embeddings"]:
    _alternatives = [k for k, v in PROVIDERS.items() if v["supports_embeddings"]]
    raise ValueError(
        f"Provider '{EMBEDDING_PROVIDER}' doesn't serve embeddings. "
        f"Set SCOUT_EMBEDDING_PROVIDER to one of: {', '.join(_alternatives)} "
        f"(SCOUT_LLM_PROVIDER can stay '{LLM_PROVIDER}' -- chat and "
        f"embeddings are resolved independently)."
    )

# --- chat client settings (explicit SCOUT_* vars always override the profile) ---
GATEWAY_URL = os.getenv("SCOUT_GATEWAY_URL", _chat["gateway_url"])
CHAT_MODEL = os.getenv("SCOUT_CHAT_MODEL", _chat["chat_model"])
API_KEY = os.getenv("SCOUT_API_KEY", _chat["api_key"])
VERIFY_SSL = os.getenv("SCOUT_VERIFY_SSL", str(_chat["verify_ssl"])).lower() == "true"

# --- embedding client settings (independent -- may be a different provider) ---
EMBEDDING_GATEWAY_URL = os.getenv("SCOUT_EMBEDDING_GATEWAY_URL", _embed["gateway_url"])
EMBEDDING_MODEL = os.getenv("SCOUT_EMBEDDING_MODEL", _embed["embedding_model"])
EMBEDDING_API_KEY = os.getenv("SCOUT_EMBEDDING_API_KEY", _embed["api_key"])
EMBEDDING_VERIFY_SSL = os.getenv("SCOUT_EMBEDDING_VERIFY_SSL", str(_embed["verify_ssl"])).lower() == "true"

if not API_KEY and LLM_PROVIDER != "ollama":
    raise ValueError(
        f"No API key set for SCOUT_LLM_PROVIDER='{LLM_PROVIDER}'. "
        f"Set SCOUT_{LLM_PROVIDER.upper()}_API_KEY in your .env."
    )
if not EMBEDDING_API_KEY and EMBEDDING_PROVIDER != "ollama":
    raise ValueError(
        f"No API key set for SCOUT_EMBEDDING_PROVIDER='{EMBEDDING_PROVIDER}'. "
        f"Set SCOUT_{EMBEDDING_PROVIDER.upper()}_API_KEY in your .env."
    )

# --- data & storage paths ---
DATA_DIR = os.getenv("SCOUT_DATA_DIR", "./data")
CHROMA_DIR = os.getenv("SCOUT_CHROMA_DIR", "./chroma_index")
PIPELINE_OUTPUT_CSV = os.path.join(DATA_DIR, "alerts_pipeline_output.csv")

# --- tunable defaults (dashboard sliders override these per-request) ---
DEFAULT_TEMPERATURE = float(os.getenv("SCOUT_TEMPERATURE", "0.3"))
DEFAULT_TOP_K = int(os.getenv("SCOUT_TOP_K", "2"))

# how many alerts the live (uncached) agent pipeline will process in one
# request before we make you wait -- protects the demo from a 200-alert
# LLM run happening live on stage
MAX_LIVE_PIPELINE_ALERTS = int(os.getenv("SCOUT_MAX_LIVE_ALERTS", "5"))

# heuristic used by the risk agent to turn "N production jobs affected"
# into an estimated dollar impact for the executive summary -- tune this
# per your problem statement's numbers, it's intentionally a single
# constant so it's easy to explain/justify in Q&A
AVG_JOB_VALUE_USD = float(os.getenv("SCOUT_AVG_JOB_VALUE_USD", "35000"))

# --- API server ---
ALLOWED_ORIGINS = os.getenv(
    "SCOUT_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://localhost:8080,http://127.0.0.1:5173"
).split(",")


if __name__ == "__main__":
    def _mask(key: str) -> str:
        return f"{key[:6]}...{key[-2:]}" if len(key) > 10 else "(short/empty)"

    print("SCOUT AI -- resolved provider configuration\n")
    print(f"  Chat provider:       {LLM_PROVIDER}")
    print(f"    gateway_url:       {GATEWAY_URL}")
    print(f"    model:             {CHAT_MODEL}")
    print(f"    api_key:           {_mask(API_KEY)}")
    print(f"    verify_ssl:        {VERIFY_SSL}")
    print(f"\n  Embedding provider:  {EMBEDDING_PROVIDER}")
    print(f"    gateway_url:       {EMBEDDING_GATEWAY_URL}")
    print(f"    model:             {EMBEDDING_MODEL}")
    print(f"    api_key:           {_mask(EMBEDDING_API_KEY)}")
    print(f"    verify_ssl:        {EMBEDDING_VERIFY_SSL}")
    print(f"\n  Available providers: {', '.join(PROVIDERS)}")
