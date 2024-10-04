from langgraph.graph import StateGraph, END, START
from state import EntryGraphState, PhoneGraphState, InternetGraphState, IotGraphState
from nodes.categorize_node import categorize
from nodes.sentiment_node import identify_sentiment
from nodes.phone_reason_node import phone_reason_node
from nodes.internet_reason_node import internet_reason_node
from nodes.phone_act_node import execute_phone_tools
from nodes.internet_act_node import execute_internet_tools
from nodes.iot_reason_node import iot_reason_node
from nodes.iot_act_node import iot_act_node_execute_tools
from langchain_core.agents import AgentAction, AgentFinish
from constants import (
                CATEGORIZE, SENTIMENT, PHONE_REASON, PHONE_ACT, PHONE_REACT_AGENT,
                INTERNET_REASON, INTERNET_ACT, INTERNET_REACT_AGENT,
                IOT_REASON, IOT_ACT, IOT_REACT_AGENT)

def should_phone_reasoning_continue(state : PhoneGraphState):
    if isinstance(state["phone_agent_outcome"], AgentAction):
        return PHONE_ACT
    elif isinstance(state["phone_agent_outcome"], AgentFinish):
        return END 

def should_internet_reasoning_continue(state : InternetGraphState):
    if isinstance(state["internet_agent_outcome"], AgentAction):
        return INTERNET_ACT
    elif isinstance(state["internet_agent_outcome"], AgentFinish):
        return END  
    
def should_iot_reasoning_continue(state : IotGraphState):
    if isinstance(state["iot_agent_outcome"], AgentAction):
        return IOT_ACT
    elif isinstance(state["iot_agent_outcome"], AgentFinish):
        return END

def add_conditonal_edge_from_sentiment(state : EntryGraphState):
    category = state["category"]
    if category.lower() == "phone":
        return "run PHONE_REACT_AGENT node"
    elif category.lower() == "internet":
        return "run INTERNET_REACT_AGENT node"
    elif category.lower() == "iot":
        return "run IOT_REACT_AGENT node"

# subgraph for Phone
phone_subgraph = StateGraph(PhoneGraphState)
phone_subgraph.add_node(PHONE_REASON, phone_reason_node)
phone_subgraph.add_node(PHONE_ACT, execute_phone_tools)
phone_subgraph.add_conditional_edges(PHONE_REASON, should_phone_reasoning_continue)
phone_subgraph.add_edge(PHONE_ACT, PHONE_REASON)
phone_subgraph.set_entry_point(PHONE_REASON)

# subgraph for Internet
internet_subgraph = StateGraph(InternetGraphState)
# Add nodes for Internet
internet_subgraph.add_node(INTERNET_REASON, internet_reason_node)
internet_subgraph.add_node(INTERNET_ACT, execute_internet_tools)
internet_subgraph.set_entry_point(INTERNET_REASON)
# Add edges for Internet
internet_subgraph.add_edge(INTERNET_ACT, INTERNET_REASON)
internet_subgraph.add_conditional_edges(INTERNET_REASON, should_internet_reasoning_continue)

# subgraph for Iot
iot_subgraph = StateGraph(IotGraphState)
# Add nodes for Iot
iot_subgraph.add_node(IOT_REASON, iot_reason_node)
iot_subgraph.add_node(IOT_ACT, iot_act_node_execute_tools)
iot_subgraph.set_entry_point(IOT_REASON)
# Add edges for Iot
iot_subgraph.add_edge(IOT_ACT, IOT_REASON)
iot_subgraph.add_conditional_edges(IOT_REASON, should_iot_reasoning_continue)


entry_graph = StateGraph(EntryGraphState)
# Add nodes
entry_graph.add_node(CATEGORIZE, categorize)
entry_graph.add_node(SENTIMENT, identify_sentiment)
entry_graph.add_node(PHONE_REACT_AGENT, phone_subgraph.compile())
entry_graph.add_node(INTERNET_REACT_AGENT, internet_subgraph.compile())
entry_graph.add_node(IOT_REACT_AGENT, iot_subgraph.compile())

# Add edges
entry_graph.add_edge(START, CATEGORIZE)
entry_graph.add_edge(CATEGORIZE, SENTIMENT)
entry_graph.add_edge(PHONE_REACT_AGENT, END)
entry_graph.add_conditional_edges(SENTIMENT, 
                                  add_conditonal_edge_from_sentiment,
                                  path_map={
                                      "run PHONE_REACT_AGENT node" : PHONE_REACT_AGENT,
                                      "run INTERNET_REACT_AGENT node" : INTERNET_REACT_AGENT,
                                      "run IOT_REACT_AGENT node" : IOT_REACT_AGENT
                                  })
entry_graph.add_edge(INTERNET_REACT_AGENT, END)
entry_graph.add_edge(IOT_REACT_AGENT, END)

entry_flow = entry_graph.compile()

entry_flow.get_graph(xray=1).draw_mermaid_png(output_file_path="/Users/anantvirsingh/Desktop/langchain-and-langgraph/ai_agents/telco_customer_service_agent/graph2.png")
#print(phone_subgraph.compile().get_graph().draw_mermaid())

if __name__ == '__main__':
    print("Entering Langgraph ReAct agent ...")

    res = entry_flow.invoke(
        input={
            "user_query": "I need help with my phone. Everytime I call someone, my call drops after 30 seconds"
        }
    )