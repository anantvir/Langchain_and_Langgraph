from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from chunking import retriever

# Multi query retrieval prompt
# Multi Query: Different Perspectives
template = """You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""

multi_query_prompt = ChatPromptTemplate.from_template(template)

# Get list of multiple queries similar to original user query
generate_multiple_queries_chain = (
    multi_query_prompt 
    | ChatOpenAI(temperature = 0) 
    | StrOutputParser()
    | (lambda x : x.split("\n"))
)

# Once we retrieve relevant documents from vector db for these 5 generated queries, we need
# to make sure we take only unique documents from all retrieved documents for these 5 queries

def get_unique_union(documents : list[list]):
    """ Unique union of retrieved docs """

    # Flatten the list of lists into a single list with all strings so that duplicates can be removed
    # using set() since strings are easily hashable
    flattened_documents = []
    for sublist in documents:
        for document in sublist:
            flattened_documents.append(dumps(document))
    
    # Get unique strings
    unique_strs = list(set(flattened_documents))

    return [loads(document) for document in unique_strs]

# Retrieve

user_question = "What is task decomposition for LLM agents?"

retrieval_chain = (
    generate_multiple_queries_chain
    | retriever.map()   # returns list[list] which is passed to get_unique_union(documents : list[list])
    | get_unique_union
)

final_unique_docs_for_llm_context = retrieval_chain.invoke({"question" : user_question})

#print(final_unique_docs_for_llm_context)




