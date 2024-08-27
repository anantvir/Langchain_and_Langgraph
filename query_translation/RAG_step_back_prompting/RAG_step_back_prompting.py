from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.load import dumps, loads
from chunking import retriever
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate



# Few shot examples to generate step back reasoning
examples = [
    {
        "input" : "Could the members of The Police perform lawful arrests?",
        "output" : "what can the members of The Police do?"
    },
    {
        "input": "Jan Sindel’s was born in what country?",
        "output": "what is Jan Sindel’s personal history?",
    }
]

# How one prompt looks like
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human" , "{input}"),
        ("ai" , "{output}")
    ])

# How few example interactions between human and ai look like
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt = example_prompt,
    examples = examples
)

prompt_step_back_question_generator = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert at world knowledge. Your task is to step back and paraphrase a question to a more generic step-back question, which is easier to answer. Here are a few examples:"),
        
        # Few shot examples
        few_shot_prompt,

        # New user question
        ("user", "{question}")
    ]
)

chain_step_back_question_generator = (
    prompt_step_back_question_generator
    | ChatOpenAI(temperature = 0)
    | StrOutputParser()
)

# user_question = "What is task decomposition for LLM agents?"

# res = chain_step_back_question_generator.invoke({"question" : user_question})
# print(res)








