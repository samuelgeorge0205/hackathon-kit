# Troubleshooting cheat sheet — real bugs we already hit, pre-armed

Every one of these actually happened during tonight's setup. If you're
on a similar stack tomorrow (Python/uv, FastAPI, LangChain, Ollama), you
WILL hit some of these again — recognize them instantly instead of
losing 20 minutes rediscovering the fix.

## `uv: command not recognized` right after installing

**Cause:** the installer updates PATH, but any terminal window already
open doesn't see the change — it loaded its environment before the
install happened.

**Fix:** close the terminal window ENTIRELY (not just clear it) and open
a genuinely new one. If it's still broken after that, your permanent
user PATH didn't actually get updated — check with:
```powershell
[Environment]::GetEnvironmentVariable("Path", "User") -split ';' | Select-String 'uv|\.local\\bin'
```
If empty, add it manually, then open a fresh terminal again. As an
immediate unblock without fixing PATH: call the full exe path directly,
or `Set-Alias uv "C:\Users\<you>\.local\bin\uv.exe"` for the session.

## `uv pip install` demands a virtual environment

**Cause:** unlike plain `pip`, `uv pip install` won't silently install
into a system Python — it wants an explicit venv target.

**Fix:**
```powershell
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
```

## `OSError: Cannot save file into a non-existent directory: 'data'`

**Cause:** any script writing to `data/some_file.csv` assumes that
folder already exists — it doesn't create it.

**Fix, immediate:** `mkdir data` before running.
**Fix, permanent:** add `os.makedirs("data", exist_ok=True)` near the
top of every script that writes there. Do this preemptively tomorrow in
every generated script — don't wait to hit the error.

## `openai.BadRequestError: 400 - invalid input type` when embedding against Ollama

**Cause:** `langchain_openai`'s `OpenAIEmbeddings` pre-tokenizes text
into integer token arrays before sending the request by default (fine
for real OpenAI, which accepts that format). Ollama's OpenAI-compatible
`/v1/embeddings` endpoint only accepts raw text strings and rejects the
token-array format with this exact error.

**Fix:** pass `check_embedding_ctx_length=False` to every
`OpenAIEmbeddings(...)` call when the embedding provider is Ollama (or
any local OpenAI-compatible endpoint). This is baked into the templates
in `02_architecture_templates/` already — if you regenerate this code
with an AI tool tomorrow, explicitly tell it to include this flag, since
it's not something the model will know to add unprompted.

## `Failed to send telemetry event ... capture() takes 1 positional argument but 3 were given`

**Cause:** a version mismatch between `chromadb` and `posthog` (its
telemetry library). Cosmetic only — doesn't affect functionality.

**Fix:** ignore it. If it bothers you: `$env:ANONYMIZED_TELEMETRY="False"`
before running, or just don't worry about it during a hackathon.

## `LangChainDeprecationWarning: The class Chroma was deprecated`

**Cause:** `langchain_community.vectorstores.Chroma` is being replaced by
a separate `langchain-chroma` package.

**Fix:** ignore it for hackathon purposes — it's a warning, not an
error, and migrating packages mid-build isn't worth the time. Only fix
if you have genuinely spare time at the very end.

## Frontend shows the exact original placeholder/mock text

**Cause:** the API call failed silently and the UI fell back to mock
data (if you built the fallback pattern — see the architecture
templates). This is a FEATURE working correctly, not a new bug — but it
means something upstream IS broken.

**Diagnosis:** open browser dev tools (F12) → Network tab → filter `api`
→ look for non-200 responses or CORS errors in the Console tab.

**Common causes:** backend not running, wrong port in `VITE_API_URL`,
or the frontend's actual dev port isn't in the backend's CORS allowlist
— **check `vite.config.ts` for the real port**, don't assume it's 5173
(ours was 8080).

## General debugging discipline under time pressure

- **Read the actual traceback's last few lines first** — the real error
  is almost always at the bottom, not the top (which just shows the
  call chain getting there).
- **One person debugs, don't crowd** — everyone else keeps building on
  what's already working.
- **If stuck more than 10 minutes on an environment issue**, consider
  whether there's a workaround that unblocks progress even if it's not
  the "proper" fix (e.g. calling a full exe path instead of fixing PATH)
  — fix it properly later if there's time, don't let it block the team.
