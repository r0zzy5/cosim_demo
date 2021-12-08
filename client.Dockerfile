FROM python:3.10-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY client.py client.py
COPY boid.py boid.py

CMD ["python3","client.py"]