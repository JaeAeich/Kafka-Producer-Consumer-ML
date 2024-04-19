import os
from dotenv import load_dotenv
import csv
from kafka import KafkaProducer
import json
import time

# Load environment variables
load_dotenv()

# configurations
bootstrap_servers = os.environ.get("KAFKA_SERVER")
topic = os.environ.get("KAFKA_TOPIC")
csv_file_path = os.environ.get("CSV_FILE_PATH")
delay = int(os.environ.get("PRODUCER_DELAY"))

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Function to send a message to Kafka
def send_message(message):
    producer.send(topic, value=message)
    producer.flush()

# Function to read CSV file and send its content to Kafka
def send_csv_to_kafka(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = json.dumps(row)
            print("sending data to kafka: ", data)
            send_message(data)
            time.sleep(delay)

if __name__ == "__main__":
    time.sleep(5)
    send_csv_to_kafka(csv_file_path)
