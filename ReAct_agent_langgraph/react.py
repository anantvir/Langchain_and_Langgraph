from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

react_prompt: PromptTemplate = hub.pull("hwchase17/react")

@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled ->  multiplied by 3
    """
    return 3 * float(num)

tools = [TavilySearchResults(max_results=1), triple]

llm = ChatOpenAI(model="gpt-3.5-turbo-1106")

react_agent_runnable = create_react_agent(llm, tools, react_prompt)









