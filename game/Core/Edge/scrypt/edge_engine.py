# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy


class EdgeEngine(object):
    """
    This is the main script of Edge of Mists core module for Mists of Eternal Rome.
    """

    def __init__(self):
        self.locations = None
