#### Problem : It does not make sense to feed all of retrieved documents to LLM. Only feed to LLM the content that is most relevant to user query. We do that through re-ranking LLMs like Cohere rerank


#### What happens under the hood : 

1. Use a base retriever to retrieve documents based on query (Vector similarity)

2. Send those retrived documents to Cohere rerank LLM through ContextualCompressionRetriever.

3. We get back list of reranked documents from Cohere rerank LLM.

4. Feed these reranked documents as context along with user query to LLM to answer user questions
