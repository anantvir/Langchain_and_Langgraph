from state import PhoneGraphState
from langgraph.prebuilt.tool_executor import ToolExecutor
from tools.CRM_tool import access_crm_tool

tools = [access_crm_tool]

tool_executor = ToolExecutor(tools)

def execute_phone_hitl_tools(state : PhoneGraphState):
    # agent_action contains all information about which tool to execute with which arguments etc.
    # This is of type AgentAction or AgentFinish and tool_executor can be invoked with these types

    # In this case PHONE_ACT node will be executed only if state["agent_outcome"] is instance of AgentAction
    agent_action = state["phone_agent_outcome"]

    # Specific tools which require HITL
    if agent_action.tool == "access_crm_tool":
        # Request human approval
        human_approval = input("Do you want to allow agent to access CRM tool ? Answer 'yes' or 'no'")
        if human_approval.lower() == 'yes':
            # If human approves continue
            output = tool_executor.invoke(agent_action)

            # If human does not approve, transfer to live agent
            """------- Routing logic to be implemented ------"""
        return {"phone_agent_intermediate_steps" : [(agent_action, str(output))]}
