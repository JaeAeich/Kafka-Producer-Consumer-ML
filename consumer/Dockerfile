FROM python:3.11.8-slim

WORKDIR /app3

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]