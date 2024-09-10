from typing import Any, Dict

from graph.chains.generation import generation_chain
from graph.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("----- ENTERING GENERATE NODE -----")
    question = state["question"]
    documents = state["documents"]

    generation = generation_chain.invoke({"context": documents, "question": question})

    # In graph state, initialize values of answers_question and is_hallucinating
    return {"documents": documents, 
            "question": question, 
            "generation": generation, 
            "is_hallucinating" : None,
            "answers_question": None}