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
        self.owner.life_quality += value*self.level
        self.last_satisfaction = value
        self.values.append(value*self.level)
        if self.level == 3 and value >= self.owner.sensitivity:
            self.owner.stimul = 1
        if self.name == 'wellness':
            if self.owner.physique <= value:
                self.owner.add_buff('drugs')
        if self.name == 'comfort':
            if self.owner.sensitivity <= value:
                self.owner.add_buff('bliss')
        if self.name == 'activity':
            if self.owner.spirit <= value:
                self.owner.add_buff('adrenaline')
        if self.name == 'eros':
            if value == 5:
                self.owner.add_buff('orgasm')

    def set_tension(self):
        if self.tension:
            return
        self.tension = True
        values = {1: -3, 2: -6, 3: -15, 0: 0}
        self.owner.life_quality += values[self.level]
        self.values.append(values[self.level])
        if self.level == 3:
            self.owner.stimul = -1
        if self.name in self._special.keys():
            self.owner.add_buff(self._special[self.name])

    @property
    def level(self):
        value = self._level + self.owner.count_modifiers(self.name)
        return min(3, max(0, value))

    def reset(self):
        self.tension = False
