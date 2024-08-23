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



"""
The above chain is already implemented by Langchain for us through the function create_stuff_documents_chain()

Two convenience functions that create pre constructed retrieval chains for us are

1. create_stuff_documents_chain()
2. create_retrieval_chain()

Details : https://python.langchain.com/v0.2/docs/tutorials/rag/#retrieval-and-generation-retrieve
"""













