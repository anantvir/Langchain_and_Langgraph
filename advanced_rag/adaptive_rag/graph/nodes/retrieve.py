from typing import Any, Dict

from graph.state import GraphState
from ingestion import retriever

# Every node takes as input the state of the graph and then updates it and outputs it
def retrieve(state : GraphState) -> Dict[str, Any]:
    print("----- Entering RETRIEVE node -----")

    # Extract user question from state
    question = state["question"]

    # Retrieve documents from vectorstore for above user question
    documents = retriever.invoke(question)

    # Update state with new information
    return {"documents" : documents, "question" : question} # We dont need to update question here but just being cautious








