# Lovable frontend prompt (contract-first version)

> **Superseded by `frontend_lovable_prompt.yaml`** — use that one, it
> also has the dark-theme, originality, chatbot, and persona-login
> standing rules baked in. This file is kept only as prose reference.

Fill in every [BRACKET] from your `00_triage_worksheet.md`, especially
section 4 (the API contract) — paste it in verbatim where marked. This
is what lets your frontend be built in PARALLEL with the backend instead
of waiting for it.

---

## 1. Project overview

Build the frontend for **[PRODUCT NAME]** — [ONE-SENTENCE DESCRIPTION].

This is a hackathon prototype judged on working functionality, creativity,
and clarity in a live 2-minute demo. It must look polished and
production-grade — this is a real differentiator against other teams
using generic templates.

**Target user:** [WHO USES THIS]
**Core problem it solves:** [1-2 SENTENCES]

## 2. Tech constraints

- Build as **React + TypeScript (Vite)**.
- A backend team is building a REST API in parallel — **do not invent
  backend logic or fake AI reasoning**. Build against the exact mock
  data shapes below, structured so swapping mock data for a real fetch
  call later is a 3-line change per component (see "wiring pattern" note
  at the end).
- Use `@tanstack/react-query` for data fetching (set up a `queryClient`
  at the app root now, even though everything's mocked initially — this
  is the thing that made wiring fast last time).
- Desktop-first, not mobile-first — this will be demoed on a laptop
  screen.

## 3. The data contract (build EXACTLY to this shape)

```typescript
// Paste your triage worksheet's section 4 here as real TypeScript
// interfaces, e.g.:

export interface [Entity] {
  id: string;
  [field]: [type];
  // ...
}

export interface KPIs {
  [field]: [type];
}

export interface ExecutiveSummary {
  text: string;
  confidence: number;
  generatedAt: string;
}
```

Put these in `src/lib/mock-data.ts` alongside generated mock data arrays
matching the shapes exactly — this file becomes the fallback data source
later, not just placeholder data to delete.

## 4. Screens needed

[LIST FROM TRIAGE WORKSHEET SECTION 4 — ONE PER ROW]

1. **[Screen name]** — [primary action], [key data shown]
2. **[Screen name]** — [primary action], [key data shown]
3. **[Screen name]** — [primary action], [key data shown]

For each: loading state, empty state, error state that fails gracefully.

## 5. The "wow" moment

**[PASTE FROM TRIAGE WORKSHEET SECTION 5]**

Design the UI to make this moment visually clear — this is the thing a
judge should remember. Don't bury it in a generic layout.

## 6. Visual style

- **Vibe:** [pick one — clean SaaS dashboard / dark developer tool /
  friendly consumer app — don't leave generic]
- **Color direction:** something that reads as intentional, not a
  default AI-template gradient
- **Avoid:** generic centered-hero-plus-3-cards layout, Lorem Ipsum
  visible anywhere in the final build, stock AI-startup purple gradients

## 7. What NOT to build

- No auth/login flow unless explicitly required
- No settings/admin screens beyond what's needed for the demo
- Don't over-engineer pagination/filtering for data volumes you don't
  have — a hackathon dataset is small

## 8. Wiring pattern (for later — mention this so Lovable's code is ready)

Structure each screen's data access as a single hook call at the top of
the component (e.g. `const { data } = useAlerts()`), not scattered
`mock-data` imports throughout the JSX. Later, `useAlerts()` becomes a
real `fetch()` wrapped in React Query with a fallback to the same mock
array — and because every component only touches data through that one
hook call, wiring the whole app is a mechanical, low-risk change instead
of a rewrite.

## First response should include

1. Confirmation of the page structure and component plan
2. The scaffolded app with mock data wired in, fully clickable end-to-end
3. Clear comments marking exactly where each screen's data hook lives,
   ready to be swapped for a real API call
