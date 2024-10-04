from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class CategorizeQuery(BaseModel):
    category : str = Field(description = "category this query belongs to. Can be one of 'Faq', 'Phone', 'Internet', 'Iot'")

llm = ChatOpenAI(temperature=0)

query_categorize_chain = llm.with_structured_output(CategorizeQuery)

system = """ You are an expert customer care representative working for a large telecom company. You are
        expert at categorizing customer queries into different categories. Given a customer query below :

        Customer Query : {query}

        Classify this query into one of the four categories (faq, phone, internet, iot) described below :
        1. Faq
        Meaning = This means if the query is a generic question about the companys products, services, plans etc. but this query is not about any problem with the phone, internet or any home automation devices (Iot devices).

        2. Phone 
        Meaning = This means if the query is about a problem related to customers phone plan. Examples could be but not limited to issues with phone service quality, phone network quality, call dropping, if customer wants to upgrade plans etc. This is basically anything that has to do with customers phone plan and everything around it.

        3. Internet
        Meaning = This means if the query is about customer's home internet plan. Examples could be but not limited to problems with internet speed, internet not working, internet down, internet modem issues. This category includes anything that has to do with customers home internet plan or subscription.

        4. Iot 
        Meaning = This means if query is about customer's home automation products like thermostats, security cameras, smart speakers, smart displays, connected vehicle products that provide internet in vehicle. This category includes any Iot type device used in home automation.

        Make sure you categorize into one of the four categories i.e "Faq", "phone", "internet", "iot". Do not return any other category apart from these. Only return one of "Faq", "phone", "internet", "iot" as one word and nothing else. 
"""

categorization_prompt = ChatPromptTemplate.from_template(system)

categorization_chain = categorization_prompt | llm

#print(categorization_chain.invoke({"query" : "Is iphone 16 available yet ?"}).content)












