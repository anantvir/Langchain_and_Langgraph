from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

"""------------------------- Load unstructured data -----------------------"""

loaders = [
    TextLoader("indexing_techniques/parent_document_indexing/data/paul_graham_essay.txt"),
    TextLoader("indexing_techniques/parent_document_indexing/data/state_of_the_union.txt"),
]
docs = []
for loader in loaders:
    docs.extend(loader.load())

"""------------------------- Retrieve full documents -----------------------"""

# This text splitter is used to create the child documents
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# The vectorstore to use to index the child chunks
vectorstore = Chroma(collection_name="full_documents", embedding_function=OpenAIEmbeddings())

# The storage layer for the parent documents
store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore = vectorstore,
    docstore = store,
    child_splitter = child_splitter
)

retriever.add_documents(docs, ids = None)


# Vectorstore similarity search gives us small chunks 
sub_docs = vectorstore.similarity_search("justice breyer")

print(sub_docs[0].page_content)

# When we use ParentDocument retriever, we get parent documents containing
# the chunk instead of chunk itself
retrieved_docs = retriever.invoke("justice breyer")

print("Length of full retrieved document :",len(retrieved_docs[0].page_content))

"""
What to do if parent documents are too large ?

-> Sometimes, the full documents can be too big to want to retrieve them as is. In that case, 
what we really want to do is to first split the raw documents into larger chunks, and then 
split it into smaller chunks. We then index the smaller chunks, but on retrieval we 
retrieve the larger chunks (but still not the full documents).

"""












