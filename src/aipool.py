"""Module contains AIPool class."""


from concurrent.futures import ThreadPoolExecutor
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
        with ThreadPoolExecutor(max_workers=MAX_WORKING_THREADS) as executor:
            results = {
                spec_id: executor.submit(
                    AIPool._process_speciment,
                    speciment,
                    Game()
                )
                for (spec_id, speciment) in self._speciments.items()
            }
        return [
            (spec_id, future.result())
            for spec_id, future in results.items()
        ]

    def _select(self, scores):
        scores.sort(
            key=lambda item: item[1],
            reverse=True
        )
        scores = scores[:int(len(scores)*SURVIVING_ODDS)]
        survived_speciments = {
            spec_id for spec_id, score in scores
        }
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

    @staticmethod
    def _process_speciment(speciment, game):
        scores = [0]*GAMES_PER_GENERATION
        for game_n in range(GAMES_PER_GENERATION):
            speciment.reset()
            game.restart()
            for _ in range(MAX_TURNS):
                game.update(speciment.direction)
                speciment.percive(game)
                speciment.update()
                if game.is_lost:
                    break
            scores[game_n] = game.score
        return sum(scores)
