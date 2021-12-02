import numpy as np
from .layers import Input


class Model:


    def __init__(self):
        self.layers = []


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


    def print_progress(self, index, total, epoch, epochs, loss_train):
        epoch = str(epoch).zfill(len(str(epochs)))
        percent = ("{0:.2f}").format(100 * ((index + 1) / total))
        filledLength = 50 * index // total
        bar = '=' * filledLength + '-' * (50 - filledLength - 1)
        print('\rEpoch %s/%s: |%s| %s%%  Loss: %s' % (epoch, epochs, bar, percent, loss_train), end='\r')
        if index == total - 1:
            print()


    def train(self, X, y, epochs=1, batch_size=None, validation_data=None):
        train_steps = 1

        if validation_data != None:
            validation_steps = 1
            X_test, y_test = validation_data

        if batch_size != None:
            train_steps = len(X)//batch_size

            if train_steps*batch_size < len(X):
                train_steps += 1

            if validation_data != None:
                validation_steps = len(X_test)

                if validation_steps*batch_size < len(X_test):
                    validation_steps += 1

        for epoch in range(1, epochs+1):

            self.loss.reset_accumulate()

            loss = 0

            for step in range(train_steps):
                if batch_size != None:
                    batch_X = X
                    batch_y = y
                else:
                    limit_start = step*batch_size
                    limit_end = (step+1)*batch_size
                    batch_X = X[limit_start:limit_end]
                    batch_y = y[limit_start:limit_end]

                output = self.forward(batch_X)
                predictions = output

                data_loss = self.loss.calculate(output, batch_y)
                loss += data_loss

                self.backward(output, batch_y)

                self.optimizer.pre_update_params()

                self.print_progress(step, train_steps, epoch, epochs, loss)

                for layer in self.trainable_layers:
                    self.optimizer.update_params(layer)
                self.optimizer.post_update_params()
        print()


    def predictions(self, X):
        output = self.forward(X)
        return output


    def forward(self, X):
        self.input_layer.forward(X)

        for layer in self.layers:
            layer.forward(layer.pre.output)

        return layer.output


    def backward(self, output, y):
        self.loss.backward(output, y)

        for layer in reversed(self.layers):
            layer.backward(layer.suf.dinputs)