from state import PhoneGraphState
from langgraph.prebuilt.tool_executor import ToolExecutor
from tools.CRM_tool import access_crm_tool
from tools.phone_area_service_quality_tool import get_service_quality_in_area
from langgraph.errors import NodeInterrupt

tools = [access_crm_tool, get_service_quality_in_area]

tool_executor = ToolExecutor(tools)

def execute_phone_tools(state : PhoneGraphState):
    # agent_action contains all information about which tool to execute with which arguments etc.
    # This is of type AgentAction or AgentFinish and tool_executor can be invoked with these types

    # In this case PHONE_ACT node will be executed only if state["agent_outcome"] is instance of AgentAction
    agent_action = state["phone_agent_outcome"]

    if agent_action.tool == "get_service_quality_in_area":
        # Only run this node for specific tools which dont require HITL. 
        # For HITL, we conditionally go to phone_hitl_node        

        output = tool_executor.invoke(agent_action)
        return{"phone_agent_intermediate_steps" : [(agent_action, str(output))]}