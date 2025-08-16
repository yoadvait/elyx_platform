FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501

ENV USE_MOCK_RESPONSES=1

CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.address", "0.0.0.0"]

