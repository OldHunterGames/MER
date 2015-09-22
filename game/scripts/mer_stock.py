# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy


class Stockpile(object):
    """
    The stockpile for base resources.
    """

    def __init__(self, stock):
        self.stock = stock       # Gets {} of resources
        self.spoil_rate = 100    # This % or resources vanishes when time advances to next global turn







