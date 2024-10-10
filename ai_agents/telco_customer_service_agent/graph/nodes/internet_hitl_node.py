from state import InternetGraphState
from langgraph.prebuilt.tool_executor import ToolExecutor
from tools.CRM_tool import access_crm_tool

tools = [access_crm_tool]

tool_executor = ToolExecutor(tools)

def execute_internet_hitl_tools(state : InternetGraphState):
    agent_action = state["internet_agent_outcome"]

    # Specific tools which require HITL
    if agent_action.tool == "access_crm_tool":
        # Request human approval
        human_approval = input("Do you want to allow agent to access CRM tool ? Answer 'yes' or 'no'")
        if human_approval.lower() == 'yes':
            # If human approves continue
            output = tool_executor.invoke(agent_action)

            # If human does not approve, transfer to live agent
            """------- Routing logic to be implemented ------"""
        return {"internet_agent_intermediate_steps" : [(agent_action, str(output))]}