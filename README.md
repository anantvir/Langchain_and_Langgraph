# Langchain and Langraph

## RAG Landscape

### Query Translation (Multi Query Retrieval)

#### Source : https://python.langchain.com/v0.2/docs/concepts/

![Project screenshot](./screenshots/rag_landscape.png)


### 1. Multi Query Retrieval

![](./screenshots/multi_query_retrieval.png)

### 2. Query Translation - RAG Fusion Retrieval (Rerank retrieved documents based on RRF algorithm (Reciprocal Rank Fusion))

#### Source : https://arxiv.org/abs/2402.03367

![1](./screenshots/RAG_fusion.jpeg)

![2](./screenshots/RAG_fusion_2.png)

### 3. Query Translation (Query Decomposition)

#### Source : https://github.com/langchain-ai/rag-from-scratch/blob/main/rag_from_scratch_5_to_9.ipynb

##### Answer current question using retrieval and any previous Q & A stored in memory

![](./screenshots/decomposition.png)

### 4. Query Translation (Step Back Prompting)

#### Source : https://github.com/langchain-ai/rag-from-scratch/blob/main/rag_from_scratch_5_to_9.ipynb , https://arxiv.org/pdf/2310.06117


##### Ask model to step back and generate a question asking about more abstract/high level concepts. Pass that as additional context along with the context retrieved for actual customer query

![](./screenshots/stepback.png)

