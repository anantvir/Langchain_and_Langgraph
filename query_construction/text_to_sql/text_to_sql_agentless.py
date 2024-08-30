"""
Chains (i.e., compositions of LangChain Runnables) support applications whose steps are predictable. We can create a simple chain that takes a question and does the following:

convert the question into a SQL query;
execute the query;
use the result to answer the original question.
There are scenarios not supported by this arrangement. For example, this system will execute a 
SQL query for any user input-- even "hello". Importantly, as we'll see below, some questions 
require more than one query to answer. We will address these scenarios in the Agents section.
"""

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

load_dotenv()

# Create DB engine for sqlite
db_engine = get_engine_for_chinook_db()
db = SQLDatabase(db_engine)

# Create LLM instance
llm = ChatOpenAI(temperature = 0)

# Predefined sql query chain from langchain
chain_write_query = create_sql_query_chain(llm, db)

# response returns a SQL query following sqlite dialect
#response = chain_write_query.invoke({"question": "How many employees are there"})

""" EXECUTE SQL QUERY"""
# db query execution tool from langchain_community package
execute_query = QuerySQLDataBaseTool(db=db)

# Chain to write and then execute query
chain_final_write_and_execute_query = chain_write_query | execute_query

#print(chain_final_write_and_execute_query.invoke({"question": "How many employees are there"}))


"""Answer question from result of executed SQL query"""

answer_prompt = PromptTemplate.from_template(
                """Given the following user question, corresponding SQL query, and SQL result, 
                answer the user question.

                Question: {question}
                SQL Query: {query}
                SQL Result: {result}
                Answer: """
                )

"""
Below we use RunnablePassthrough. It is normally used when we want to create a dictionary to use
at a later step in LCEL chain.
Since our prompt expects , question, query and result, we create a dict with these keys and corresponding values 
so that it could be fed to next step in chain i.e answer_prompt
"""
chain_answer_user_question = (
    RunnablePassthrough.assign(query=chain_write_query) 
                        .assign(result=itemgetter("query") | execute_query)
    | answer_prompt
    | llm
    | StrOutputParser()
)

print(chain_answer_user_question.invoke({"question": "How many employees are there"}))
