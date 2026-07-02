"""
TEMPLATE -- DetectionAgent

Single responsibility: turn raw signals into a severity/priority
classification. Keep this rule-based, not an LLM call -- it should be
fast, deterministic, and explainable in one sentence.
"""
from agents.state_template import EntityState  # TODO: fix import path/name


class DetectionAgent:
    name = "detection_agent"

    def run(self, state: EntityState) -> EntityState:
        # TODO: your classification logic here. Example shape:
        # score = <some function of state's raw fields>
        # severity = "high" if score >= THRESHOLD_HIGH else "medium" if ... else "low"
        severity = "medium"  # placeholder
        return {**state, "severity": severity}


detection_agent = DetectionAgent()


def detection_node(state: EntityState) -> EntityState:
    return detection_agent.run(state)


# =============================================================================
"""
TEMPLATE -- RiskAgent (aka ImpactAgent)

Single responsibility: turn "this entity is flagged" into "here's what's
actually affected, and roughly what it costs." Usually a graph
traversal or lookup -- keep it deterministic, not an LLM call, so it's
easy to justify the numbers in Q&A.
"""


class RiskAgent:
    name = "risk_agent"

    def run(self, state: EntityState) -> EntityState:
        # TODO: your impact computation here. Example shape:
        # downstream = <graph traversal, lookup, or rule-based estimate>
        # cost = <a SINGLE, EXPLAINABLE heuristic -- one constant times a count>
        downstream = []       # placeholder
        cost = 0.0             # placeholder
        return {**state, "downstream_impact": downstream, "estimated_cost_impact": cost}


risk_agent = RiskAgent()


def risk_node(state: EntityState) -> EntityState:
    return risk_agent.run(state)


# =============================================================================
"""
TEMPLATE -- RetrievalAgent

Single responsibility: find relevant precedent from a RAG knowledge
base. This is what grounds the recommendation agent's output instead of
letting it hallucinate.
"""
import httpx
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import config

_vectordb = None


def get_vectordb() -> Chroma:
    global _vectordb
    if _vectordb is None:
        client = httpx.Client(verify=config.EMBEDDING_VERIFY_SSL)
        embedding_model = OpenAIEmbeddings(
            base_url=config.EMBEDDING_GATEWAY_URL,
            model=config.EMBEDDING_MODEL,
            api_key=config.EMBEDDING_API_KEY,
            http_client=client,
            # REQUIRED if embedding provider is Ollama or another local
            # OpenAI-compatible endpoint -- see 05_checklists/troubleshooting_cheatsheet.md
            check_embedding_ctx_length=False,
        )
        _vectordb = Chroma(persist_directory=config.CHROMA_DIR, embedding_function=embedding_model)
    return _vectordb


class RetrievalAgent:
    name = "retrieval_agent"

    def run(self, state: EntityState) -> EntityState:
        k = state.get("top_k") or config.DEFAULT_TOP_K
        query = f"{state['entity_id']}"  # TODO: build a real query from state's fields
        similar = get_vectordb().similarity_search(query, k=k)
        context = "\n".join(f"- {d.page_content}" for d in similar)
        return {**state, "retrieved_context": context}


retrieval_agent = RetrievalAgent()


def retrieval_node(state: EntityState) -> EntityState:
    return retrieval_agent.run(state)


# =============================================================================
"""
TEMPLATE -- RecommendationAgent

Single responsibility: the ONE LLM call in the pipeline. Grounded in
Risk + Retrieval agents' output, not just the raw entity.
"""
from langchain_openai import ChatOpenAI

_llm = None


def get_llm() -> ChatOpenAI:
    global _llm
    if _llm is None:
        client = httpx.Client(verify=config.VERIFY_SSL)
        _llm = ChatOpenAI(
            base_url=config.GATEWAY_URL, model=config.CHAT_MODEL,
            api_key=config.API_KEY, http_client=client,
        )
    return _llm


class RecommendationAgent:
    name = "recommendation_agent"

    def run(self, state: EntityState) -> EntityState:
        prompt = f"""You are an expert advisor for [YOUR DOMAIN]. Entity: {state['entity_id']}
Severity: {state['severity']}
Downstream impact: {state.get('downstream_impact')}
Estimated impact: {state.get('estimated_cost_impact')}

Similar past cases:
{state.get('retrieved_context') or 'None found.'}

In under 100 words: 1) plain-language cause, 2) two concrete recommended actions."""
        temp = state.get("temperature") if state.get("temperature") is not None else config.DEFAULT_TEMPERATURE
        response = get_llm().bind(temperature=temp).invoke(prompt)
        return {**state, "recommendation": response.content, "recommendation_category": "general"}  # TODO: real categorization


recommendation_agent = RecommendationAgent()


def recommendation_node(state: EntityState) -> EntityState:
    return recommendation_agent.run(state)


# =============================================================================
"""
TEMPLATE -- EscalationAgent

Single responsibility: decide auto-handle vs. human review. Rule-based,
not an LLM call -- an escalation decision should be auditable by reading
one if-statement.
"""


class EscalationAgent:
    name = "escalation_agent"

    def run(self, state: EntityState) -> EntityState:
        # TODO: your escalation rule here. Example:
        needs_escalation = state["severity"] == "high"  # placeholder
        return {**state, "needs_escalation": needs_escalation}


escalation_agent = EscalationAgent()


def escalation_node(state: EntityState) -> EntityState:
    return escalation_agent.run(state)


def route_after_escalation_check(state: EntityState) -> str:
    return "flag_for_manual_review" if state["needs_escalation"] else "auto_log"
