import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import random


def update_graph(data_points, pred_line, obs_line):
    pred_data = [(x, y) for data_type, x, y in data_points if data_type == "prediction"]
    obs_data = [(x, y) for data_type, x, y in data_points if data_type == "observation"]

    pred_line.set_data(*zip(*pred_data))
    obs_line.set_data(*zip(*obs_data))

    # Adjust plot limits if necessary
    ax.relim()
    ax.autoscale_view()


def generate_data():
    all_data = []  # Accumulate all data points
    for i in range(1, 1000):
        data_points = [
            (
                "prediction",
                i + 1,
                random.randint(1, 10) * i,
            ),
            ("observation", i, random.randint(1, 10) * i),
            ("prediction", i + 1, random.randint(1, 10) * i),
            ("observation", i, random.randint(1, 10) * i),
        ]
        all_data.extend(data_points)
        yield all_data
        time.sleep(1)


fig, ax = plt.subplots()
(pred_line,) = ax.plot([], [], "r-", label="Predicted")
(obs_line,) = ax.plot([], [], "b-", label="Actual")
ax.legend()


def update(frame):
    data_points = next(data_generator)
    update_graph(data_points, pred_line, obs_line)


data_generator = generate_data()
ani = FuncAnimation(fig, update, frames=range(100), repeat=False)
plt.show()
