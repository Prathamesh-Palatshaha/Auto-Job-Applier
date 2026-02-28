from langgraph.graph import StateGraph, START, END
from state import JobApplicationState

from agents.resume_agent import resume_agent
from agents.job_search_agent import job_search_agent
from agents.job_evaluator_agent import job_evaluator_agent
from agents.review_agent import review_agent
from agents.tracker_agent import tracker_agent

def route_decision(state: JobApplicationState):
    """Routes the graph based on the LLM's evaluation decision."""
    if state.get("decision") == "apply":
        return "review"
    return END

def route_after_review(state: JobApplicationState):
    """Routes the graph based on human-in-the-loop approval."""
    if state.get("human_approval") == "approved":
        return "tracker"
    return END

def build_graph():
    workflow = StateGraph(JobApplicationState)

    workflow.add_node("resume", resume_agent)
    workflow.add_node("job_search", job_search_agent)
    workflow.add_node("evaluate", job_evaluator_agent)
    workflow.add_node("review", review_agent)
    workflow.add_node("tracker", tracker_agent)

    workflow.set_entry_point("resume")

    workflow.add_edge("resume", "job_search")
    workflow.add_edge("job_search", "evaluate")

    workflow.add_conditional_edges(
        "evaluate",
        route_decision,
        {
            "review": "review",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "review",
        route_after_review,
        {
            "tracker": "tracker",
            END: END
        }
    )

    workflow.add_edge("tracker", END)

    return workflow.compile()