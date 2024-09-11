## Adaptive RAG

Adaptive RAG introduces a form of Query Routing. We have already discussed query routing in this repository. We have already implemented 1. Logical Routing 2. Semantic Routing

ChatGPT says : The model is called "Adaptive" because it dynamically adjusts its retrieval strategy based on the complexity of the incoming queries. Unlike traditional one-size-fits-all approaches, Adaptive-RAG uses a specialized classifier to predict the complexity of each question. Depending on whether a query is simple or complex, the system selects the most appropriate method—from the simplest no-retrieval approach to more sophisticated, multi-step retrieval strategies. This adaptability helps conserve computational resources while improving the quality and efficiency of responses across different query types​

#### Main Idea :

1. Retrieve the documents
2. Ask LLM to grade the retrieved documents and tell us which documents are relevent to user question. We filter out irrelevant docs **(We Correct our retrieval)**
3. For relevant docs, we feeed them as context to LLM to generate final answer
4. If there are some irrelevant docs, then we trigger web search to get additional context that is fed to LLM as context along with relevant docs
5. After final answer has been generated, we check for hallucination. We ask LLM to check if generated response is grounded in provided context. If yes then we move to next step where check if generated answer actually answers users query. If LLM says no that means our model is hallucinating, so we generate response again.
6. If no hallucination, then we ask LLM to check if generated response actually answers user question. If yes, then we end the flow. If not, then flow again goes to web_search node and then -> hallucination check -> answer question check and repeat
   

#### Self RAG Graph from Langgraph

![](./self_rag_multinode_graph.png)

#### Self RAG Flow

![](./crag.png)




