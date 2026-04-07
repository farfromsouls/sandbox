FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install mysql-connector-python

WORKDIR .

COPY main.py .
COPY sql_script.txt .

CMD ["python", "main.py"]