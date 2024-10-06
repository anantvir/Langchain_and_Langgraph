FROM langchain/langgraph-api:3.12



ADD . /deps/telco_customer_service_agent

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"agent": "/deps/graph/graph.py:entry_flow"}'

WORKDIR /deps/telco_customer_service_agent