import os
from dotenv import load_dotenv
from kafka import KafkaConsumer
import asyncio
import json

# Load environment variables
load_dotenv()

def modelTrain(model, data):
    pass

def modelPredict(model, data):
    return data # {name, close, time, open, high, low}

# configurations
bootstrap_servers = os.environ.get("KAFKA_SERVER")
topic = os.environ.get("KAFKA_TOPIC")
delay = int(os.environ.get("CONSUMER_DELAY"))

# Create Kafka consumer
consumer = KafkaConsumer(topic,
                         group_id='my-group',
                         bootstrap_servers=bootstrap_servers,
                         auto_offset_reset='earliest',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Function to receive messages from Kafka
async def get_message_from_kafka():
    for message in consumer:
        print(message.value)

# Function to receive messages from Kafka
async def consume_messages():
    buffer = []
    start_time = asyncio.get_event_loop().time()  # Get the current event loop's time
    
    # Consume messages for 5 seconds
    while asyncio.get_event_loop().time() - start_time < delay:
        message = await get_message_from_kafka()
        buffer.append(message)
    
    return buffer

if __name__ == "__main__":
    while(True):
        # Consuming messages
        data_from_kafka = asyncio.run(consume_messages())
        model = "Model"  # TODO: load model when ready
        modelTrain(model, data_from_kafka)
        print(modelPredict(model, data_from_kafka))  # TODO: send data to UI
