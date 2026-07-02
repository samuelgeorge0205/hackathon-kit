# Spec-driven templates (Spec Kit style)

These work two ways: literally with GitHub's Spec Kit CLI
(`/constitution`, `/specify`, `/plan`, `/tasks`, `/implement` slash
commands in Claude Code or a compatible agent), OR as plain structured
prompts you paste into any chat-based Claude session if Spec Kit itself
isn't installed on the contest machine. Same value either way — the
structure is what matters, not the tool.

**Note:** Spec Kit is a fast-moving project — if you do have it
installed, check `github.com/github/spec-kit` for current exact syntax
before relying on the command names below; treat this as the shape of
the workflow, not a guaranteed-current CLI reference.

---

## /constitution — paste this first, once, at the start of the build

```
This project has the following non-negotiable principles:

1. Every LLM/embedding client reads its provider, model, and key from a
   single config module -- never hardcoded inline. Switching providers
   must be a one-line env var change.
2. The system is multi-agent, not a single script calling an LLM once.
   At minimum: a detection/classification step (rule-based), a
   retrieval step (RAG grounding), a generation step (the LLM call,
   grounded in the retrieval step), and a routing/escalation step
   (rule-based decision on what happens next). Each is a separate,
   single-responsibility module.
3. The API layer's response schemas must exactly match the frontend's
   TypeScript types, field-for-field -- this is fixed before either side
   is built in depth.
4. Every script that writes to a data/ or output directory creates that
   directory if it doesn't exist -- never assumes it's already there.
5. Code should be modular and self-explanatory: docstrings on every
   module explaining its single responsibility, meaningful names, no
   god-files. A judge should understand any file in under a minute.
6. We build our own core logic. AI assistance is for scaffolding and
   speed, not for replacing our understanding of what the system does --
   every team member must be able to explain any part of it.
```

## /specify — paste this, filled in from your triage worksheet

```
Build a [ONE-LINE PROBLEM DOMAIN] system with the following components:

WHAT (not how):
- Detects/flags [ENTITY] based on [SIGNALS FROM TRIAGE WORKSHEET]
- Assesses downstream impact of each flagged [ENTITY]
- Retrieves relevant historical precedent to ground its recommendations
- Generates a plain-language recommendation for each flagged [ENTITY]
- Routes high-severity/low-confidence cases to human review, auto-logs
  the rest
- Exposes all of the above via a REST API
- Is displayed in a live dashboard showing: [LIST SCREENS FROM TRIAGE
  WORKSHEET]

WHY:
[PASTE PROBLEM STATEMENT'S "why this matters" framing]

SUCCESS CRITERIA:
- End-to-end demo: raw data in, flagged/scored/recommended output out,
  visible in the dashboard
- At least 3 distinct agents with a real coordination story (one
  agent's output feeding another)
- Every screen shows real computed data, with a documented fallback if
  the API is unreachable
```

## /plan — paste this after /specify

```
Tech stack:
- Backend: Python, FastAPI, LangGraph for agent orchestration,
  LangChain for LLM/embedding clients, Chroma for the vector store,
  pandas for data handling
- Frontend: React + TypeScript (Vite), React Query for data fetching,
  [Tailwind/shadcn or whatever your team already knows]
- LLM: [contest gateway / Ollama / Groq -- pick based on what's
  actually available tomorrow]

Architecture: reuse the proven 5-file agent pattern (state.py +
detection/risk/retrieval/recommendation/escalation agents +
orchestrator.py) and the config.py provider-switching pattern from our
reference build -- see 02_architecture_templates/ for the exact files
to adapt.

Non-goals for this build: authentication, multi-tenancy, production
deployment, handling data volumes beyond what a hackathon demo needs.
```

## /tasks — let the agent generate this, but sanity-check it against

```
Does the task breakdown:
- Put agents/state.py first (the data contract everything depends on)?
- Separate backend tasks from frontend tasks so they can run in parallel?
- Include a task for locking the API contract BEFORE deep backend/
  frontend work starts?
- Include an early "wire one screen end-to-end" task before "build all
  screens" -- proving the full loop works before investing in breadth?
- Leave polish/extra screens as the LAST tasks, not interspersed --
  so a time crunch cuts scope from the end, not randomly?
```

## /implement — standard, but with this reminder each time

```
Before implementing, restate in one line what this specific file's
single responsibility is. If you can't state it in one line, it's
probably doing too much -- split it.
```
