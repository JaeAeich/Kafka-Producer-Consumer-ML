import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.optimizers import Adam
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os


class Stock_Predictor:
    features = [
        "name",
        "date",
        "close",
        "high",
        "low",
        "open",
        "volume",
        "sma5",
        "sma10",
        "sma15",
        "sma20",
        "ema5",
        "ema10",
        "ema15",
        "ema20",
        "upperband",
        "middleband",
        "lowerband",
        "HT_TRENDLINE",
        "KAMA10",
        "KAMA20",
        "KAMA30",
        "SAR",
        "TRIMA5",
        "TRIMA10",
        "TRIMA20",
        "ADX5",
        "ADX10",
        "ADX20",
        "APO",
        "CCI5",
        "CCI10",
        "CCI15",
        "macd510",
        "macd520",
        "macd1020",
        "macd1520",
        "macd1226",
        "MFI",
        "MOM10",
        "MOM15",
        "MOM20",
        "ROC5",
        "ROC10",
        "ROC20",
        "PPO",
        "RSI14",
        "RSI8",
        "slowk",
        "slowd",
        "fastk",
        "fastd",
        "fastksr",
        "fastdsr",
        "ULTOSC",
        "WILLR",
        "ATR",
        "Trange",
        "TYPPRICE",
        "HT_DCPERIOD",
        "BETA",
    ]

    predict_features = ["close", "open", "high", "low", "volume"]
    seq_length = 10
    model = None
    input_shape = None
    label_encoder = LabelEncoder()

    def __init__(self, model_file=None, seq_length=10):
        self.input_shape = (seq_length, len(self.features))
        if model_file is not None and os.path.exists(model_file):
            self.model = load_model(model_file)
        else:
            self.model = self.create_model()
        self.seq_length = seq_length

    def create_model(self):
        model = Sequential()
        model.add(
            LSTM(
                units=50,
                return_sequences=True,
                input_shape=self.input_shape,
            )
        )
        model.add(LSTM(units=50))
        model.add(Dense(units=len(self.predict_features)))
        model.compile(optimizer=Adam(learning_rate=0.001), loss="mean_squared_error")
        return model

    def preprocessing(self, data):
        # data processing
        df = data.copy()
        df["date"] = pd.to_datetime(df["date"]).astype(int)
        df["name"] = self.label_encoder.fit_transform(df["name"])
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df[self.features])
        return df, scaled_data, scaler

    def create_sequences(self, data, seq_length):
        X = []
        y = []
        for i in range(len(data) - seq_length - 1):
            X.append(data[i : (i + seq_length)])
            y.append(data[i + seq_length])
        return np.array(X), np.array(y)

    def processing_pipleine(self):
        pass

    # data expecects queue object
    def train_model(self, data):

        test_loss_list = []
        train_loss_list = []
        data, scaled_data, scaler = self.preprocessing(data)
        X, y = self.create_sequences(scaled_data, self.seq_length)
        y = y[:, :5]
        train_size = int(len(X) * 0.8)
        test_size = len(X) - train_size
        X_train, X_test = X[0:train_size], X[train_size : len(X)]
        y_train, y_test = y[0:train_size], y[train_size : len(y)]
        self.model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1)
        # train_loss = self.model.evaluate(X_train, y_train, verbose=0)
        # test_loss = self.model.evaluate(X_test, y_test, verbose=0)
        # train_loss_list.append(train_loss)
        # test_loss_list.append(test_loss)
        # return train_loss_list, test_loss_list

    def prediction_pipeline(self, data):
        data["date"] = pd.to_datetime(data["date"]).astype(int)
        data["name"] = self.label_encoder.fit_transform(data["name"])
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data[self.features])
        scaled_data = scaled_data.reshape((1, self.seq_length, len(self.features)))
        return scaled_data, scaler

    def postprocessing_pipeline(self, predicted_data, scaler):
        temp = np.zeros((1, 61))
        temp[:, :5] = predicted_data
        predicted_data = temp
        predicted_data = scaler.inverse_transform(predicted_data)
        predicted_data = pd.DataFrame(predicted_data, columns=self.features)
        return predicted_data

    def predict(self, data):
        scaled_data, scaler = self.prediction_pipeline(data)
        predicted_data = self.model.predict(scaled_data)
        predicted_data = self.postprocessing_pipeline(predicted_data, scaler)
        return predicted_data[self.predict_features]


# commet
