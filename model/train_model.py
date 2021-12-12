from pv.layers import Dense, Input
from pv.loss import MeanSquaredError
from pv.optimizer import Adam
from pv.activation import ReLU
from pv.model import Model
import numpy as np
import matplotlib.pyplot as plt


def load_data(fileName):
    with open(fileName, "rb") as f:
        return np.load(f)


if __name__ == "__main__":
    path = "../datasets/train_data/"
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
        loss=MeanSquaredError(),
        optimizer=Adam()
    )
    model.train(
        X_train, y_train,
        test_data=(X_test, y_test),
        epochs=20, batch_size=X_train.shape[0]//1000
    )

    model.save_parameters("./backup/parameters.backup")

    model.save_model("./backup/model.backup")

    loss_his = model.get_loss()

    labelX = np.arange(1, 21)
    plt.plot(labelX, loss_his[:, 0], 'r')
    plt.plot(labelX, loss_his[:, 1], 'b')
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend(["Train loss", "Test loss"])
    plt.show()

