from collections import deque
import pandas as pd


class FifoBuffer:
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    def insert(self, data_point):
        self.buffer.append(data_point)

    def getlatest(self):
        return pd.DataFrame((self.buffer)).tail(10)

    def getall(self):
        return pd.DataFrame((self.buffer))

    def dump_buffer_as_dataframe(self):
        return pd.DataFrame(self.buffer)
