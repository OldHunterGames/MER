# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
import sys
import inspect
from random import *
import renpy.store as store
import renpy.exports as renpy


class Event(object):

    def __init__(self, env):
        self.env = env              # Enviroment. Instance of current game engive instance
        self.goto = "evn_blank"     # RenPy location to start an event
        self.natures = []           # "triggered", "turn_end", "faction", "personal", "special"
        self.tags = []              # tags for filtering "gay", "lolicon", "bestiality", "futanari" etc
        self.unique = False         # Unique events shown once in a game instance
        self.seen = 0               # Number of times this event seen

    def trigger(self):
        """
        On event activation
        """
        self.seen += 1
        return self.goto

    def check(self):
        """
        Check out of this event can be triggered in a particular situation
        :return: if True - event is available, else - is not
        """
        check = True
        if self.unique == True and self.seen > 0:
            check = False
        return check




class EVUnique(Event):
    """
    Unique event for test
    """

    def __init__(self, env):
        super(EVUnique, self).__init__(env)
        self.natures = ["triggered", "turn_end", "faction"]
        self.goto = "evn_unic"
        self.unique = True


class EVGeneric(Event):
    """
    Generic event for test
    """

    def __init__(self, env):
        super(EVGeneric, self).__init__(env)
        self.goto = "evn_1"
        self.natures = ["triggered", "turn_end", "faction"]










