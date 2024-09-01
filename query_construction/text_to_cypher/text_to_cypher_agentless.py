from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI

load_dotenv()

graph = Neo4jGraph()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

graph.refresh_schema()

chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True, validate_cypher = True)

response = chain.invoke({"query": "What was the cast of the Casino?"})















