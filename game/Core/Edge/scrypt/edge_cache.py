# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from mer_utilities import encolor_text
from factions import Faction
from mer_person import gen_random_person
from mer_resources import BarterSystem

class Cache(object):

    def __init__(self, name):
        self.name = name
        self.stash = []
        