"""Module contains Recurrent Neural Network class."""

from random import random as randfloat, choice
from numpy import array, zeros
from numpy.random import uniform
from nn import NN
from config import SCHEME, MUTATION_CHANCE


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
        NN._inherit_connections(self, parent)

        self._hidden_in = [array(layer) for layer in parent._hidden_in]
        self._hidden_out = [array(layer) for layer in parent._hidden_out]

        for hidden in (self._hidden_in, self._hidden_out):
            chance = MUTATION_CHANCE * sum(
                hidden_layer.size for hidden_layer in hidden
            )
            for hidden_layer in hidden:
                n, = hidden_layer.shape
                for i in range(n):
                    if randfloat() <= chance:
                        hidden_layer[i] = randfloat() * choice((-1, 1))

    def _generate_connections(self):
        NN._generate_connections(self)
        self._hidden_in = [uniform(-1, 1, layer) for layer in SCHEME[1:]]
        self._hidden_out = [uniform(-1, 1, layer) for layer in SCHEME[1:]]
