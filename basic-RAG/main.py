"""
Credits  : https://python.langchain.com/v0.2/docs/tutorials/rag/#indexing-load
"""

from dotenv import load_dotenv
import getpass
import os
from langchain_openai import ChatOpenAI
import bs4
from langchain_community.document_loaders import WebBaseLoader
from chunking import format_docs
from langchain import hub
from chunking import retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


# Define you llm instance
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = hub.pull("rlm/rag-prompt")


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

for chunk in rag_chain.stream("What is Task Decomposition?"):
    print(chunk, end="", flush=True)

















