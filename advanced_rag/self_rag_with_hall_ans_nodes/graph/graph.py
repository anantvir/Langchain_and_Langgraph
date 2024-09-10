from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from graph.constants import GENERATE, GRADE_DOCUMENTS, RETRIEVE, WEBSEARCH, HALLUCINATION, GENERATION_ANSWERS_QUESTION
from graph.nodes import generate, grade_documents, retrieve, web_search, hallucination, answers_question
from graph.state import GraphState
from graph.chains.hallucination_grader import hallucination_grader_chain
from graph.chains.answer_grader import answer_grader_chain
load_dotenv()

# def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
#     print("---CHECK HALLUCINATIONS---")
#     question = state["question"]
#     documents = state["documents"]
#     generation = state["generation"]

#     score = hallucination_grader_chain.invoke(
#         {"documents": documents, "generation": generation}
#     )

#     if hallucination_grade := score.binary_score:
#         print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
#         print("---GRADE GENERATION vs QUESTION---")
#         score = answer_grader_chain.invoke({"question": question, "generation": generation})
#         if answer_grade := score.binary_score:
#             print("---DECISION: GENERATION ADDRESSES QUESTION---")
#             return "useful"
#         else:
#             print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
#             return "not useful"
#     else:
#         print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
#         return "not supported"

def decide_to_generate(state : GraphState):
    print("--- ASSESS GRADED DOCUMENTS AND SELECT TARGET NODE FOR CONDITIONAL EDGE ---")

    if state["web_search"]:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE

def check_hallucination_move_to_node(state : GraphState):
    is_hallucinating = state["is_hallucinating"]
    if is_hallucinating:
        # Instead of returning Node, we return string and then later use path_map
        return "hallucinating"
    else:
        return "not hallucinating"

def check_generation_answers_question_move_to_node(state : GraphState):
    generation_answers_question = state["answers_question"]
    if generation_answers_question:
        # Here we can directly return the Node i.e END but we return string and then map it to node
        # in the path_map arcgument of add_conditional_edges function
        return "generate final answer" 
    else:
        # Here we can directly return the Node i.e WEBSEARCH but we return string and then map it to node
        # in the path_map arcgument of add_conditional_edges function
        return "go back to web search"

workflow = StateGraph(GraphState)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(HALLUCINATION, hallucination)
workflow.add_node(GENERATION_ANSWERS_QUESTION, answers_question)
workflow.set_entry_point(RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, HALLUCINATION)

workflow.add_conditional_edges(
    HALLUCINATION,
    check_hallucination_move_to_node,
    path_map = {
        "hallucinating" : GENERATE,
        "not hallucinating" : GENERATION_ANSWERS_QUESTION
    }
)
workflow.add_conditional_edges(
    GENERATION_ANSWERS_QUESTION,
    check_generation_answers_question_move_to_node,
    path_map = {
        "generate final answer" : END,
        "go back to web search" : WEBSEARCH
    }
)
app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="/Users/anantvirsingh/Desktop/langchain-and-langgraph/advanced_rag/self_rag_with_hall_ans_nodes/self_rag_multinode_graph.png")

print("-------- Created Langgraph diagram in directory --------")