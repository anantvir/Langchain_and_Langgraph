from state import EntryGraphState
from chains.sentiment_chain import sentiment_chain

def identify_sentiment(state : EntryGraphState):
    user_query = state["user_query"]
    sentiment = sentiment_chain.invoke({"query" : user_query})
    return {"sentiment" : sentiment.content.lower()}





