"""
This file checks if the answer we have received from LLM is grounded in the retrieved documents
passed to LLM
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)

# Object type we want the LLM to return
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: bool = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )

# We tell LLM what type of object we want in response
structured_llm_grader = llm.with_structured_output(GradeHallucinations)

# Prompt to tell LLM to tell if generated response in grounded in retrieved docs
system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
     Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
    ]
)
# Hallucination detector chain
hallucination_grader_chain: RunnableSequence = hallucination_prompt | structured_llm_grader





















