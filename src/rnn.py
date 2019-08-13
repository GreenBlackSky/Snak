"""Module contains Recurrent Neural Network class."""

from random import random as randfloat, randint, choice
from numpy import array, zeros, sum as np_sum
from numpy.random import uniform
from nn import NN
from config import SCHEME, MUTATION_CHANCE, MUTATION_POWER


class RNN(NN):
    """Implements Recurrent Neural Network."""

    def __init__(self, parent=None):
        """Initialize RNN."""
        self._hidden = [zeros(layer_size) for layer_size in SCHEME[1::]]
        self._hidden_in = None
        self._hidden_out = None
        NN.__init__(self, parent)

    def update(self):
        """Process signals from inputs to outputs."""
        for n, connections in enumerate(self._connections):
            self._neurons[n + 1] = self._neurons[n] @ connections
            self._neurons[n + 1] += self._hidden[n]*self._hidden_out[n]
            self._neurons[n + 1] = self._activation(self._neurons[n + 1])
            self._hidden[n] = self._neurons[n + 1]*self._hidden_in[n]

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
        NN._generate_connections(self)
        self._hidden_in = [uniform(-1, 1, layer) for layer in SCHEME[1:]]
        self._hidden_out = [uniform(-1, 1, layer) for layer in SCHEME[1:]]
