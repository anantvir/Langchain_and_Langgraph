from langchain.tools import tool
from langchain_core.runnables.config import RunnableConfig

# Assumption : User was authenticated before entering chatbot, so we have access to User ID
@tool
def access_crm_tool(tool_input, config : RunnableConfig) -> str:
    """
    This tool is called when you want to lookup customer detail, past tickets, resolutions, products they own etc. from CRM system. Tool called with input 'customerId'
    """
    userId = config.get("configurable", {}).get("user_id")
    # Get user record from CRM using userId
    # Feed this into LLM and store it in conversation history
    crm_data = """Customer faced similar issue before where the calls were dropping every 30 seconds
    and network coverage in the area was poor. Customer support agent provided a resolution
    by resetting the phone network by transferring it from one cell tower to another"""
    
    return  crm_data
