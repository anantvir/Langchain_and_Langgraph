from graph.chains.answer_grader import answer_grader_chain
from graph.state import GraphState


def answers_question(state : GraphState):

    # From state, we need to get
    # 1. Generated answer  2. User question  3. answers_question flag
    generated_answer = state["generation"]
    user_question = state["question"]
    answers_question = state["answers_question"]

    # Invoke answer grader chain
    score = answer_grader_chain.invoke(
        {
            "question" : user_question,
            "generation" : generated_answer
        }
    )
    if score:
        print("----- DECISION : GENERATION ANSWERS QUESTION -----")
        # Set new graph state
        return{"answers_question" : True}
    else:
        print("----- DECISION : GENERATION DOES NOT ANSWER QUESTION -----")
        
        # Set new graph state
        return{"answers_question" : False}


