"""Module contains the AIPool class."""


from multiprocessing import Process, Manager
from random import choice
from aicontroller import AIController
from game import Game
from config import POPULATION_SIZE, GAMES_PER_GENERATION, \
    MAX_TURNS, SURVIVING_ODDS


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
        self._scores = Manager().dict({
            key: 0
            for key in self._speciments
        })
        self._process = None
        self._game = Game()
        self._gen_n = 0

    def get_instances_data(self):
        """Get the list of instances ids."""
        return [
            (*key, self._scores[key])
            for key in self._speciments
        ]

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
            args=((self._speciments, self._scores))
        )
        self._process.start()

    def _run(self, speciments, scores):
        self._speciments = speciments
        self._scores = scores
        self._play()
        self._select()
        self._repopulate()

    def _play(self):
        self._scores.clear()
        for (spec_id, speciment) in self._speciments.items():
            self._scores[spec_id] = self._process_speciment(speciment)

    def _select(self):
        scores_list = [
            (score, spec_id)
            for spec_id, score in self._scores.items()
        ]
        scores_list.sort(reverse=True)
        scores_list = scores_list[:int(len(scores_list)*SURVIVING_ODDS)]
        survived_speciments = {spec_id for score, spec_id in scores_list}
        for spec_id in self._speciments.keys():
            if spec_id not in survived_speciments:
                del self._speciments[spec_id]
                del self._scores[spec_id]

    def _repopulate(self):
        parents = list(self._speciments.items())
        last_id = 0
        for _ in range(POPULATION_SIZE - len(self._speciments)):
            (gen_id, spec_id), parent = choice(parents)
            child_id = (self._gen_n, last_id)
            last_id += 1
            self._speciments[child_id] = AIController(parent)
            self._scores[child_id] = 0

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
