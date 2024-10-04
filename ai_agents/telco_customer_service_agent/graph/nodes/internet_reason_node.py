from chains.internet_react_agent_chain import internet_react_agent
from state import InternetGraphState


def internet_reason_node(state : InternetGraphState):
    # Get user question
    user_query = state["user_query"]
    intermediate_steps = state["internet_agent_intermediate_steps"]

    # Ask the agent to reason how to answer this question using any tools it has access to
    agent_reasoning_response = internet_react_agent.invoke({"input" : user_query, "intermediate_steps" : intermediate_steps})

    return {"internet_agent_outcome" : agent_reasoning_response}