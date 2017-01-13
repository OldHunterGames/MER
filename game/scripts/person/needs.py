# -*- coding: UTF-8 -*-
from copy import deepcopy


needs_names = ["nutrition", "wellness", "comfort", "activity", "communication",
        "amusement", "prosperity", "authority", "ambition", "eros"]

_default_need = {"level": 2}


def init_needs(owner):
    l = []
    for name in needs_names:
        l.append(Need(owner, name))
    return l


class Need(object):
    _special = {'wellness': 'pain', 'comfort': 'discomfort',
        'activity': 'deprivation', 'eros': 'lust'}
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self._level = _default_need['level']
        self.tokens = []
        self.spoils = []
        self.values = []
        self.max_satisfaction = 0
        self.last_satisfaction = 0
        self.tension = False

    def add_spoil(self, value):
        self.spoils.append(value)

    def remove_spoil(self, value):
        self.spoils.remove(value)

    def spoil_level(self):
        if self.level == 1:
            value = 4
        elif self.level == 2:
            value = 2
        else:
            value = 1
        return len(self.spoils)+value

    def use_token(self, token):
        self.tokens.append(token)

    def token_used(self, token):
        return token in self.tokens
    
    def set_satisfaction(self, value):
        if self.name not in self.owner.good_markers:
            self.owner.good_markers.append(self.name)
        self.max_satisfaction = max(self.max_satisfaction, value*self.level)
        self.last_satisfaction = value
        self.values.append(value*self.level)
        if self.level == 3:
            if self.owner.master is not None:
                if not self.player_controlled:
                    if 4 - self.player_stance().value > value:
                        self.owner.stimul += 1

    def set_tension(self):
        if self.tension:
            return
        self.owner.bad_markers.append(self.name)
        self.tension = True
        values = {1: -3, 2: -6, 3: -15, 0: 0}
        self.owner.life_quality += values[self.level]
        self.values.append(values[self.level])
        if self.level == 3:
            self.owner.stimul = -1


    @property
    def level(self):
        value = self._level + self.owner.count_modifiers(self.name)
        return min(3, max(0, value))

    def reset(self):
        self.tension = False
        self.max_satisfaction = 0
