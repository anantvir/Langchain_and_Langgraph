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
from multi_query_retrieval import retrieval_chain
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter

load_dotenv()


# Define you llm instance
llm = ChatOpenAI(model="gpt-4o-mini")

prompt_template = """Answer the following question based on this context:

        {context}

        Question: {question}
        """

final_input_prompt = ChatPromptTemplate.from_template(prompt_template)

user_question = "What is task decomposition for LLM agents?"

final_multi_query_rag_chain = (
    {"context": retrieval_chain, "question": itemgetter("question")}
    | final_input_prompt
    | llm
    | StrOutputParser()
)

print(final_multi_query_rag_chain.invoke({"question" : user_question})) 











