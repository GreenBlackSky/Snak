"""Module cntains basic NN class."""

from random import random as randfloat, choice
from numpy import array, zeros
from numpy.random import uniform
from config import SCHEME, ACTIVATION, MUTATION_CHANCE
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

        chance = MUTATION_CHANCE * sum(
            connections.size
            for connections in self._connections
        )

        for connections in self._connections:
            h, w = connections.shape
            for y in range(h):
                for x in range(w):
                    if randfloat() <= chance:
                        connections[y][x] = randfloat() * choice((-1, 1))

    def _generate_connections(self):
        self._connections = [
            uniform(-1, 1, (SCHEME[layer_n], SCHEME[layer_n + 1]))
            for layer_n in range(len(SCHEME) - 1)
        ]
