from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_react_agent
from tools.CRM_tool import access_crm_tool
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0)

tools = [access_crm_tool]

react_prompt: PromptTemplate = hub.pull("hwchase17/react")

iot_react_agent = create_react_agent(llm,tools,react_prompt)












