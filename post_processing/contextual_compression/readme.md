#### Problem : The information most relevant to a query may be buried in a document with a lot of irrelevant text. Passing that full document through your application might not make sense. So we ask LLM to compress the retrieved documents i.e we ask LLM to extract from retrieved documents, any text that is relevant to answer user query.


#### Input prompt to LLM for contextual compression using LLMChainExtractor : 

prompt_template = """Given the following question and context, extract any part of the context *AS IS* that is relevant to answer the question. If none of the context is relevant return {no_output_str}. 

Remember, *DO NOT* edit the extracted parts of the context.

> Question: {{question}}
> Context:
>>>
{{context}}
>>>
Extracted relevant parts:"""

#### We can also use LLMChainFilter

The LLMChainFilter is slightly simpler but more robust compressor that uses an LLM chain to decide which of the initially retrieved documents to filter out and which ones to return, without manipulating the document contents.

##### Input prompt for LLMChainFilter

prompt_template = """Given the following question and context, return YES if the context is relevant to the question and NO if it isn't.

> Question: {question}
> Context:
>>>
{context}
>>>
> Relevant (YES / NO):"""

