### Self Query Construction 

#### Source : https://blog.langchain.dev/query-construction/

#### Query construction is taking a natural language query and converting it into the query language of the database you are interacting with.

Sometimes just comparing users embedded text queries to vectors is not enough. In additon to vector similarity search, we might need also need to generate
structured queries with filters to query our database. So we ask LLM to generate 2 things for us

1. Natural language query which we will compare with vectors (Semantic similarity)
2. Filters (which allow us to query our databases example vector db or SQL db etc.)

Example :

User Question : What's a movie after 1990 but before 2005 that's all about toys, and preferably is animated

LLM Output i.e Structured Query :
```json
{
    "query": "toys", # This will be used for Semantic similarity search
    "filter": "and(gt(\"year\", 1990), lt(\"year\", 2005), eq(\"genre\", \"animated\"))" # this will be used to query our vector store
}
```


![](../screenshots/self_querying.jpg)
