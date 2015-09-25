# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import renpy.store as store
import renpy.exports as renpy


class Feature(object):

    def __init__(self, owner, name="generic"):
        self.name = name
        self.slot = None        # There can be only one feature for every feature slot
        self.revealed = False   # true if the feature is revealed to player
        self.owner = owner      # the Person() who owns this feature
        self.modifiers = {}     # parameter in key will be modified by value. Example: "agility": -1


class Blood(Feature):
    """
    "degenerate"    -1 all attributes
    "thin blood"    -1 phys, -1 agi
    "weak blood"    -1 phys
    "normal"        nothing
    "strong blood"  +1 phys
    "savage blood"  +1 phys, +1 agi
    "purebreed"     +1 all attrubutes
    """

    def __init__(self, owner, name):
        super(Feature).__init__(owner, name)
        self.slot = "blood"
        if name == "purebreed":
            self.modifiers["physique"] = 1
            self.modifiers["agility"] = 1
            self.modifiers["spirit"] = 1
            self.modifiers["mind"] = 1
            self.modifiers["sensitivity"] = 1
        elif name == "savage blood":
            self.modifiers["physique"] = 1
            self.modifiers["agility"] = 1
        elif name == "strong blood":
            self.modifiers["physique"] = 1
        elif name == "weak blood":
            self.modifiers["physique"] = -1
        elif name == "thin blood":
            self.modifiers["physique"] = -1
            self.modifiers["agility"] = -1
        elif name == "degenerate":
            self.modifiers["physique"] = -1
            self.modifiers["agility"] = -1
            self.modifiers["spirit"] = -1
            self.modifiers["mind"] = -1
            self.modifiers["sensitivity"] = -1
        else:
            self.name = "normal"









