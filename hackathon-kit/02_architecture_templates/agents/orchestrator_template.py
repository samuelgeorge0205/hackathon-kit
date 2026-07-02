"""
TEMPLATE -- multi-agent orchestrator. Split the code from
all_agents_template.py into their own files (detection_agent.py,
risk_agent.py, etc.) before using this -- it assumes separate modules.

Wires the 5 agents into a LangGraph state graph:

    detection -> risk -> retrieval -> recommendation -> escalation ──┬──> flag_for_manual_review -> END
                                                                       └──> auto_log -> END
"""
from typing import List, Optional
import pandas as pd
from langgraph.graph import StateGraph, END

from ssl_patch import apply_ssl_monkeypatch
apply_ssl_monkeypatch()

from agents.state import EntityState, new_state  # TODO: fix names/paths
from agents.detection_agent import detection_node
from agents.risk_agent import risk_node
from agents.retrieval_agent import retrieval_node
from agents.recommendation_agent import recommendation_node
from agents.escalation_agent import escalation_node, route_after_escalation_check


def flag_for_manual_review(state: EntityState) -> EntityState:
    print(f"[ESCALATED] {state['entity_id']} needs human review "
          f"(est. impact {state.get('estimated_cost_impact', 0)})")
    return state


def auto_log(state: EntityState) -> EntityState:
    print(f"[LOGGED] {state['entity_id']} -- {state['severity']} severity, recommendation ready")
    return state


def build_pipeline():
    graph = StateGraph(EntityState)
    graph.add_node("detection_agent", detection_node)
    graph.add_node("risk_agent", risk_node)
    graph.add_node("retrieval_agent", retrieval_node)
    graph.add_node("recommendation_agent", recommendation_node)
    graph.add_node("escalation_agent", escalation_node)
    graph.add_node("flag_for_manual_review", flag_for_manual_review)
    graph.add_node("auto_log", auto_log)

    graph.set_entry_point("detection_agent")
    graph.add_edge("detection_agent", "risk_agent")
    graph.add_edge("risk_agent", "retrieval_agent")
    graph.add_edge("retrieval_agent", "recommendation_agent")
    graph.add_edge("recommendation_agent", "escalation_agent")
    graph.add_conditional_edges("escalation_agent", route_after_escalation_check, {
        "flag_for_manual_review": "flag_for_manual_review",
        "auto_log": "auto_log",
    })
    graph.add_edge("flag_for_manual_review", END)
    graph.add_edge("auto_log", END)
    return graph.compile()


def process_single_entity(pipeline, entity_id: str, **kwargs) -> EntityState:
    return pipeline.invoke(new_state(entity_id, **kwargs))


if __name__ == "__main__":
    import sys
    import config
    import os

    os.makedirs(config.DATA_DIR, exist_ok=True)
    pipeline = build_pipeline()
    entities = pd.read_csv(f"{config.DATA_DIR}/flagged_entities.csv")  # TODO: your filename

    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(entities)
    to_process = entities.head(limit)

    results = []
    for idx, (_, row) in enumerate(to_process.iterrows(), start=1):
        final_state = process_single_entity(pipeline, row["entity_id"])  # TODO: pass real fields
        results.append(final_state)
        print(f"  [{idx}/{len(to_process)}] {row['entity_id']} done")
        if idx % 10 == 0 or idx == len(to_process):
            pd.DataFrame(results).to_csv(f"{config.DATA_DIR}/pipeline_output.csv", index=False)

    print(f"Pipeline processed {len(results)}/{len(to_process)} -> {config.DATA_DIR}/pipeline_output.csv")
