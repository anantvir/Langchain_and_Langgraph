"""This node is where we run all tools specified in tool_calls field"""
from state import IotGraphState
from tools.CRM_tool import access_crm_tool
from langgraph.prebuilt.tool_executor import ToolExecutor

tools = [access_crm_tool]

tool_executor = ToolExecutor(tools)

def iot_act_node_execute_tools(state : IotGraphState):
    iot_agent_outcome = state['iot_agent_outcome']
    output = tool_executor.invoke(iot_agent_outcome)
    return {"iot_agent_intermediate_steps" : [(iot_agent_outcome, str(output))]}

    








