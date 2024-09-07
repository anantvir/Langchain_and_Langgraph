from dotenv import load_dotenv
from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph
from nodes import run_agent_reasoning_engine, execute_tools
from state import AgentState

load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"


def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT # This should be name of node where we want to go if not ending the loop
    
flow = StateGraph(AgentState)

flow.add_node(AGENT_REASON, run_agent_reasoning_engine)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, execute_tools)


flow.add_conditional_edges(
    AGENT_REASON,
    should_continue,
)

flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="/Users/anantvirsingh/Desktop/langchain-and-langgraph/ReAct_agent_langgraph/graph.png")


if __name__ == '__main__':
    print("Entering Langgraph ReAct agent ...")

    res = app.invoke(
        input={
            "input": "what is the weather in Detroit ? List it and then Triple it ",
        }
    )
    print(res["agent_outcome"].return_values["output"])