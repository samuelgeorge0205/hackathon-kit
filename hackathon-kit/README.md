# Hackathon Kit — for tomorrow's (unknown) problem statement

Built from tonight's proven end-to-end session (synthetic data →
multi-agent pipeline → FastAPI → React dashboard, verified working with
real Ollama calls). Everything here is domain-agnostic — fill in the
brackets once you know the problem.

## Start here

1. **Read `00_MASTER_PLAYBOOK.md` first** — the 5-hour timeline and the
   single most important practice (locking the API contract before
   building).
2. **Fill in `01_prompts/00_triage_worksheet.md`** as a team, first 20
   minutes, before anyone writes code.
3. **Feed `01_prompts/backend_generation_prompt.md`** and
   **`01_prompts/frontend_lovable_prompt.md`** (filled in from the
   worksheet) to your AI tools to scaffold both sides fast.
4. **Copy from `02_architecture_templates/`** for the proven code
   patterns — `config.py` and `ssl_patch.py` are reusable as-is.
5. **Assign roles now** using `03_team_roles/role_scripts.md`.
6. **When you're building the deck/demo**, `04_presentation/` has the
   slide skeleton, demo script template, and tech Q&A cheat sheet.
7. **Keep `05_checklists/troubleshooting_cheatsheet.md` open in a tab**
   — it has the exact bugs (PATH issues, missing `data/` dir, Ollama
   embedding format) we already hit and fixed tonight.

## The one-sentence version of the whole strategy

Lock the contract, build in parallel, wire early, protect time for one
genuine "wow" moment, and rehearse the demo more than you build features.
