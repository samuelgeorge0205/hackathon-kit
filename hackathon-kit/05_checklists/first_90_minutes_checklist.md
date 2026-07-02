# First 90 minutes — do this in order, don't skip ahead

This is the highest-risk window: enthusiasm is high, discipline is low,
and most hackathon teams lose their edge here by either over-planning or
diving into code with no shared contract.

## 0:00–0:20 — Triage (see 01_prompts/00_triage_worksheet.md)

- [ ] Everyone reads the problem statement together, out loud, once
- [ ] Fill in the entity, the 5 agent roles, and data sources as a group
      (5 minutes of disagreement now saves an hour of rework later)
- [ ] Pick the "wow" moment NOW — don't leave it for later, it shapes
      what you prioritize

## 0:20–0:50 — Lock the contract

- [ ] Write the API schema (backend pydantic + frontend TypeScript)
      TOGETHER, in the same conversation, at the same time
- [ ] Once locked, backend and frontend people physically split up and
      stop blocking on each other
- [ ] Put the locked contract somewhere everyone can see it (shared doc,
      pinned message) — this is your single source of truth for the
      next 4 hours

## 0:50 onward — Build, but check in

- [ ] Backend: data generation script running and producing real CSVs
      before 1:30 — if it's not, you're behind, cut scope now not later
- [ ] Frontend: at least 2 screens visually complete (on mock data)
      before 1:30
- [ ] **Hard checkpoint at 2:30**: wire ONE real screen end-to-end. If
      this doesn't work by 2:30, STOP adding new screens/agents and fix
      the wiring — an impressive-looking disconnected frontend and a
      correct disconnected backend is a worse demo than a plain
      end-to-end working loop

## Signs you're off track (fix immediately, don't push through)

- Nobody can currently explain what the "wow" moment will be → decide now
- Backend and frontend haven't looked at the same schema doc in an hour
  → resync
- More than 2 people are debugging the same environment issue → one
  person keeps debugging, everyone else keeps building on what works
- You're 90 minutes in and still discussing architecture → force a
  decision, you can revisit if there's time later (there won't be)
