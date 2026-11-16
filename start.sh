#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
export LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false
exec .venv/bin/python -m streamlit run app.py --server.address=127.0.0.1 --server.port="${BRAIN_PORT:-8780}"
