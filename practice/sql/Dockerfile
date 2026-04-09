FROM python:3.11-slim

RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

RUN pip install mysql-connector-python sqlparse

WORKDIR /app

COPY . .

CMD ["python", "main.py"]