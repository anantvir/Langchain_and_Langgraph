from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.document_compressors import LLMChainFilter
from langchain_community.embeddings import CohereEmbeddings
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere

load_dotenv()

llm = Cohere(temperature=0)

# Helper function for printing docs
def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

# Load documents
documents = TextLoader("/Users/anantvirsingh/Desktop/langchain-and-langgraph/post_processing/reranking_documents/data/state_of_the_union.txt").load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

# Configure retriever and retrieve top 20 docs based on vector similarity
retriever = FAISS.from_documents(
    texts, CohereEmbeddings(model="embed-english-v3.0", user_agent="my_app")
).as_retriever(search_kwargs={"k": 20})

# Cohere rerank model returns Sequence[Document]i.e list of reranked documents
compressor = CohereRerank(model="rerank-english-v3.0")

# Contextual compressor uses provided retriever to first retrieve docs, then it uses provided compressor
# to contextually compress those docs. Contextual Compression could mean filtering out relevant text from each document
# or it could mean just return reranked documents in this case without modifying/filtering text of each document
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

# Invole our compression retriever
compressed_docs = compression_retriever.invoke(
    "What did the president say about Ketanji Jackson Brown"
)

# Returns 3 documents out of 20 retrieved
pretty_print_docs(compressed_docs)

























