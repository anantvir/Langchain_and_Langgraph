from state import EntryGraphState
from chains.categorize_chain import categorization_chain


def categorize(state : EntryGraphState):
    user_query = state["user_query"]
    category = categorization_chain.invoke({"query" : user_query})
    return {"category" : category.content.lower()}
