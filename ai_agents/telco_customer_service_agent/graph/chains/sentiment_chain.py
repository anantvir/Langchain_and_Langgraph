from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0)

prompt = """You are an expert at analyzing sentiment from human dialogues. Your task is to identify
customer sentiment from user query provided to you below. You should categorize it on the scale below
    0 - Calm: Customer asks questions but does not seem upset; is just seeking information.

    1 - Slightly Frustrated: Customer shows subtle signs of irritation but is still open to solutions.

    2 - Frustrated: Customer explicitly states being unhappy or irritated but is willing to discuss a solution.

    3 - Very Frustrated: Customer is clearly agitated, uses strong language, or mentions the problem repeatedly.

    4 - Extremely Frustrated: Customer is intensely unhappy, may raise their voice or use aggressive language.

    5 - Overwhelmed: Customer seems emotionally upset, says things like 'I can't take this anymore' or 'This is the worst experience ever.'

If you cannot identify the sentiment for some reason, simply respond with 'Unknown'

User Query : {query}
"""

sentiment_prompt = ChatPromptTemplate.from_template(prompt)

sentiment_chain = sentiment_prompt | llm

#print(sentiment_chain.invoke({"query" : "Why the hell is my internet not working ?"}))











