import numpy as np
import pickle
from copy import deepcopy
from .layers import Input


class Model:


    def __init__(self):
        self.layers = []
        self.loss_his = []


    def add(self, layer):
        self.layers.append(layer)


    def compile(self, loss=None, optimizer=None):
        if loss != None:
            self.loss = loss

        if optimizer != None:
            self.optimizer = optimizer

        self.input_layer = Input()

        layer_count = len(self.layers)

        self.trainable_layers = []

        for i in range(layer_count):
            """
                pre: prefix node 
                suf: suffix node
            """
            if i == 0:
                self.layers[i].pre = self.input_layer
                self.layers[i].suf = self.layers[i+1]
            elif i == layer_count - 1:
                self.layers[i].pre = self.layers[i-1]
                self.layers[i].suf = self.loss
                self.output_layer_activation = self.layers[i]
            else:
                self.layers[i].pre = self.layers[i-1]
                self.layers[i].suf = self.layers[i+1]

            # Append layer Dense to trainable_layers
            if hasattr(self.layers[i], "weights"):
                self.trainable_layers.append(self.layers[i])

        self.loss.remember_trainable_layers(self.trainable_layers)


    def print_progress(self, index, total, epoch, epochs):
        epoch = str(epoch).zfill(len(str(epochs)))
        percent = ("{0:.2f}").format(100 * ((index) / total))
        filledLength = 50 * index // total
        bar = '=' * filledLength + '-' * (50 - filledLength - 1)
        print('\rEpoch %s/%s: |%s| %s%%' % (epoch, epochs, bar, percent), end='\r')
        if index == total:
            print()


    def train(self, X, y, epochs=1, batch_size=0, test_data=None):
        train_steps = 1

        if test_data != None:
            test_steps = 1
            X_test, y_test = test_data

        if batch_size != 0:
            train_steps = len(X)//batch_size

            if train_steps*batch_size < len(X):
                train_steps += 1

            if test_data != None:
                test_steps = len(X_test)

                if test_steps*batch_size < len(X_test):
                    test_steps += 1

        for epoch in range(1, epochs+1):

            self.loss.reset_accumulate()

            for step in range(train_steps):
                self.print_progress(step+1, train_steps, epoch, epochs)
                if batch_size == 0:
                    batch_X = X
                    batch_y = y
                else:
                    limit_start = step*batch_size
                    limit_end = (step+1)*batch_size
                    batch_X = X[limit_start:limit_end]
                    batch_y = y[limit_start:limit_end]

                output = self.forward(batch_X)

                data_loss = self.loss.calculate(output, batch_y, include_regularization=True)

                self.backward(output, batch_y)

                self.optimizer.pre_update_params()

                for layer in self.trainable_layers:
                    self.optimizer.update_params(layer)
                self.optimizer.post_update_params()

            train_loss = self.loss.calculate_accumulate()

            # Get loss values in test set
            self.loss.reset_accumulate()

            output = self.forward(X_test)

            loss = self.loss.calculate(output, y_test)

            test_loss = self.loss.calculate_accumulate()

            self.loss_his.append([train_loss, test_loss])
            print("Epochs {0}/{1}, Train loss: {2}, Test loss: {3}".format(epoch, epochs, train_loss, test_loss))


    def predictions(self, X, batch_size=0):

        prediction_steps = 1
        if batch_size != 0:
            prediction_steps = len(X)//batch_size

            if prediction_steps*batch_size < len(X):
                prediction_steps += 1

        output = []
        for step in range(prediction_steps):
            self.print_progress(step+1, prediction_steps, 1, 1)
            if batch_size == 0:
                batch_X = X
            else:
                limit_start = step*batch_size
                limit_end = (step+1)*batch_size
                batch_X = X[limit_start:limit_end]
            batch_output = self.forward(batch_X)

            output.append(batch_output)

        return np.vstack(output)


    def get_loss(self):
        return np.array(self.loss_his)


    def forward(self, X):
        self.input_layer.forward(X)

        for layer in self.layers:
            layer.forward(layer.pre.output)

        return layer.output


    def backward(self, output, y):
        self.loss.backward(output, y)

        for layer in reversed(self.layers):
            layer.backward(layer.suf.dinputs)


    def get_parameters(self):
        parameters = []

        for layer in self.trainable_layers:
            parameters.append(layer.get_parameters())

        return parameters


    def set_parameters(self, parameters):
        for parameter, layer in zip(parameters, self.trainable_layers):
            layer.set_parameters(*parameter)


    def save_parameters(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.get_parameters(), f)
            print("[+] Parameters saving on", path)


    def load_parameters(self, path):
        with open(path, "rb") as f:
            print("[+] Loading parameters from", path)
            self.set_parameters(pickle.load(f))


    def save_model(self, path):
        model = deepcopy(self)

        model.loss.reset_accumulate()

        model.input_layer.__dict__.pop('output', None)
        model.loss.__dict__.pop('dinputs', None)

        for layer in model.layers:
            for prop in ["inputs", "output", "dinputs", "dweights", "dbiases"]:
                layer.__dict__.pop(prop, None)

        with open(path, "wb") as f:
            pickle.dump(model, f)
            print("[+] Model saving on", path)


    @staticmethod
    def load_model(path):
        with open(path, "rb") as f:
            print("[+] Loading model from", path)
            model = pickle.load(f)

        return model