"""
TEMPLATE -- persona/login router. Required per standing rules: login
should be specific to who actually uses this app, not generic
email+password. No real auth needed for a demo -- persona selection
determining view/data scope is enough.
"""
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/personas", tags=["personas"])


class Persona(BaseModel):
    id: str
    name: str            # e.g. "Operations Manager"
    description: str     # one line on what they care about / see
    default_view: str    # which screen/route they land on


# TODO: define the REAL personas for your domain, from the problem
# statement -- don't leave these generic. Example shape:
PERSONAS: List[Persona] = [
    Persona(id="ops_manager", name="Operations Manager",
            description="Sees all alerts across every plant/region, focuses on escalations",
            default_view="/dashboard"),
    Persona(id="analyst", name="Domain Analyst",
            description="Deep-dives into individual cases, uses the explain-reasoning feature most",
            default_view="/alerts"),
]


@router.get("", response_model=List[Persona])
def list_personas():
    return PERSONAS


@router.get("/{persona_id}", response_model=Optional[Persona])
def get_persona(persona_id: str):
    return next((p for p in PERSONAS if p.id == persona_id), None)
