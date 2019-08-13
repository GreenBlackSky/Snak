"""Module cntains basic NN class."""

from random import random as randfloat, randint, choice
from numpy import array, zeros, sum as np_sum
from numpy.random import uniform
from config import SCHEME, ACTIVATION, MUTATION_CHANCE, MUTATION_POWER
import activations


class NN(object):
    """Basic inheritable nuron network."""

    def __init__(self, parent=None):
        """Create NN."""
        self._neurons = [zeros(layer_size) for layer_size in SCHEME]
        self._connections = None

        self._activation = getattr(activations, ACTIVATION)

        if parent:
            self._inherit_connections(parent)
        else:
            self._generate_connections()

    def update(self):
        """Process signals from inputs to outputs."""
        for n, connections in enumerate(self._connections):
            self._neurons[n + 1] = self._neurons[n] @ connections
            self._neurons[n + 1] = self._activation(self._neurons[n + 1])

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
