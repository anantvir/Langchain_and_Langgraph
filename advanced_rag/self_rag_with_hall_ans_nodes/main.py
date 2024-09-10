"""
Credits :

1. https://github.com/mistralai/cookbook/tree/main/third_party/langchain
2. Udemy : Learn LangGraph by building FAST a real world generative ai LLM Agents (Python) by Eden Marco
"""
from graph.graph import app
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    print("Starting Self RAG ...")
    print(app.invoke(input={"question" : "what is agent memory ?"}))









