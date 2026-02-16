"""
LangGraph flow definition for the SMS agent.
"""

from langgraph.graph import StateGraph, END
from functools import partial

from src.agent.state import AgentState
from src.agent.nodes import classify_message_type, generate_sms, update_history
from src.services import GroqClient


def create_sms_graph(groq_client: GroqClient) -> StateGraph:
    """
    Create the LangGraph workflow for SMS generation.

    Args:
        groq_client: Configured Groq client for AI generation

    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(AgentState)

    # Bind groq_client to generate_sms node
    generate_sms_with_client = partial(generate_sms, groq_client=groq_client)

    # Add nodes
    workflow.add_node("classify", classify_message_type)
    workflow.add_node("generate", generate_sms_with_client)
    workflow.add_node("update_history", update_history)

    # Define edges
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "generate")
    workflow.add_edge("generate", "update_history")
    workflow.add_edge("update_history", END)

    return workflow.compile()


def run_agent(lead, groq_client: GroqClient) -> AgentState:
    """
    Run the SMS agent for a single lead.

    Args:
        lead: Lead object from Google Sheet
        groq_client: Configured Groq client

    Returns:
        Final agent state with generated SMS
    """
    graph = create_sms_graph(groq_client)

    initial_state: AgentState = {
        "lead": lead,
        "message_type": "",
        "generated_sms": None,
        "updated_history": None,
        "error": None,
    }

    result = graph.invoke(initial_state)
    return result
