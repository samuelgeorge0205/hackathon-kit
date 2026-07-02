"""
TEMPLATE -- AI assistant chatbot router. Required per standing rules:
every build needs a real, working chatbot grounded in the same
RAG/LLM stack as the main pipeline, with DYNAMICALLY generated
suggested questions based on current dashboard context -- not a
hardcoded static list.

Two endpoints:
  POST /api/copilot/chat                -- the actual chat
  GET  /api/copilot/suggested-questions -- context-aware question chips
"""
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from agents.retrieval_agent import get_vectordb  # TODO: fix import path
from agents.recommendation_agent import get_llm    # TODO: fix import path
from api import data_store  # TODO: fix import path
import config

router = APIRouter(prefix="/api/copilot", tags=["copilot"])


class CopilotMessage(BaseModel):
    role: str  # "user" | "ai"
    text: str
    sources: Optional[List[str]] = None
    confidence: Optional[int] = None


class CopilotChatRequest(BaseModel):
    message: str
    history: List[CopilotMessage] = []
    # optional: which screen/entity the user is currently looking at,
    # so the chat can be grounded in what's actually on their screen
    current_context_id: Optional[str] = None


class SuggestedQuestionsResponse(BaseModel):
    questions: List[str]


@router.post("/chat", response_model=CopilotMessage)
def chat(body: CopilotChatRequest):
    similar = get_vectordb().similarity_search(body.message, k=config.DEFAULT_TOP_K)
    sources = [f"Precedent {d.metadata.get('id', '?')}" for d in similar]
    context_text = "\n".join(f"- {d.page_content}" for d in similar)

    # TODO: pull whatever live dashboard state is relevant here, e.g.:
    # kpis = data_store.get_kpis()
    # current_entity = data_store.get_entity_by_id(body.current_context_id) if body.current_context_id else None

    history_text = "\n".join(f"{m.role}: {m.text}" for m in body.history[-6:])

    prompt = f"""You are an AI assistant embedded in a [YOUR DOMAIN] dashboard.
Answer conversationally and concisely (under 80 words), grounded in the
context below. If you can't answer from this context, say what you'd
need to check.

Relevant precedent:
{context_text or 'None found.'}

Recent conversation:
{history_text}

User question: {body.message}"""

    response = get_llm().invoke(prompt)
    return CopilotMessage(role="ai", text=response.content, sources=sources or ["Live data"], confidence=88)


@router.get("/suggested-questions", response_model=SuggestedQuestionsResponse)
def suggested_questions(context_id: Optional[str] = None):
    """Generates 3-4 suggested questions FROM live data, not a static
    list. Two ways to implement, pick based on time budget:

    FAST (rule-based, no LLM call, use this under time pressure):
        Build questions from a template string filled with real current
        data, e.g.:
            top_entity = data_store.get_highest_priority_entity()
            questions = [
                f"Why is {top_entity['name']} flagged as {top_entity['severity']}?",
                f"What happens if {top_entity['name']} isn't addressed?",
                "Summarize today's highest-priority items",
            ]

    RICHER (one LLM call, use if you have time budget):
        Pass a summary of current dashboard state to the LLM and ask it
        to generate 3-4 natural questions a user would plausibly ask
        about THIS specific data right now.
    """
    # TODO: implement one of the two approaches above
    top_entity = data_store.get_highest_priority_entity() if context_id is None else data_store.get_entity_by_id(context_id)
    if not top_entity:
        return SuggestedQuestionsResponse(questions=["What's the current status?"])

    questions = [
        f"Why is {top_entity.get('name', top_entity.get('id'))} flagged as {top_entity.get('severity', 'high priority')}?",
        f"What's the recommended action for {top_entity.get('name', top_entity.get('id'))}?",
        "Summarize today's highest-priority items",
        "What changed since yesterday?",
    ]
    return SuggestedQuestionsResponse(questions=questions)
