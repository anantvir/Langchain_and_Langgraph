from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver


class State(TypedDict):
    input: str
    user_feedback: str

def step_1(state: State) -> None:
    print("---Step 1---")


def human_feedback(state: State) -> None:
    print("---human_feedback---")


def step_3(state: State) -> None:
    print("---Step 3--")

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

#memory = SqliteSaver.from_conn_string("checkpoints.sqlite")
memory = MemorySaver()

graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])

graph.get_graph().draw_mermaid_png(output_file_path="/Users/anantvirsingh/Desktop/langchain-and-langgraph/human_in_the_loop_memory/graph.png")

if __name__ == "__main__":
    # Unique thread ID for each user conversation/session. Can use uuid etc.
    thread = {"configurable": {"thread_id": "1"}}

    initial_input = {"input": "hello world"}

    # Stream each graph event
    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(event)
    
    # Get next node in graph
    print(graph.get_state(thread).next)

    print("--- State before update --- \n",graph.get_state(thread))

    user_input = input("Tell me how you want to update the state: ")

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback")

    print("--- State after update --- \n",graph.get_state(thread))

    # Stream graph events after user feedback
    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)















