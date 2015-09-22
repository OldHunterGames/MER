# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy


class OWForest(object):
    """
    This is an Outer World main engine.
    """

    descriptions_list = [
        "Forest world. Description 1.",
        "Forest world. Description 2.",
        "Forest world. Description 3.",
    ]

    def __init__(self):
        self.point_of_arrival = "owforest_arrive"
        self.type = "Forest"
        self.index = randint(1, 999)
        self.name = self.type + str(self.index)
        self.description = choice(self.descriptions_list)






