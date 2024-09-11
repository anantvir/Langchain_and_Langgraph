"""Literal library is used to specify that a variable or a function argument can only take on specific, predefined values.  """
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    # Literal library is used to specify that a variable or a function argument can only take on specific, predefined values. 
    # datasource can only have 2 values "vectorstore" and "websearch"
    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )

llm = ChatOpenAI(temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

# Prompt tells LLM what data source has what type of data. This will help LLM decide where to route query
system = """You are an expert at routing a user question to a vectorstore or web search.
            The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
            Use the vectorstore for questions on these topics. For everything else, use web-search."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router_chain = route_prompt | structured_llm_router