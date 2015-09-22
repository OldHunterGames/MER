# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy


class MistsOfEternalRome(object):
    """
    This is the engine of MER core module
    """

    def __init__(self, protagonist):
        self.protagonist = protagonist  # Our main hero
        self.actor = protagonist        # Our active character, hero by default but maybe someone else!
        self.decade = 0                 # The number of decades (turns) passed in ERome
        self.menues = []                # For custom RenPy menu screen

    def end_turn(self):
        self.protagonist.sparks -= self.protagonist.lifestyle
        if self.protagonist.sparks < 0:
            return "game_over"
        else:
            return "new_turn"

    def discover_world(self, worlds):
        return choice(worlds)().point_of_arrival









