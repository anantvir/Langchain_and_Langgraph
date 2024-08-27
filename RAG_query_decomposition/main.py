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
from RAG_query_decomposition import chain_query_decomposition

load_dotenv()


# Define you llm instance
llm = ChatOpenAI(model="gpt-4o-mini")

user_question = "What are the main components of an LLM-powered autonomous agent system?"

# list of questions
decomposed_questions = chain_query_decomposition.invoke({"question" : user_question})

template_to_answer_decomposed_questions = """Here is the question you need to answer:

                \n --- \n {question} \n --- \n

                Here is any available background question + answer pairs:

                \n --- \n {q_a_pairs} \n --- \n

                Here is additional context relevant to the question: 

                \n --- \n {context} \n --- \n

                Use the above context and any background question + answer pairs to answer the question: \n {question}
                """

prompt_to_answer_decomposed_questions = ChatPromptTemplate.from_template(template_to_answer_decomposed_questions)

def format_qa_pair(question, answer):
    """Format Q and A pair"""
    
    formatted_string = ""
    formatted_string += f"Question: {question}\nAnswer: {answer}\n\n"
    return formatted_string.strip()

q_a_pairs = ""
for q in decomposed_questions:

    # Answer question i.e call final RAG chain
    # This RAG chain takes into account all previous Q&As and current retrieved documents
    # (Previous Q/A History + questions retrieved for current question) -> are passed to -> (final RAG chain)
    final_RAG_chain = (
        {
            "context" : itemgetter("question") | retriever,
            "question" : itemgetter("question"),
            "q_a_pairs" : itemgetter("q_a_pairs")
        }
        | prompt_to_answer_decomposed_questions
        | llm
        | StrOutputParser()
    )

    answer = final_RAG_chain.invoke({"question" : q, "q_a_pairs" : q_a_pairs})

    # Save Ques. and Ans. to memory
    # q_a_pairs += add Question : {current question} Answer : { whatever was output of LLM}
    q_a_pair = format_qa_pair(q,answer)
    q_a_pairs = q_a_pairs + "\n---\n"+  q_a_pair

    
    





