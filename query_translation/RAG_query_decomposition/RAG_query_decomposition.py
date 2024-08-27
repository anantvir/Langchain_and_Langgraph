from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from chunking import retriever

# Decomposition
template = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
The goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \n
Generate multiple search queries related to: {question} \n
Output (3 queries):"""

prompt_for_query_decomposition = ChatPromptTemplate.from_template(template)

# LLM OpenAI instance
llm = ChatOpenAI(temperature=0)

# Query decomposition chain
chain_query_decomposition = (
    prompt_for_query_decomposition
    | llm
    | StrOutputParser()
    | (lambda x : x.split("\n"))
)

# user_question = "What are the main components of an LLM-powered autonomous agent system?"

# questions = chain_query_decomposition.invoke({"question" : user_question})

# print(questions)






