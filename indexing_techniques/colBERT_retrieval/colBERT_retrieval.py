from get_data import RAG
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


# We can easily convert ragatouille's RAGPretrainedModel to langchain retriever usiing the 
# method they have provided (as_langchain_retriever)
retriever = RAG.as_langchain_retriever(k=3)

#print(retriever.invoke("What animation studio did Miyazaki found?"))

"""---------------------- create Chain ----------------------"""


prompt = ChatPromptTemplate.from_template(
        """Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}"""
        )

llm = ChatOpenAI()

# Predefined chain from Langchain
document_chain = create_stuff_documents_chain(llm, prompt)

# Predefined chain from Langchain
retrieval_chain = create_retrieval_chain(retriever, document_chain)


print(retrieval_chain.invoke({"input": "What animation studio did Miyazaki found?"}))




