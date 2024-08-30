"""
1. Different promopts achieve different tasks. Embed each prompt
2. Embedd user query
3. Compare user embedded query with embedded prompts and then route query to appropriate 
prompt based on similarity

"""


from langchain_community.utils.math import cosine_similarity
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()

# Embedding model
embedding_model = OpenAIEmbeddings()

# Prompt 1
physics_template = """You are a very smart physics professor. \
                    You are great at answering questions about physics in a concise and easy to understand manner. \
                    When you don't know the answer to a question you admit that you don't know.

                    Here is a question:
                    {question}"""

# Prompt 2
math_template = """You are a very good mathematician. You are great at answering math questions. \
                    You are so good because you are able to break down hard problems into their component parts, \
                    answer the component parts, and then put them together to answer the broader question.

                    Here is a question:
                    {question}"""

prompt_templates = [physics_template, math_template]

# Embed both prompts
embedded_prompts = embedding_model.embed_documents([physics_template, math_template])

# Make this function RunnableLambda. Input is a dictionary
# Inputs to RunnableLambda is always dictionary
def prompt_router(input):
    query_embedding = embedding_model.embed_query(input["question"])
    
    # calculate similarity between embedded user query and embedded prompts
    similarity = cosine_similarity([query_embedding], embedded_prompts)[0]
    most_similar_prompt = prompt_templates[similarity.argmax()]
    print("Using MATH" if most_similar_prompt == math_template else "Using PHYSICS")
    return PromptTemplate.from_template(most_similar_prompt)

chain_final_res = (
    {
        "question" : itemgetter("question")
    }
    | RunnableLambda(prompt_router)
    | ChatOpenAI(temperature=0)
    | StrOutputParser()
)

print(chain_final_res.invoke({"question" : "What are differential equations and hessian ?"}))









