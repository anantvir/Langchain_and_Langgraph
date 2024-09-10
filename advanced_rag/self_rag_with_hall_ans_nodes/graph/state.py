from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
        is_hallucinating : weather LLM is hallucinating
        answers_question :  weather LLM generation answers the user question
    """

    question: str
    generation: str
    web_search: bool
    documents: List[str]
    is_hallucinating : bool
    answers_question : bool