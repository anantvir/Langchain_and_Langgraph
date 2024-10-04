from langchain.tools import tool
from typing import Union

# Assumption : User was authenticated before entering chatbot, so we have access to User ID
@tool
def access_billing_details_from_db(userId : Union[int, str]) -> str :
    """
    Lookup customer billing and plan details

    Args:
        userId : Unique user id
    """
    # Connect to database

    # query plan details for user with username and password

    # convert that table row into text data to feed into LLM context and store into conversation history

    pass


