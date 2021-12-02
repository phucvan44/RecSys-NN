import numpy as np


class Input:


    def forward(self, inputs):
        self.output = inputs


class Dense:


    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01*np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))


    def forward(self, inputs):
        self.inputs = inputs
        self.output = (inputs@self.weights) + self.biases


    def backward(self, dvalues):
        self.dweights = self.inputs.T@dvalues
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)

        self.dinputs = dvalues@self.weights.T


    def get_parameters(self):
        return self.weights, self.biases


    def set_parameters(self, weights, biases):
        self.weights = weights
        self.biases = biases