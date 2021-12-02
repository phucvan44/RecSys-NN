from pv.layers import Dense, Input
from pv.loss import MeanSquaredError
from pv.optimizer import Adam
from pv.activation import ReLU
from pv.model import Model
import numpy as np
import pandas as pd


def load_data(fileName):
    with open(fileName, "rb") as f:
        return np.load(f)


if __name__ == "__main__":
    path = "./datasets/"
    X_train = load_data(path+"TrainingFeatures.npy")
    y_train = load_data(path+"TrainingLabels.npy")
    X_test = load_data(path+"TestingFeatures.npy")
    y_test = load_data(path+"TestingLabels.npy")

    y_train = y_train.reshape(len(y_train), 1)
    y_test = y_test.reshape(len(y_test), 1)

    model = Model()
    model.add(Dense(X_train.shape[1], 128))
    model.add(ReLU())
    model.add(Dense(128, 32))
    model.add(ReLU())
    model.add(Dense(32, 1))

    model.compile(
        loss = MeanSquaredError(),
        optimizer = Adam()
    )
    model.train(
        X_train, y_train,
        validation_data = (X_test, y_test),
        epochs=2, batch_size= 900
    )

    predict = model.predictions(X_test)

    y_test = y_test.reshape(1, -1)[0]
    predict = predict.reshape(1, -1)[0]

    df = pd.DataFrame(columns=["True Lables", "Predict Lables"])
    df["True Lables"] = y_test
    df["Predict Lables"] = predict
    print(df)

