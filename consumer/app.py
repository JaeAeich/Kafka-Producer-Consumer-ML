import os

# from dotenv import load_dotenv
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

# load_dotenv()

MAX_MEMORY = 1000  # Maximum number of data points to store in memory

# configurations
# bootstrap_servers = os.environ.get("KAFKA_SERVER")
# topic = os.environ.get("KAFKA_TOPIC")
# delay = int(os.environ.get("CONSUMER_DELAY"))

bootstrap_servers = "localhost:29092"
topic = "test_topic"
delay = 5

print("#######################################")
print("bootstrap_servers: ", bootstrap_servers)
print("topic: ", topic)
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


import csv


# def append_to_csv(data_point, csv_file):
#     with open(csv_file, "a", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(data_point)


def append_to_csv(data_point, csv_file, max_data_points=1000):
    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_point)
    with open(csv_file, "r") as csvfile:
        lines = csvfile.readlines()
        if len(lines) > max_data_points:
            lines_to_keep = lines[-max_data_points:]
            with open(csv_file, "w", newline="") as csvfile:
                csvfile.writelines(lines_to_keep)


TIME_INTERVAL_OF_TRAIN = 100000
if __name__ == "__main__":
    i = 0
    model = Stock_Predictor("model.keras", 10)

    fig, ax = plt.subplots()
    (pred_line,) = ax.plot([], [], "r-", label="Predicted")
    (obs_line,) = ax.plot([], [], "b-", label="Actual")
    ax.legend()

    for message in consumer:
        i += 1
        i = i % TIME_INTERVAL_OF_TRAIN
        if i == 0:
            data_from_kafka = asyncio.run(consume_messages(model))
            model.save("model.keras")
        message = json.loads(message.value)
        if buffer.get(message["name"]) is None:
            buffer[message["name"]] = FifoBuffer(MAX_MEMORY)
        buffer[message["name"]].insert(message)
        if buffer[message["name"]].getlatest().shape[0] >= 10:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")
            # print("Current time:", formatted_time)
            temp = [
                message["name"],
                float(message["close"]),
                model.predict(buffer[message["name"]].getlatest())["close"].values[0],
                formatted_time,
            ]
            print(temp)
            append_to_csv(temp, temp[0])
