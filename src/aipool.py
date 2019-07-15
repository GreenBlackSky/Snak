"""Module contains AIPool class."""


from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from random import choice
from aicontroller import AIController
from game import Game
from config import POPULATION_SIZE, GAMES_PER_GENERATION, \
    MAX_TURNS, SURVIVING_ODDS, MUTATION_CHANCE, MAX_WORKING_THREADS


class AIPool(object):
    """
    AIPool contains the pool of AIController instances.

    Inside it controllers are being trained and evolve.
    """

    def __init__(self):
        """Create the AIPool."""
        Thread.__init__(self)
        self._speciments = {
            (0, i): AIController()
            for i in range(POPULATION_SIZE)
        }
        self._games_pool = [Game() for _ in range(POPULATION_SIZE)]
        self._thread = None
        self._gen_n = 0

    def get_instances_ids(self):
        """Get the list of instances ids."""
        return list(self._speciments)

    def get_instance_by_id(self, id):
        """Get the instance of an AIController by its id."""
        return AIController(self._speciments[id])

    def ready(self):
        """Check if pool is ready for next generation."""
        return self._thread is None or not self._thread.is_alive()

    def start_process(self):
        """Process one generation."""
        if self._thread:
            self._thread.join()
        self._thread = Thread(target=self._run)
        self._thread.start()

    def _run(self):
        self._gen_n += 1
        scores = self._play()
        self._select(scores)
        self._repopulate()

    def _play(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKING_THREADS) as executor:
            results = {
                spec_id: executor.submit(
                    AIPool._process_speciment,
                    speciment,
                    game
                )
                for (spec_id, speciment), game in
                zip(self._speciments.items(), self._games_pool)
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
        self._speciments = {
            spec_id: self._speciments[spec_id]
            for spec_id, score in scores
        }

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
        scores = []
        for game_n in range(GAMES_PER_GENERATION):
            speciment.reset()
            game.restart()
            for _ in range(MAX_TURNS):
                game.update(speciment.direction)
                speciment.percive(game)
                speciment.update()
                if game.is_lost:
                    break
            scores.append(game.score)
        return sum(scores)
