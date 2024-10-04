from state import PhoneGraphState
from langgraph.prebuilt.tool_executor import ToolExecutor
from tools.CRM_tool import access_crm_tool

tools = [access_crm_tool]

tool_executor = ToolExecutor(tools)

def execute_phone_tools(state : PhoneGraphState):
    # agent_action contains all information about which tool to execute with which arguments etc.
    # This is of type AgentAction or AgentFinish and tool_executor can be invoked with these types

    # In this case PHONE_ACT node will be executed only if state["agent_outcome"] is instance of AgentAction
    agent_action = state["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return{"intermediate_steps" : [(agent_action, str(output))]}