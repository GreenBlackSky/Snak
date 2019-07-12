"""Module contains AIPool class."""


from aicontroller import AIController
from game import Game


class AIPool(object):
    """
    AIPool contains pool of AIController instances.

    Inside it controllers are being trained and evolve.
    """

    def __init__(self):
        """Create AIPool."""
        pass

    def get_instances_ids(self):
        """Get list of instances ids."""
        pass

    def get_instance_by_id(self, id):
        """Get instance of AIController by its id."""
        pass

    def update(self):
        """Update situation inside pool."""
        pass
