from langchain.tools import tool
from typing import Union, Any

# Assumption : User was authenticated before entering chatbot, so we have access to User ID
@tool
def retrieve_from_vectorstore(userId : Union[int, str, Any]) -> str :
    """
    This tool used to answer any questions around phone plan, network issues, call quality, upgrading plan, activate roaming etc. (basicall everything around phone).
    """
    pass