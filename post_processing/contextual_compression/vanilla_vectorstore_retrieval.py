from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

load_dotenv()

# Helper function for printing docs


def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

documents = TextLoader("/Users/anantvirsingh/Desktop/langchain-and-langgraph/post_processing/contextual_compression/data/state_of_the_union.txt").load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

texts = text_splitter.split_documents(documents)

retriever = FAISS.from_documents(texts, OpenAIEmbeddings()).as_retriever()


docs = retriever.invoke("What did the president say about Ketanji Brown Jackson")
#pretty_print_docs("Original uncomressed retrieved documents :",docs)

"""----------------- Add contextual compression -------------------"""

# Now let's wrap our base retriever with a ContextualCompressionRetriever. We'll add an 
# LLMChainExtractor, which will iterate over the initially returned documents and extract 
# from each only the content that is relevant to the query.

llm = OpenAI(temperature=0)

# Document compressor that uses an LLM chain to extract the relevant parts of documents.
compressor = LLMChainExtractor.from_llm(llm)


compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

compressed_docs = compression_retriever.invoke(
    "What did the president say about Ketanji Jackson Brown"
)

print(compressed_docs)

















