FROM python:3.14-slim
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock
COPY brain.py app.py ./
COPY .streamlit .streamlit
ENV BRAIN_DB=/data/brain.sqlite3 LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false
# Host networking keeps Streamlit bound to the host loopback on Linux.
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=127.0.0.1", "--server.port=8780"]
