"""
TEMPLATE -- rename [Entity] and fields to match your actual problem
domain. This is the data contract every agent reads and writes to --
get this right first, everything else follows from it.

Shared state that flows through the multi-agent pipeline. Every agent
reads this TypedDict and returns an updated copy.
"""
from typing import TypedDict, List, Optional


class EntityState(TypedDict):  # TODO: rename to your domain, e.g. AlertState, TicketState
    # --- input: raw signals your detection step already has ---
    entity_id: str            # TODO: rename, e.g. po_id, ticket_id, transaction_id
    # TODO: add your raw input fields here, e.g.:
    # item: str
    # delay_days: int
    # reasons: List[str]

    # --- filled in by the Detection agent ---
    severity: Optional[str]                # e.g. "low" | "medium" | "high"

    # --- filled in by the Risk/Impact agent ---
    downstream_impact: Optional[List[str]]     # what's affected
    estimated_cost_impact: Optional[float]     # $ estimate, or your domain's equivalent metric

    # --- filled in by the Retrieval agent ---
    retrieved_context: Optional[str]           # RAG-retrieved precedent

    # --- filled in by the Recommendation agent ---
    recommendation: Optional[str]              # plain-language recommendation text
    recommendation_category: Optional[str]     # bucket/tag for the recommendation

    # --- filled in by the Escalation agent ---
    needs_escalation: Optional[bool]

    # --- tunable knobs (surface as dashboard sliders if useful) ---
    temperature: Optional[float]
    top_k: Optional[int]


def new_state(entity_id: str, /, **kwargs) -> EntityState:
    """Factory for a clean starting state -- avoids every caller having
    to remember every field name by hand."""
    base: EntityState = {
        "entity_id": entity_id,
        "severity": None,
        "downstream_impact": None, "estimated_cost_impact": None,
        "retrieved_context": None,
        "recommendation": None, "recommendation_category": None,
        "needs_escalation": None,
        "temperature": None, "top_k": None,
    }
    base.update(kwargs)
    return base
