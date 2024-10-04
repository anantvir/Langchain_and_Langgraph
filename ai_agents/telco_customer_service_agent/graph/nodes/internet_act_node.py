# This node will have access to all tools to execute to get to answer
from tools.CRM_tool import access_crm_tool
from langgraph.prebuilt.tool_executor import ToolExecutor
from state import InternetGraphState

tools = [access_crm_tool]

tool_executor = ToolExecutor(tools)

def execute_internet_tools(state : InternetGraphState):

    internet_agent_action = state["internet_agent_outcome"]
    output = tool_executor.invoke(internet_agent_action)
    return{"internet_agent_intermediate_steps" : [(internet_agent_action, str(output))]}
