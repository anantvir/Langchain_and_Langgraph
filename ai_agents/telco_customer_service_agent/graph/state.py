from typing import List, TypedDict
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    """
        represents state of the graph
    """
    user_query : str
    category : str
    sentiment : str
    current_conversation_history : List[BaseMessage]
    resolution_status : bool
    esclation_decision : bool











