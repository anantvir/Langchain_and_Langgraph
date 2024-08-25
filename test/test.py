from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
output_parser = StrOutputParser()

prompt_template = PromptTemplate.from_template("Tell me about {input} in 50 words")


chain = prompt_template | llm | output_parser

# for chunk in chain.stream({"input" : "Bhagat Singh"}):
#     print(chunk, end="", flush=True)











