# -*- coding: UTF-8 -*-
from copy import deepcopy


needs_names = ["relief", "general", 'purpose',  # basic needs that all character have. "relief" intensity fixed at 1, "general" at 2, "purporse" at 3
               "nutrition", "wellness", "comfort", "activity", "communication", "amusement", "prosperity", "authority", "ambition", "eros",
               "order", "independence", "approval", "thrill", "altruism", "power"]

_default_need = {"level": 2}


def init_needs(owner):
    l = []
    for name in needs_names:
        l.append(Need(owner, name))
    return l


class Need(object):

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self._level = _default_need['level']
        self._satisfaction = 0
        self._tension = False
        self.tokens = []

    def use_token(self, token):
        self.tokens.append(token)

    def token_used(self, token):
        return token in self.tokens

    @property
    def satisfaction(self):
        return self._satisfaction

    @satisfaction.setter
    def satisfaction(self, value):
        levels = [0, self.owner.sensitivity, 5, 5]
        if value < 0:
            value = 0
        if value > levels[self.level]:
            value = levels[self.level]
        if value < self._satisfaction:
            return
        self._satisfaction = value

    @property
    def tension(self):
        return self._tension or self.owner.count_modifiers(self.name) < 0

    def set_satisfaction(self, value):
        levels = [0, self.owner.sensitivity, 5, 5]
        if value < 0:
            value = 0
        if value > levels[self.level]:
            value = levels[self.level]
        if value < self._satisfaction:
            return
        self._satisfaction = value

    def set_tension(self):
        self._tension = True

    @property
    def level(self):
        if self.name == 'relief':
            return 1
        elif self.name == 'general':
            return 2
        elif self.name == 'purpose':
            return 3
        n = self.owner.alignment.special_needs()
        if self.name in n[2]:
            return 1
        if self.name in n[0]:
            return 3
        elif self.name in n[1]:
            return 0
        value = self._level + self.owner.count_modifiers(self.name)
        return min(3, max(0, value))

    def reset(self):
        self._satisfaction = 0
        self._tension = False
