"""
Vanilla text-to-sql system will always convert user question to a sql query and try to execute it.
Example, if a user says "Hello", system will try to convert it to a SQL query which is 
obviously invalid. How to solve this problem ? Make your system smarter. Reflect or think about 
what the user is asking and how to answer it. Keep having normal english conversation and if
you feel that response to users question requires external data, then convert text-to-sql
and retrieve query results

Source : https://python.langchain.com/v0.2/docs/tutorials/sql_qa/
"""
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from get_db_engine import get_engine_for_chinook_db
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()


# Create DB engine for sqlite
db_engine = get_engine_for_chinook_db()
db = SQLDatabase(db_engine)

# Create LLM instance
llm = ChatOpenAI(temperature = 0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# List of tools available for LLM
tools = toolkit.get_tools()

SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

Do NOT skip both of the following steps :

1. To start you should ALWAYS look at the tables in the database to see what you can query.

2. ALWAYS look at the schema of those tables to get better understanding of the data inside those tables.

Do NOT skip both of these steps.

Then you should query the schema of the most relevant tables."""

system_message = SystemMessage(content=SQL_PREFIX)

# Use pre-built ReAct agent from Langgraph
agent_executor = create_react_agent(llm, tools, messages_modifier=system_message)


print(agent_executor.invoke({"messages": [HumanMessage(content="Which country's customers spent the most?")]}))













