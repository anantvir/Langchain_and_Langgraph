from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from scrape_data_from_web import scrape_data_from_url
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

docs = scrape_data_from_url("https://lilianweng.github.io/posts/2023-06-23-agent/")

# Create small chunks using RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create vector store, from_documents is a function in langchain_community. This helps talk
# to Chroma db, create vectors, reterieve them using parameters etc.
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Create retriever (Also a function from langchain_community package)
"""
More advanced retrieving mechanisms:
1. https://python.langchain.com/v0.2/docs/how_to/MultiQueryRetriever/
2. https://python.langchain.com/v0.2/docs/how_to/multi_vector/
3. https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf
"""
retriever =  vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)






