from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from chunking import retriever
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# HyDE document generation
template = """Please write a scientific paper passage to answer the question
Question: {question}
Passage:"""

prompt_generate_hyde_doc = ChatPromptTemplate.from_template(template)

# Chain to generate HyDE document from input query
chain_generate_hyde_doc = (
    prompt_generate_hyde_doc
    | ChatOpenAI(temperature = 0)
    | StrOutputParser()
)

#user_question = "What is task decomposition for LLM agents?"

#print(chain_generate_hyde_doc.invoke({"question" : user_question}))









