"""
Here we create a semantic layer on top of our graph. This means that we give our LLM access to
various tools to interact with our graph
"""

from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from create_graph_db import create_graph_db
from typing import List, Optional, Tuple, Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.callbacks import AsyncCallbackManagerForToolRun,CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function

load_dotenv()

graph = create_graph_db()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

graph.refresh_schema()


description_query = """
                    MATCH (m:Movie|Person)
                    WHERE m.title CONTAINS $candidate OR m.name CONTAINS $candidate
                    MATCH (m)-[r:ACTED_IN|HAS_GENRE]-(t)
                    WITH m, type(r) as type, collect(coalesce(t.name, t.title)) as names
                    WITH m, type+": "+reduce(s="", n IN names | s + n + ", ") as types
                    WITH m, collect(types) as contexts
                    WITH m, "type:" + labels(m)[0] + "\ntitle: "+ coalesce(m.title, m.name) 
                        + "\nyear: "+coalesce(m.released,"") +"\n" +
                        reduce(s="", c in contexts | s + substring(c, 0, size(c)-2) +"\n") as context
                    RETURN context LIMIT 1
                    """
"""
We have defined the Cypher statement used to retrieve information. Therefore, we can avoid 
generating Cypher statements and use the LLM agent to only populate the input parameters.
"""
def get_information(entity: str) -> str:
    try:
        # Query knowledge graph 
        data = graph.query(description_query, params={"candidate": entity})
        return data[0]["context"]
    except IndexError:
        return "No information was found"



"""--------------------Custom Tool Creation----------------------"""

class InformationInput(BaseModel):
    entity: str = Field(description="movie or a person mentioned in the question")

# Langchain tools can be created in 3 ways
#   1.  Functions : Using @tool decorator
#   2.  LangChain Runnables : LangChain Runnables that accept string or dict input can be converted to tools using the as_tool method
#   3.  By sub-classing from BaseTool -- This is the most flexible method, it provides the largest 
#         degree of control, at the expense of more effort and code.
class InformationTool(BaseTool):
    name = "Information"
    description = (
        "useful for when you need to answer questions about various actors or movies"
    )
    # Input argument to this tool is of Type BaseModel
    args_schema: Type[BaseModel] = InformationInput

    # Returns callback function get_information
    def _run(self, entity: str, run_manager: Optional[CallbackManagerForToolRun] = None,) -> str:
        """Use the tool."""
        return get_information(entity)

    async def _arun(self, entity: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return get_information(entity)


"""------------------- OpenAI Agent ------------------"""

tools = [InformationTool()]

llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that finds information about movies "
            " and recommends them. If tools require follow up questions, "
            "make sure to ask the user for clarification. Make sure to include any "
            "available options that need to be clarified in the follow up questions "
            "Do only the things the user specifically requested. ",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
        # ,
        # MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# This function creates chat history between Human and AI
def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

agent = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: _format_chat_history(x["chat_history"])
        if x.get("chat_history")
        else [],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "Who played in Casino?"})






