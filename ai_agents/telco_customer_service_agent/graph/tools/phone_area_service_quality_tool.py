from langchain.tools import tool
from typing import Union

# Assumption : User was authenticated before entering chatbot, so we have access to User ID
@tool
def get_service_quality_in_area(userId : Union[int, str]) -> str :
    """
    Lookup current quality of service in area 

    Args:
        userId : Unique user id
    """

    return "service quality return"


