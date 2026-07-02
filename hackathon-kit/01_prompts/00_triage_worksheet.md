# Triage worksheet — fill this in first, as a team, in the first 20 minutes

Don't write code until this is filled in. Every field here maps directly
into a template elsewhere in this kit.

## 0. Standing rules (non-negotiable — see STANDING_RULES.yaml)

Every build tonight follows these regardless of domain: dark theme only,
no generic/templated UI, a real context-aware AI chatbot on every
screen, persona-based login (not generic auth), real/real-time data
preferred over synthetic where feasible, and every AI-directed prompt
given in YAML. Don't re-decide these per problem — they're already
decided. Just fill in the domain-specific values below.

## 1. The core entity

What is the "thing" that gets detected/flagged/scored? (Tonight: an
`Alert`. Could be: a `Transaction`, `Ticket`, `Candidate`, `Anomaly`,
`Conflict` — whatever noun the problem statement centers on.)

**Entity name:** ______________________

**Its key fields** (the raw data it carries before AI touches it):
- ______________________
- ______________________
- ______________________

## 2. The five agent roles

Map the proven 5-role pattern onto this domain. You don't have to keep
these names, but keep the SEPARATION — five single-responsibility agents
beats one script, and it's what makes your Q&A story strong.

| Role (generic) | Tonight's version | Your version | What it does, one line |
|---|---|---|---|
| Detection | DetectionAgent (severity) | ______________________ | Classifies/scores the entity — usually rule-based, no LLM, fast |
| Impact/Risk | RiskAgent (graph traversal) | ______________________ | Computes downstream/business impact — often a graph or lookup, not LLM |
| Retrieval | RetrievalAgent (RAG) | ______________________ | Pulls relevant precedent/context from a knowledge base |
| Recommendation | RecommendationAgent (LLM) | ______________________ | The one LLM call — grounded in the two agents above |
| Escalation/Routing | EscalationAgent (rule) | ______________________ | Decides what happens next — auto-handle vs. human review |

If your problem genuinely doesn't need all 5, that's fine — but try to
keep at least 3 distinct agents with a real coordination story (one
agent's output feeding another) rather than a single "do everything"
LLM call. That distinction is what "multi-agent" actually means and
what a jury will probe.

## 3. Data sources

**Real data check first (timebox: 20-30 min max):**
- Does the problem statement provide a real dataset? ______________________
- Is there a free public API/open dataset for this domain? ______________________
- Decision: real data / synthetic — ______________________

What does `generate_data.py`'s equivalent need to produce, if synthetic?

- ______________________
- ______________________
- ______________________

What goes into the RAG knowledge base (the "historical precedent" your
RetrievalAgent searches)? Even 5-10 hand-written example records is
enough — that's all tonight's build used.

## 3a. User personas (for login screen — required, see standing rules)

Who actually uses this app? List every distinct role from the problem
statement:

| Persona | What they care about | Default view |
|---|---|---|
| ______________________ | ______________________ | ______________________ |
| ______________________ | ______________________ | ______________________ |

## 3b. Chatbot context questions

For each screen, what's ONE data point that should drive a dynamic
suggested question? (e.g. "highest-risk entity's name/severity")

| Screen | Data point to reference in suggested questions |
|---|---|
| ______________________ | ______________________ |
| ______________________ | ______________________ |

## 4. The API contract (do this NOW, before building)

List every screen/component you'll build, and for each one, the exact
JSON shape it needs. Write this as TypeScript interfaces (frontend) AND
pydantic models (backend) — they should be field-for-field identical.
See `02_architecture_templates/api/schemas_template.py` for the pattern.

| Screen/component | Fields it needs |
|---|---|
| Dashboard KPIs | ______________________ |
| Main list/table | ______________________ |
| Detail/drill-down | ______________________ |
| AI summary/explanation | ______________________ |
| Chat/copilot (if any) | ______________________ |

## 5. The "wow" moment

What's the ONE thing that should make the jury remember your demo
specifically? Pick this now, protect time for it later. (Tonight's was
"Explain reasoning" — a button that fires a live multi-agent run and
shows the agent trace, not a canned response.)

**Our wow moment:** ______________________

## 6. Team roles (fill in now, see 03_team_roles/)

| Person | Primary responsibility | Demo segment they present |
|---|---|---|
| ______________________ | ______________________ | ______________________ |
| ______________________ | ______________________ | ______________________ |
| ______________________ | ______________________ | ______________________ |
| ______________________ | ______________________ | ______________________ |
| ______________________ | ______________________ | ______________________ |
