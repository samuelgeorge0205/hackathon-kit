# Team roles & demo scripts

Fill in names against these roles as soon as you've triaged the problem
(section 6 of the worksheet). Each role has: what you build, and what
you say if the jury asks YOU specifically to explain your piece.

---

## Role 1: Data & Detection

**Build:** `generate_data.py`, `detect_[X].py`, the raw dataset.

**If asked "how realistic is your data":** "It's synthetic but seeded
and structured to mirror real [DOMAIN] patterns — [N] records, generated
with [describe the realistic constraint you built in, e.g. 'each
supplier specializes in 1-2 item types so the dependency graph shows
real clusters instead of a fully-connected mess']. We used synthetic
data because [reason from problem statement — privacy, no real dataset
available, etc.], which the problem statement explicitly allows."

**If asked "why rule-based detection, not ML/LLM":** "Detection needs to
be fast and explainable — a jury or ops team can read the exact
if-statement that flagged something. We save the LLM for the part that
actually benefits from language generation: the recommendation."

## Role 2: Multi-agent pipeline

**Build:** `agents/*.py`, `orchestrator.py`.

**If asked "why multi-agent, not one LLM call":** "Each agent has one
job and can be tested or swapped independently — [RiskAgent] doesn't
touch the LLM at all, it's a graph traversal, so we can change that
logic without touching the prompt in [RecommendationAgent]. And
[RiskAgent]'s output feeds into [RecommendationAgent] — that's real
coordination between agents, not just a renamed function."

**If asked "how do you know the recommendation isn't hallucinated":**
"[RetrievalAgent] pulls grounding context from real historical
precedent *before* [RecommendationAgent] ever runs — the LLM is
generating language, not inventing facts from nothing."

**If asked "what if the AI is wrong":** "[EscalationAgent] is a
deliberate safety valve — high-severity or low-confidence cases route
to a human instead of auto-trusting the LLM. That's not a limitation,
it's a design decision."

## Role 3: Backend API

**Build:** `api/main.py`, `schemas.py`, `data_store.py`, routers.

**If asked "how does the frontend get this data":** "REST API, FastAPI —
[N] endpoints, one per screen. The schemas are written to match the
frontend's TypeScript types field-for-field, so there's zero translation
layer needed on either side."

**If asked about scale/production-readiness:** "This is a prototype —
in-memory/CSV-backed for the demo. The one thing we did think about for
real use: [mention config.py's provider-switching, or the escalation
safety valve, or whatever's genuinely production-minded in your build]."

## Role 4: Frontend

**Build:** Lovable-generated UI, wiring (`api.ts`, `queries.ts`, hooks).

**If asked "did AI build your whole frontend":** "We used Lovable to
scaffold the UI quickly, but the data layer — how it talks to our real
backend, the fallback behavior, the wiring — is our own code, and any
of us can walk through it." (Say this confidently — it's true and it's
the correct, honest answer per your event's rules.)

**If asked about the fallback behavior:** "If the API's unreachable, the
UI falls back to realistic placeholder data instead of breaking — a
deliberate resilience choice for a live demo, not an accident."

## Role 5: Demo & Q&A lead

**Build:** the demo script (see `demo_script_template.md`), rehearses
the click path, fields questions the other four can't answer live.

**Job during the demo:** narrate the "why" while a teammate drives the
keyboard, or drive it yourself if your team prefers one presenter for
the live-demo segment specifically (see your event's suggested flow —
one presenter per SEGMENT, not necessarily per feature).

---

## General Q&A prep — questions likely for ANY team, have an answer ready

- "What's your accuracy / how do you know it works?" → have ONE number
  ready (detection accuracy against your synthetic ground truth, or
  recommendation acceptance rate if you tracked it)
- "What would you build next with more time?" → 2-3 concrete items, not
  vague ("wire the remaining screens using the same pattern," "add a
  second data source," etc.)
- "Why this tech stack?" → one sentence per major piece, see
  `tech_stack_cheat_sheet.md`
