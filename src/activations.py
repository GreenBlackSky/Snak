"""Module contains some activations functions for NN."""

from numpy import maximum, minimum, exp, tanh as np_tanh


def relu(array):
    """Rectified Linear Unit activation function."""
    return maximum(array, 0)


def relu_leaky(array):
    """Leaky ReLU activation function."""
    return maximum(array, 0) + minimum(array, 0) * 0.01


def sigmoid(array):
    """Sigmoid activation function."""
    return 1/(1 + exp(-array))


def tanh(array):
    """Hyperbolic tan activation function."""
    return np_tanh(array)
