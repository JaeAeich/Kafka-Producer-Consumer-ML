# KAFKA Consumer Producer Stock predictor (ML)
This project is a simple example of how to use Kafka to create a producer and consumer to predict stock prices using machine learning.

## Requirements
- Python 3.11
- Docker
- Docker-compose

## How to run
1. Clone the repository
2. Run the following command to start the Kafka cluster
```bash
docker-compose up
```
3. Add .env files, check sample.env files for default values.
4. Install producer deps and run the producer
```bash
cd producer
pip install -r requirements.txt
python app.py
```
5. Install consumer deps and run the consumer
```bash
cd consumer
pip install -r requirements.txt
python consumer.py
```
