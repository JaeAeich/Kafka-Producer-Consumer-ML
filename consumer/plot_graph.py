import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import pandas as pd
import sys
import numpy as np


if len(sys.argv) != 2:
    print("Specify share file name")
    sys.exit(1)

csv_file = sys.argv[1] + ".csv"
plt.figure(sys.argv[1])


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def animate(i):
    data = pd.read_csv(csv_file)
    y = data.iloc[:, 2].tolist()
    y1 = data.iloc[:, 1].tolist()
    x = range(len(y))
    print(
        "Mean absolute percentage error ",
        "{:.3f}".format(mean_absolute_percentage_error(np.array(y), np.array(y1))),
    )
    print(
        "Mean square error ",
        "{:.3f}".format(mean_squared_error(np.array(y), np.array(y1))),
    )
    plt.cla()
    plt.plot(x, y, color="orange", label="Real price")
    plt.plot(x, y1, label="Predicted price")
    plt.legend()


ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.legend()
plt.show()
