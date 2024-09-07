from dotenv import load_dotenv
from langgraph.prebuilt.tool_executor import ToolExecutor

from react import react_agent_runnable, tools
from state import AgentState

load_dotenv()

def run_agent_reasoning_engine(state: AgentState):
    # state object has a property "input" and so does react_agent_runnable. So it can be invoked
    agent_outcome = react_agent_runnable.invoke(state)
    
    # agent_outcome property in state will be overwritten when node returns as its not being added
    return {"agent_outcome": agent_outcome}


tool_executor = ToolExecutor(tools)


def execute_tools(state: AgentState):
    # agent_action contains all information about which tool to execute with which arguments etc.
    # This is of type AgentAction or AgentFinish and tool_executor can be invoked with these types
    agent_action = state["agent_outcome"]
    output = tool_executor.invoke(agent_action)

    # This value of intermediate_steps will be added to existing value
    return {"intermediate_steps": [(agent_action, str(output))]}








