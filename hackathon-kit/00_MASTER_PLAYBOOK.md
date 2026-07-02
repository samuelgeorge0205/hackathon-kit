# The 5-Hour Playbook — index & battle plan

You don't know tomorrow's problem statement yet. This kit is built so the
first 30 minutes after you receive it are triage and typing into
templates, not architecture debates.

## What's in this kit

```
01_prompts/            Prompt skeletons -- feed these to Claude/your AI
                        agent, filled in with tomorrow's specifics, and
                        get a working scaffold in minutes instead of hours
02_architecture_templates/  Copy-paste-and-rename code skeletons (state,
                        agents, API) matching the proven pattern from
                        tonight's build
03_team_roles/          Who does what, and what each person can say if
                        asked to explain their piece
04_presentation/         Slide skeleton, demo script template, Q&A prep
05_checklists/           First-90-minutes checklist, differentiation
                        ideas, and the exact bugs we hit tonight
                        (pre-armed so you don't lose time to them again)
```

## The core insight this whole kit is built on

Most "detect something → explain it → recommend an action" problems —
which covers a huge fraction of hackathon problem statements (fraud,
IT incidents, churn, quality defects, supply chain, scheduling
conflicts, anomaly detection of any kind) — reduce to the same shape:

```
raw/synthetic data → detect/classify → retrieve context (RAG) →
generate recommendation → route/decide → expose via API → dashboard
```

Tonight's supply-chain build proved this shape works end-to-end. Tomorrow
you're not starting from zero — you're reskinning a proven skeleton.

## The 5-hour timeline

| Time | Block | What happens |
|---|---|---|
| 0:00–0:20 | **Triage** | Read the problem statement together. Fill in `01_prompts/00_triage_worksheet.md`. Agree on the core entity, the 5 agent roles, and the API contract (this is the single most important artifact — see below). |
| 0:20–0:50 | **Contract lock** | Write `api/schemas.py` (backend) AND the matching TypeScript types (frontend) TOGETHER, before either side is built. This is what lets backend and frontend build in parallel instead of sequentially — the #1 speed lever in this whole kit. |
| 0:50–2:30 | **Parallel build** | Backend person(s): data generation → agents → FastAPI, using `02_architecture_templates/`. Frontend person(s): Lovable prompt from `01_prompts/frontend_lovable_prompt.md`, built against the AGREED schema, using mock data matching it exactly — so wiring later is a 3-line swap, not a rewrite. |
| 2:30–3:00 | **First integration checkpoint** | Wire ONE screen to the real API. Prove the loop works end-to-end before building more screens. This is the checkpoint tonight's session validated is worth doing early. |
| 3:00–4:00 | **Finish wiring + polish the "wow" moment** | Wire remaining screens using the proven pattern. Protect explicit time for the ONE feature that should make the jury remember you (see `05_checklists/differentiation_ideas.md`). |
| 4:00–4:30 | **Freeze + rehearse** | Stop building new things. Run the demo script twice, timed. Fix only what's broken, don't add anything. |
| 4:30–5:00 | **Presentation prep** | `04_presentation/` — slides, per-person talking points, Q&A. |

## The single highest-leverage practice

**Lock the API contract before building either side.** Tonight's build
worked because the schema (`api/schemas.py`) was written to match the
frontend's types field-for-field — meaning frontend and backend were
built independently and wiring was a 3-line change per component, not
an integration project. Do this FIRST tomorrow, even before writing any
real logic. See `01_prompts/00_triage_worksheet.md`.
