"""
Shared SSL monkeypatch for the hackathon lab's corporate network, where the
proxy breaks normal certificate verification for tiktoken/requests/httpx
background calls.

This is now gated by config.VERIFY_SSL (see config.py / .env):
  - SCOUT_VERIFY_SSL=false (default, matches the contest lab) -> patch applies,
    same behavior as before.
  - SCOUT_VERIFY_SSL=true (recommended on a personal laptop hitting real
    internet APIs -- Ollama, Groq, OpenAI, etc.) -> this function is a no-op.
    Disabling certificate verification against a real public API is an
    unnecessary security hole once you're off the corporate proxy that
    actually needed it.

Import and call this FIRST, before any other imports, in every script:

    from ssl_patch import apply_ssl_monkeypatch
    apply_ssl_monkeypatch()
"""

import ssl


def apply_ssl_monkeypatch():
    import config
    # Skip only if NEITHER the chat provider nor the embedding provider
    # needs verification bypassed -- e.g. contest gateway (VERIFY_SSL=False)
    # + Ollama embeddings (EMBEDDING_VERIFY_SSL=True) should still patch,
    # since the contest gateway leg needs it.
    if config.VERIFY_SSL and config.EMBEDDING_VERIFY_SSL:
        return  # neither provider is behind a proxy that breaks cert checks

    # 1. Default SSL context (covers urllib-based calls)
    ssl._create_default_https_context = ssl._create_unverified_context

    # 2. httpx.Client -- force verify=False even for clients constructed deep inside libraries
    import httpx
    _orig_httpx_init = httpx.Client.__init__
    def _patched_httpx_init(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_httpx_init(self, *args, **kwargs)
    httpx.Client.__init__ = _patched_httpx_init

    # 3. requests -- tiktoken and some other libraries use requests, not httpx
    try:
        import requests
        _orig_get = requests.get
        _orig_post = requests.post
        requests.get = lambda *a, **kw: _orig_get(*a, **{**kw, "verify": False})
        requests.post = lambda *a, **kw: _orig_post(*a, **{**kw, "verify": False})
    except ImportError:
        pass

    # Silence the resulting "InsecureRequestWarning" noise
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except ImportError:
        pass