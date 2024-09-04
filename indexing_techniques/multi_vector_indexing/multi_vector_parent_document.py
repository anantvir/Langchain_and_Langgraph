"""
This is already implemented in parent_document_indexing folder.

Idea is to 

1. split each larger document into chunks 
2. Embedd those chunks and associate parent document ID with each chunk
3. During retrieval, we retrieve those chunks based on vector similarity. But during retrieval,
   instead of small chunks, parent documents containing those chunks are returned
4. These entire documents are then passed as context to LLM to answer user queries

"""