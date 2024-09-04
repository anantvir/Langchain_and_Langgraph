"""
Main Idea : Create a summary of each chunk and embedd that in vector store.
For every user query, the MultiVectorRetriever will run a similarity search between user query and vectorstore docs. This
similarity search will return summary/summaries. Then MultiVectorRetriever will retrieve corresponding
larger source documents from which these summaries have been generated. Feed these larger source documents and user query
as context to LLM to answer user question
"""
from langchain.storage import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from create_vectorstore import docs
from langchain_openai import ChatOpenAI
import uuid
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers.multi_vector import MultiVectorRetriever

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# This chain takes in a full Document and creates a summary. 
chain = (
    {"doc": lambda x: x.page_content}
    | ChatPromptTemplate.from_template("Summarize the following document:\n\n{doc}")
    | llm
    | StrOutputParser()
)

# Run this chain on list of Documents. Returns list of Document objects(summaries)
summaries = chain.batch(docs, {"max_concurrency": 5})

# The vectorstore to use to index the child chunks
vectorstore = Chroma(collection_name='summaries', embedding_function=OpenAIEmbeddings())

# The storage layer for the parent documents
store = InMemoryByteStore()
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)

# Create unique id for each chunked document
doc_ids = [str(uuid.uuid4()) for _ in docs]

# Create Document object for each summary. Add unique doc_id with each summary
summary_docs = [
    Document(page_content=s, metadata={id_key: doc_ids[i]})
    for i, s in enumerate(summaries)
]

retriever.vectorstore.add_documents(summary_docs)
retriever.docstore.mset(list(zip(doc_ids, docs)))

"""-----------Querying the vector store will return summaries:----------"""
sub_docs = retriever.vectorstore.similarity_search("justice breyer")

print(sub_docs[0]) # Summary returned against user query

"""-----------Whereas the retriever will return the larger source document -------"""

retrieved_docs = retriever.invoke("justice breyer")

len(retrieved_docs[0].page_content)












