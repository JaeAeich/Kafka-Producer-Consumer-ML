import os

from dotenv import load_dotenv
from kafka import KafkaConsumer
import asyncio
import json
from support_files.fifo import FifoBuffer
import pandas as pd
from support_files.model import Stock_Predictor
import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

load_dotenv()

# configurations
max_memory = int(os.environ.get("MAX_MEMORY"))  # Maximum memory to store the data
time_interval = max_memory*int(os.environ.get('NUMBER_OF_PRODUCER'))  # Time interval to train the model
bootstrap_servers = os.environ.get("KAFKA_SERVER")
topic = os.environ.get("KAFKA_TOPIC")

print("#######################################")
print("bootstrap_servers: ", bootstrap_servers)
print("topic: ", topic)
print("max_memory: ", max_memory)
print("time_interval: ", time_interval)
print("#######################################")

buffer_backup = "buffer_backup.json"

# Create Kafka consumer
consumer = KafkaConsumer(
    topic,
    group_id="my-group",
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

consumer.subscribe(topic)
buffer = {}


async def consume_messages(model):
    l = []
    for i in buffer.values():
        l.append(i.getall())
    if l is None or len(l) == 0:
        return
    dfs = pd.concat(l, ignore_index=True)
    model.train_model(dfs)


if __name__ == "__main__":
    i = 0
    model = Stock_Predictor("model.keras", 10)

    fig, ax = plt.subplots()
    (pred_line,) = ax.plot([], [], "r-", label="Predicted")
    (obs_line,) = ax.plot([], [], "b-", label="Actual")
    ax.legend()

    for message in consumer:
        i += 1
        i = i % time_interval
        if i == 0:
            data_from_kafka = asyncio.run(consume_messages(model))
            model.save('model.keras')
        message = json.loads(message.value)
        if buffer.get(message["name"]) is None:
            buffer[message["name"]] = FifoBuffer(max_memory)
        buffer[message["name"]].insert(message)
        if buffer[message["name"]].getlatest().shape[0] >= 10:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            print("Current time:", formatted_time)
            print(
                message["name"],
                message["close"],
                model.predict(buffer[message["name"]].getlatest())["close"],
            )
