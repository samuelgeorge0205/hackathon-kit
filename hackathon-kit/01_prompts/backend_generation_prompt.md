# Backend generation prompt

> **Superseded by `backend_generation_prompt.yaml`** — use that one.
> This file is kept only as prose reference for the reasoning behind
> each requirement. Per standing rule, all AI-directed prompts are now
> given in YAML.

Fill in every [BRACKET] from your completed `00_triage_worksheet.md`, then
paste this whole thing to Claude (chat, Claude Code, or via Spec Kit's
`/specify` + `/plan` if available on your machine — see
`spec_kit_specify_template.md` for that flow instead).

---

## Context

I'm building a backend for a hackathon problem: **[ONE-SENTENCE PROBLEM STATEMENT]**.

I have a proven architecture pattern from a previous build (attaching/
describing it below) and want you to adapt it to this new domain — reuse
the SHAPE, replace the domain logic.

## Required architecture (reuse this shape exactly)

```
config.py               -- centralized provider config (see reference below,
                            reuse almost verbatim, it's domain-agnostic)
ssl_patch.py             -- reuse verbatim, domain-agnostic
generate_data.py         -- synthetic data generator for [ENTITY NAME],
                            seeded random, writes CSVs/JSON to data/
detect_[X].py             -- rule-based detection/classification, no LLM,
                            explainable by construction
build_knowledge_base.py  -- embeds [N] example precedent records into Chroma

agents/
  state.py                -- shared TypedDict state, fields:
                             [LIST FIELDS FROM TRIAGE WORKSHEET]
  detection_agent.py       -- [WHAT IT CLASSIFIES], rule-based, no LLM
  risk_agent.py             -- [WHAT IMPACT IT COMPUTES], graph/lookup, no LLM
  retrieval_agent.py        -- RAG lookup from the knowledge base above
  recommendation_agent.py   -- the ONE LLM call, grounded in risk + retrieval
  escalation_agent.py       -- rule-based routing: auto-handle vs. escalate
  orchestrator.py           -- LangGraph StateGraph wiring all 5 in sequence,
                             with a real conditional edge at the escalation step

api/
  main.py                  -- FastAPI app, CORS, router registration
  schemas.py                -- pydantic models, MUST match the frontend's
                             TypeScript types field-for-field (see the API
                             contract from the triage worksheet)
  data_store.py              -- loads CSVs, maps to schemas.py shapes,
                             in-memory state for anything mutable (status
                             updates etc.)
  routers/
    [one per screen from the API contract]
```

## Critical constraints (don't skip these — they're bugs we already hit)

1. **Every LLM/embedding client must read from `config.py`**, never
   hardcode a gateway URL, model name, or API key anywhere else. This is
   what makes provider-switching (contest gateway vs. Ollama vs. Groq
   vs. OpenAI) a one-line `.env` change instead of a code change.
2. **If using `langchain_openai.OpenAIEmbeddings` against an
   OpenAI-compatible LOCAL endpoint (Ollama, LM Studio, etc.)**, you
   MUST pass `check_embedding_ctx_length=False` — otherwise it
   pre-tokenizes into integer arrays that Ollama's endpoint rejects with
   a confusing `400 invalid input type` error. This cost real time
   tonight; don't rediscover it tomorrow.
3. **`os.makedirs("data", exist_ok=True)` at the top of any script that
   writes to `data/`** — don't assume the folder exists on a fresh
   checkout.
4. **Every pydantic response model in `schemas.py` must exactly match** a
   TypeScript interface on the frontend, field-for-field, including
   casing (camelCase on both sides, since that's what the frontend
   expects). This is what makes wiring a component later a 3-line
   change: swap the import, call the hook, done.
5. **CORS**: `SCOUT_ALLOWED_ORIGINS`-equivalent must include whatever
   port your frontend dev server actually uses — check `vite.config.ts`,
   don't assume 5173 (ours was 8080).
6. **Don't call the LLM in a loop without a limit for anything
   user-triggered from the UI** — cap live/on-demand agent runs (e.g.
   "explain reasoning" for ONE item, not a full re-run of everything) so
   a button click can't accidentally trigger a multi-minute wait during
   a demo.

## Reference: config.py pattern to reuse near-verbatim

[PASTE YOUR config.py FROM THE PREVIOUS BUILD HERE, OR SAY "same as
before, provider registry for contest/ollama/groq/openai with
SCOUT_LLM_PROVIDER switching"]

## What I need from you right now

1. Confirm you understand the 5-agent split for THIS domain (restate it
   back to me in one line per agent)
2. Generate `agents/state.py` first — this is the data contract everything
   else depends on
3. Then generate the rest in this order: `generate_data.py` →
   `detect_[X].py` → the 5 agent files → `orchestrator.py` → `schemas.py`
   → `api/main.py` + routers
4. After each file, tell me the exact command to run it and what output
   I should expect to see — I'll run it and confirm before we move to
   the next file (this catches bugs one at a time instead of all at once
   at the end)
