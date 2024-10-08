from langchain.tools import tool
from typing import Union
from langchain_core.runnables.config import RunnableConfig

# Assumption : User was authenticated before entering chatbot, so we have access to User ID
@tool
def get_service_quality_in_area(userId : Union[int, str], config : RunnableConfig) -> str :
    """
    Lookup current quality of service in area 
    """

    return "service quality return"


