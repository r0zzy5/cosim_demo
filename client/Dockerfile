FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/* .

CMD ["python3","client.py"]