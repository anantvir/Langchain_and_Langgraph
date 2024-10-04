from langchain import hub
from langchain.agents import create_react_agent
from tools.CRM_tool import access_crm_tool
from tools.phone_area_service_quality_tool import get_service_quality_in_area
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


react_prompt: PromptTemplate = hub.pull("hwchase17/react")

# Tools specific to Internet use case
tools = [access_crm_tool, get_service_quality_in_area]

llm = ChatOpenAI(temperature=0)

internet_react_agent = create_react_agent(llm, tools, react_prompt)