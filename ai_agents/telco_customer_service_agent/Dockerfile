FROM langchain/langgraph-api:3.11



ADD . /deps/telco_customer_Service_agent

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"agent": "/deps/adaptive_rag/graph/graph.py:entry_flow"}'

WORKDIR /deps/telco_customer_Service_agent