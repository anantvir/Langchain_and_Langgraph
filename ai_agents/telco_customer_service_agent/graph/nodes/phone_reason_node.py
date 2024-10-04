""" 
1. Extract user query from state
2. Get ReAct prompt from hub and modify it for phone use case
3. Create ReAct agent. Provide it llm, tools, react prompt
4. When agent reasons, store the thought, action in intermediate steps in state
5. Execute the tools and store observation in intermediate steps

This node processes customer questions about their phone plan, network issues, call quality,
upgrading plan, activate roaming etc. (basicall everything around phone).
If our chatbot cannot answer the question, we delegate to human

"""
from chains.phone_react_agent_chain import react_agent
from state import PhoneGraphState


def phone_reason_node(state : PhoneGraphState):
    user_query = state["user_query"]
    intermediate_steps = state["phone_agent_intermediate_steps"]
    
    # This returns either AgentAction or AgentFinish and we set it as agent_outcome in state
    agent_reasoning_outcome = react_agent.invoke({"input" : user_query, "intermediate_steps" : intermediate_steps})

    return {"phone_agent_outcome" : agent_reasoning_outcome}



