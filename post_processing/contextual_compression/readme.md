#### Problem : The information most relevant to a query may be buried in a document with a lot of irrelevant text. Passing that full document through your application might not make sense. So we ask LLM to compress the retrieved documents i.e we ask LLM to extract from retrieved documents, any text that is relevant to answer user query.


#### Input prompt to LLM for contextual compression : 

prompt_template = """Given the following question and context, extract any part of the context *AS IS* that is relevant to answer the question. If none of the context is relevant return {no_output_str}. 

Remember, *DO NOT* edit the extracted parts of the context.

> Question: {{question}}
> Context:
>>>
{{context}}
>>>
Extracted relevant parts:"""
