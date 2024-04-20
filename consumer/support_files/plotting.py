import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation


class RealTimePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        (self.pred_line,) = self.ax.plot([], [], "r-", label="Predicted")
        (self.obs_line,) = self.ax.plot([], [], "b-", label="Actual")
        self.ax.legend()
        self.all_data = []

    def update_graph(self):
        pred_data = [
            (x, y) for data_type, x, y in self.all_data if data_type == "prediction"
        ]
        obs_data = [
            (x, y) for data_type, x, y in self.all_data if data_type == "observation"
        ]

        if pred_data:
            self.pred_line.set_data(*zip(*pred_data))
        if obs_data:
            self.obs_line.set_data(*zip(*obs_data))

        # Adjust plot limits if necessary
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()  # Force redraw of the plot

    def add_data_point(self, data_type, x, y):
        self.all_data.append((data_type, x, y))
        self.update_graph()

    def update(self, frame):
        # If you want to update data dynamically, you can implement your logic here
        pass

    def start_animation(self):
        ani = FuncAnimation(self.fig, self.update, frames=range(100), repeat=False)
        plt.show()


# Example usage:
plot = RealTimePlot()
plot.start_animation()
for i in range(1, 1000):
    plot.add_data_point("prediction", i + 1, random.randint(1, 10) * i)
    plot.add_data_point("observation", i, random.randint(1, 10) * i)
    plot.add_data_point("prediction", i + 1, random.randint(1, 10) * i)
    plot.add_data_point("observation", i, random.randint(1, 10) * i)
    plt.show()
