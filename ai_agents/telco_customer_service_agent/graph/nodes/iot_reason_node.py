from chains.iot_react_agent_chain import iot_react_agent
from state import IotGraphState


def iot_reason_node(state : IotGraphState):
    user_query = state['user_query']
    intermediate_steps = state["iot_agent_intermediate_steps"]

    # AgentAction or AgentFinish
    iot_agent_outcome_from_react_prompt = iot_react_agent.invoke(
        {
            "input" : user_query,
            "intermediate_steps" : intermediate_steps
        }
    )
    return {"iot_agent_outcome" : iot_agent_outcome_from_react_prompt}
    