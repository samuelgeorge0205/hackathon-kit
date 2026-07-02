"""
TEMPLATE -- pydantic response models. Keep these field-for-field
identical to your frontend's TypeScript interfaces (mock-data.ts). This
is the contract you locked in the triage worksheet -- write both sides
from the SAME list at the same time.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    # TODO: match your triage worksheet's fields exactly, e.g.:
    # severity: Literal["critical", "warning", "info"]
    # status: Literal["active", "acknowledged", "resolved"]
    # ...


class KPIs(BaseModel):
    pass  # TODO


class ExecutiveSummary(BaseModel):
    text: str
    confidence: int
    generatedAt: str
    highlightedEntityId: Optional[str] = None


class Recommendation(BaseModel):
    id: str
    title: str
    reasoning: str
    confidence: int
    category: str


class ExplainResponse(BaseModel):
    """Powers a live "explain reasoning" drill-down -- re-runs the
    entity through the live pipeline and returns each agent's output."""
    id: str
    severity: str
    retrievedContext: str
    downstreamImpact: List[str]
    estimatedCostImpact: float
    recommendation: str
    needsEscalation: bool
    agentTrace: List[str]
