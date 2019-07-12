"""Module contains AIPool class."""


from aicontroller import AIController
from game import Game
from config import POPULATION


class AIPool(object):
    """
    AIPool contains pool of AIController instances.

    Inside it controllers are being trained and evolve.
    """

    def __init__(self):
        """Create AIPool."""
        self._speciments = {
            i: AIController()
            for i in range(POPULATION)
        }
        pass

    def get_instances_ids(self):
        """Get list of instances ids."""
        return list(self._speciments)

    def get_instance_by_id(self, id):
        """Get instance of AIController by its id."""
        return AIController(self._speciments[id])

    def process_generation(self):
        """Update situation inside pool."""
        pass
