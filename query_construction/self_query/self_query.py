"""
---------------------- https://blog.langchain.dev/query-construction/ ------------------------
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import ChatOpenAI
from langchain.chains.query_constructor.base import (
    StructuredQueryOutputParser,
    get_query_constructor_prompt,
)
from create_vector_store import metadata_field_info, document_content_description, vectorstore
from langchain_community.query_constructors.chroma import ChromaTranslator

from dotenv import load_dotenv

load_dotenv()

"""Langchain provides built in SelfQueryRetriever but we will be building from scratch using LCEL"""

# ------------------------ Self Query Construction --------------------------
prompt = get_query_constructor_prompt(document_content_description, metadata_field_info)

llm = ChatOpenAI(temperature=0)


output_parser = StructuredQueryOutputParser.from_components()
query_constructor = prompt | llm | output_parser


#print(prompt.format(query="What are some sci-fi movies from the 90's directed by Luc Besson about taxi drivers"))

print(query_constructor.invoke(
    {
        "query": "What are some sci-fi movies from the 90's directed by Luc Besson about taxi drivers"
    }
))

# ------------------------ Self Query Translator --------------------------
"""This is the object responsible for translating the generic StructuredQuery object into a 
metadata filter in the syntax of the vector store you're using."""

retriever = SelfQueryRetriever(
    query_constructor=query_constructor,
    vectorstore=vectorstore,
    structured_query_translator=ChromaTranslator(),
)

print(retriever.invoke(
    "What's a movie after 1990 but before 2005 that's all about toys, and preferably is animated"
))







