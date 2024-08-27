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
from RAG_step_back_prompting import chain_step_back_question_generator

load_dotenv()


# Define you llm instance
llm = ChatOpenAI(model="gpt-4o-mini")

user_question = "What are the main components of an LLM-powered autonomous agent system?"

# Response prompt 
response_prompt_template = """You are an expert of world knowledge. I am going to ask you a question. Your response should be comprehensive and not contradicted with the following context if they are relevant. Otherwise, ignore them if they are not relevant.

                            # {normal_context}
                            # {step_back_context}

                            # Original Question: {question}
                            # Answer:"""

prompt_final_response = ChatPromptTemplate.from_template(response_prompt_template)

chain_final_response = (
    {
        # Get context for actual question asked by user
        "normal_context" : itemgetter("question") | retriever, 

        # Get context for step back question we generated(high level concepts)
        "step_back_context" : chain_step_back_question_generator | retriever ,

        # Actual user question
        "question" : itemgetter("question") 
    }
    | prompt_final_response
    | llm
    | StrOutputParser()
)

final_response = chain_final_response.invoke({"question" : user_question})

print(final_response)


