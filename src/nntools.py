"""Module contains some activations functions and BasicNN class."""

from random import random as randfloat, randint, choice
from numpy import array, zeros, sum as np_sum, \
    maximum, minimum, exp, tanh as np_tanh
from numpy.random import uniform
from config import SCHEME, ACTIVATION, MUTATION_CHANCE, MUTATION_POWER


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


activations = {
    'relu': relu,
    'relu_leaky': relu_leaky,
    'sigmoid': sigmoid,
    'tanh': tanh
}


class BasicNN(object):
    """Basic inheritable nuron network."""

    def __init__(self, parent=None):
        """Create NN."""
        self._neurons = [zeros(layer_size) for layer_size in SCHEME]
        self._connections = None

        self._activation = activations[ACTIVATION]

        if parent:
            self._inherit_connections(parent)
        else:
            self._generate_connections()

    def update(self):
        """Process signals from inputs to outputs."""
        for layer_n, connections in enumerate(self._connections):
            self._neurons[layer_n + 1] = self._neurons[layer_n] @ connections
            self._neurons[layer_n] = self._activation(self._neurons[layer_n])

    def get_connection(self, layer_n, start_node_n, end_node_n):
        """Get the weight of connection between twoneurons."""
        return self._connections[layer_n][start_node_n][end_node_n]

    def get_node_value(self, layer_n, node_n):
        """Pretty much self described."""
        return self._neurons[layer_n][node_n]

    def max_min(self):
        """Get pairs of `(max, min)` values for each layer."""
        return tuple(
            (max(layer), min(layer))
            for layer in self._neurons
        )

    def _inherit_connections(self, parent):
        self._connections = [array(layer) for layer in parent._connections]
        if randfloat() > MUTATION_CHANCE:
            return

        connections_n = sum(np_sum(layer) for layer in self._connections)
        mutations_n = int(randfloat() * connections_n * MUTATION_POWER)

        for _ in range(mutations_n):
            layer_n = randint(0, len(SCHEME) - 2)
            start_node_n = randint(0, SCHEME[layer_n] - 1)
            end_node_n = randint(0, SCHEME[layer_n + 1] - 1)
            val = randfloat() * choice((-1, 1))
            self._connections[layer_n][end_node_n][start_node_n] = val

    def _generate_connections(self):
        self._connections = [
            uniform(-1, 1, (SCHEME[layer_n], SCHEME[layer_n + 1]))
            for layer_n in range(len(SCHEME) - 1)
        ]


class RecurrentNN(BasicNN):

    def __init__(self, parent=None):
        self._hidden = [zeros(layer_size) for layer_size in SCHEME[1::]]
        self._hidden_in = None
        self._hidden_out = None
        BasicNN.__init__(self, parent)

    def update(self):
        """Process signals from inputs to outputs."""
        for prev_n, connections in enumerate(self._connections):
            n = prev_n + 1
            self._neurons[n] = self._neurons[prev_n] @ connections
            self._neurons[n] += self._hidden[n]*self._hidden_out[n]
            self._neurons[prev_n] = self._activation(self._neurons[prev_n])
            self._hidden[n] = self._neurons[n]*self._hidden_in[n]

    def _inherit_connections(self, parent):
        self._connections = [array(layer) for layer in parent._connections]
        self._hidden_in = [array(layer) for layer in parent._hidden_in]
        self._hidden_out = [array(layer) for layer in parent._hidden_out]

        if randfloat() > MUTATION_CHANCE:
            return

        connections_n = sum(np_sum(layer) for layer in self._connections)
        hidden_inputs_n = sum(np_sum(layer) for layer in self._hidden_in)
        hidden_outputs_n = sum(np_sum(layer) for layer in self._hidden_out)
        full_connections_n = connections_n+hidden_inputs_n+hidden_outputs_n
        mutations_n = int(randfloat() * full_connections_n * MUTATION_POWER)

        for _ in range(mutations_n):
            layer_n = randint(0, len(SCHEME) - 2)
            start_node_n = randint(0, SCHEME[layer_n] - 1)
            val = randfloat() * choice((-1, 1))
            dice = randint(0, full_connections_n)

            if dice <= connections_n:
                end_node_n = randint(0, SCHEME[layer_n + 1] - 1)
                self._connections[layer_n][end_node_n][start_node_n] = val
            elif connections_n < dice <= connections_n + hidden_inputs_n:
                self._hidden_in[layer_n][start_node_n] = val
            else:
                self._hidden_out[layer_n][start_node_n] = val

    def _generate_connections(self):
        BasicNN._generate_connections(self)
        self._hidden_in = [uniform(-1, 1, layer) for layer in SCHEME[1:]]
        self._hidden_out = [uniform(-1, 1, layer) for layer in SCHEME[1:]]
