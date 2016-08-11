# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

camp_improvements_list = ['stove', 'workbench', 'distillery', 'alarm', 'fortifications',]

class EdgeCamp(object):
    """
    This is the player camp in Edge of Mists module.
    """

    def __init__(self):
        self.founded = False
        self.accommodation = 'accommodation_makeshift'
        self.beads = 0
        self.cells = 0
        self.scarecrows = 0
        self.traps = 0
        self.storage = None
        self.improvements = camp_improvements_list

    def found(self):
        self.founded = True
        self.improvements = []

    def dismantle(self):
        self.founded = False
        self.improvements = camp_improvements_list
        self.beads = 0
        self.cells = 0
        self.scarecrows = 0
        self.traps = 0

