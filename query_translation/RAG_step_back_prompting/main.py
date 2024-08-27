"""
This is just a re-implementation of original, all credits to original author : 
https://github.com/langchain-ai/rag-from-scratch/blob/main/rag_from_scratch_5_to_9.ipynb

Paper : https://arxiv.org/pdf/2402.03367

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
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter

load_dotenv()


# Define you llm instance
llm = ChatOpenAI(model="gpt-4o-mini")

user_question = "What are the main components of an LLM-powered autonomous agent system?"
