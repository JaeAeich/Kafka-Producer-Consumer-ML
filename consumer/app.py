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
    return data  # {name, close, time, open, high, low}

# configurations
bootstrap_servers = os.environ.get("KAFKA_SERVER")
topic = os.environ.get("KAFKA_TOPIC")
delay = int(os.environ.get("CONSUMER_DELAY"))

print("#######################################")
print("bootstrap_servers: ", bootstrap_servers)
print("topic: ", topic)
# print("consumer delay: ", delay)
print("#######################################")

# Create Kafka consumer
consumer = KafkaConsumer(topic,
                         group_id='my-group',
                         bootstrap_servers=bootstrap_servers,
                         auto_offset_reset='earliest',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

consumer.subscribe(topic)

# Function to receive messages from Kafka
async def get_message_from_kafka():
    for message in consumer:
        yield message.value

# Function to receive messages from Kafka for 5 seconds
async def consume_messages():
    buffer = {}
    start_time = asyncio.get_event_loop().time()  # Get the current event loop's time
    
    # Consume messages for 5 seconds
    async for message in get_message_from_kafka():
        # buffer.append(message)
        message = json.loads(message)
        if(buffer.get(message['name']) is None):
            buffer[message['name']] = []
        buffer[message['name']].append(message)
        if asyncio.get_event_loop().time() - start_time >= delay:
            break
    print(buffer.keys())
    return buffer

if __name__ == "__main__":
    while True:
        # Consuming messages
        data_from_kafka = asyncio.run(consume_messages())
        model = "Model"  # TODO: load model when ready
        modelTrain(model, data_from_kafka)
        # print(modelPredict(model, data_from_kafka))  # TODO: send data to UI
