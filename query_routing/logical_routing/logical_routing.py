"""
Routing : At a high level, it means to which database should we route the user query ?
Logical routing can use an LLM to 
reason about the query and choose which datastore is most appropriate."""

"""
RunnableLambda is essentially a way to inject custom logic into the chain. 
It allows you to define a function that takes some input (like the result of a previous step) and 
returns a new runnable (another chain or sub-chain) based on that input. 
This makes the chain dynamic and adaptive to the specific input it's processing.
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from operator import itemgetter

load_dotenv()

# Ask LLM to classify the question as being about `LangChain`, `OpenAI`, or `Other`
chain_classification = (
    PromptTemplate.from_template(
        """Given the user question below, classify it as either being about `LangChain`, `OpenAI`, or `Other`.

            Do not respond with more than one word.

            <question>
            {question}
            </question>

            Classification:"""
                )
                | ChatAnthropic(model='claude-3-opus-20240229')
                | StrOutputParser()
)

# Chain to answer any question with classification 'Langchain'
langchain_chain = PromptTemplate.from_template(
            """You are an expert in langchain. \
        Always answer questions starting with "As Harrison Chase told me". \
        Respond to the following question:

        Question: {question}
        Answer:"""
        ) | ChatOpenAI(model="gpt-4o-mini")

# Chain to answer any question with classification 'Anthropic'
anthropic_chain = PromptTemplate.from_template(
            """You are an expert in anthropic. \
        Always answer questions starting with "As Dario Amodei told me". \
        Respond to the following question:

        Question: {question}
        Answer:"""
        ) | ChatAnthropic(model='claude-3-opus-20240229')

# Chain to answer any question with classification 'Other'
general_chain = PromptTemplate.from_template(
            """Respond to the following question:

            Question: {question}
            Answer:"""
            ) | ChatAnthropic(model_name="claude-3-haiku-20240307")


# Use a custom function as RunnableLambda. Wrap this function in RunnableLambda to implement
def route(info):
    if "anthropic" in info["topic"].lower(): 
        return anthropic_chain
    elif "langchain" in info["topic"].lower():
        return langchain_chain
    else:
        return general_chain

"""
How Data Flows in a Composite Runnable:

In LangChain, when you define a composite runnable like {"topic": chain_classification, "question": lambda x: x["question"]}, 
and then invoke it with some input, LangChain automatically handles how the input data is passed 
to each runnable in the dictionary.
"""
chain_final_res = (
    {
        "topic" : chain_classification,
        "question" : itemgetter("question")
    }
    | RunnableLambda(route)
)

res = chain_final_res.invoke({"question" : "how do I use Anthropic?"})
print(res)








