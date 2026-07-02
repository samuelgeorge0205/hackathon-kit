# Differentiation ideas — pick 1-2, don't try all of these

Most teams at any hackathon build "a dashboard that shows AI output."
These are ways to stand out without adding much build time, roughly
ordered by effort-to-impact ratio.

## Low effort, real impact

- **"Explain reasoning" / agent trace visibility** — showing the actual
  multi-agent trace live (which agent ran, what it found) rather than
  just a final answer. This alone is often the single most memorable
  moment in a demo — it makes "multi-agent" tangible instead of a claim.
- **A visible confidence score + "why"** — not just "94% confidence" but
  a one-line reason (grounded in N precedent records, or bounded by X
  uncertainty). Shows the system knows its own limits.
- **A live toggle between "before AI" and "after AI"** — e.g. show the
  raw data table first (what an ops person sees today), then the AI
  layer on top. Makes the value-add visually obvious instead of assumed.
- **Real numbers in the exec summary, not vague language** — "$X impact,
  Y hours, Z affected" reads as more credible than "significant risk
  detected."

## Medium effort, strong differentiation

- **A what-if / simulator screen** — letting the jury themselves trigger
  a scenario live ("what if supplier X goes down") is interactive in a
  way a static dashboard isn't, and judges remember things they touched.
- **Escalation/routing as a visible decision, not just a badge** — show
  the actual rule that triggered escalation, framed as a safety feature
  ("we don't let the AI auto-decide high-stakes cases").
- **A "what we'd build next" slide that's genuinely specific** — instead
  of vague roadmap talk, show one concrete next screen following the
  exact same wiring pattern already proven, signaling engineering
  maturity, not just enthusiasm.

## Higher effort, only if you have real time left

- **A second, smaller AI capability using a DIFFERENT technique** than
  your main pipeline (e.g. main pipeline is RAG + LLM, but you also add
  a simple anomaly-detection stat model) — shows range, but only do this
  if your core loop is already rock solid; don't split focus early.
- **Voice or natural-language query** into your data ("ask anything"
  chat, if you don't already have one) — high wow factor, but only
  worth it if your RAG grounding is already solid, since a bad chat
  answer live is worse than not having chat at all.

## What NOT to do for differentiation

- Don't add a feature you can't reliably demo twice in rehearsal — an
  impressive feature that fails live costs more than it gains
- Don't add visual flourishes (animations, extra pages) that don't
  connect to the actual AI/technical story — judges score
  creativity/innovation, not aesthetics alone
- Don't try to hide that you used AI tools (Lovable, Claude, etc.) to
  build faster — own it, and pivot to what YOU built on top (the logic,
  the grounding, the safety decisions)
