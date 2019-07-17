"""Module contains AIPool class."""


from multiprocessing import Process, Manager
from random import choice
from aicontroller import AIController
from game import Game
from config import POPULATION_SIZE, GAMES_PER_GENERATION, \
    MAX_TURNS, SURVIVING_ODDS, MUTATION_CHANCE, MAX_WORKING_THREADS


class AIPool(object):
    """
    AIPool contains the pool of AIController instances.

    Inside it controllers are being trained and evolve.
    All the evolution is happening in parallel Process.
    """

    def __init__(self):
        """Create the AIPool."""
        self._speciments = Manager().dict({
            (0, i): AIController()
            for i in range(POPULATION_SIZE)
        })
        self._process = None
        self._game = Game()
        self._gen_n = 0

    def get_instances_ids(self):
        """Get the list of instances ids."""
        return list(self._speciments)

    def get_instance_by_id(self, id):
        """Get the instance of an AIController by its id."""
        return AIController(self._speciments[id])

    def ready(self):
        """Check if pool is ready for next generation."""
        return self._process is None or not self._process.is_alive()

    def process_generation(self):
        """
        Process one generation.

        Method starts sub-process.
        """
        self._gen_n += 1
        if self._process:
            self._process.join()
        self._process = Process(
            target=self._run,
            args=((self._speciments,))
        )
        self._process.start()

    def _run(self, speciments):
        self._speciments = speciments
        scores = self._play()
        self._select(scores)
        self._repopulate()

    def _play(self):
        return [
            (self._process_speciment(speciment), spec_id)
            for (spec_id, speciment) in self._speciments.items()
        ]

    def _select(self, scores):
        scores.sort(reverse=True)
        scores = scores[:int(len(scores)*SURVIVING_ODDS)]
        survived_speciments = {spec_id for score, spec_id in scores}
        for spec_id in self._speciments.keys():
            if spec_id not in survived_speciments:
                del self._speciments[spec_id]

    def _repopulate(self):
        children = []
        parents = list(self._speciments.items())
        last_id = 0
        for _ in range(POPULATION_SIZE - len(self._speciments)):
            (gen_id, spec_id), parent = choice(parents)
            child = AIController(parent, MUTATION_CHANCE)
            child_id = (self._gen_n, last_id)
            last_id += 1
            children.append((child_id, child))
        self._speciments.update(children)

    def _process_speciment(self, speciment):
        scores = [0]*GAMES_PER_GENERATION
        for game_n in range(GAMES_PER_GENERATION):
            speciment.reset()
            self._game.restart()
            for _ in range(MAX_TURNS):
                self._game.update(speciment.direction)
                speciment.percive(self._game)
                speciment.update()
                if self._game.is_lost:
                    break
            scores[game_n] = self._game.score
        return sum(scores)
