import numpy as np


class Loss:


    def remember_trainable_layers(self, trainable_layers):
        self.trainable_layers = trainable_layers


    def calculate(self, output, y, include_regularization=False):
        sample_loss = self.forward(output, y)
        loss_values = np.mean(sample_loss)

        self.accumulate_sum += np.sum(sample_loss)
        self.accumulate_count += len(sample_loss)

        if not include_regularization:
            return loss_values

        return loss_values


    def calculate_accumulate(self, include_regularization=False):
        loss_values = self.accumulate_sum/self.accumulate_count

        if not include_regularization:
            return loss_values

        return loss_values


    def reset_accumulate(self):
        self.accumulate_sum = 0
        self.accumulate_count = 0


class MeanSquaredError(Loss):


    def forward(self, y_pred, y_true):
        loss_values = np.mean((y_true - y_pred)**2, axis=1)
        return loss_values


    def backward(self, dvalues, y_true):
        samples = len(dvalues)
        output = len(dvalues[0])

        self.dinputs = -2*(y_true-dvalues)/output
        self.dinputs = self.dinputs/samples