FROM langchain/langgraph-api:3.11



ADD . /deps/adaptive_rag

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"agent": "/deps/adaptive_rag/graph/graph.py:app"}'

WORKDIR /deps/adaptive_rag