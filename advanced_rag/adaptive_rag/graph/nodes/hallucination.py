from graph.chains.hallucination_grader import hallucination_grader_chain
from graph.chains.answer_grader import answer_grader_chain
from graph.state import GraphState


def hallucination(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    is_hallucinating = state["is_hallucinating"]

    score = hallucination_grader_chain.invoke(
        {"documents": documents, "generation": generation}
    )
    
    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        is_hallucinating = False
        return {"is_hallucinating" : is_hallucinating}
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        is_hallucinating = True
        return {"is_hallucinating" : is_hallucinating}

















