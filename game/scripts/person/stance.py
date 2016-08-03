# -*- coding: UTF-8 -*-


class Stance(object):
    _types = {'master': ['cruel', 'opressive', 'rightful', 'benevolent'],
            'slave': ['rebellious', 'forced', 'accustomed', 'willing'],
            'neutral': ['hostile', 'distrustful', 'favorable', 'friendly']} 
    def __init__(self, person1, person2):
        self.persons = [person1, person2]
        self._type = 'neutral'
        self._value = 0
        self.conquest = 0
        self.convention = 0
        self.contribution = 0
        self._special_value = None
        self.is_player_stance()
    def is_player_stance(self):
        if self.persons[0].player_controlled or self.persons[1].player_controlled:
            if not hasattr(self, 'player') and not hasattr(self, 'npc'):
                for p in self.persons:
                    if p.player_controlled:
                        self.player = p
                    else:
                        self.npc = p
            return True
        return False
    def nature(self):
        if self.conquest == self.convention and self.convention == self.contribution:
            return 0
        if self.convention > self.contribution and self.convention > self.conquest:
            return 0
        if self.conquest > self.contribution and self.conquest > self.convention:
            return -1
        if self.contribution > self.conquest and self.contribution > self.convention:
            return 1
        if self.conquest == self.contribution and self.conquest > self.convention:
            return 0
        if self.convention == self.conquest and self.conquest > self.contribution:
            return -1
        if self.convention == self.contribution and sle.contribution > self.conquest:
            return 1
        return 0

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        if self._value < -1:
            self._value = -1

        elif self._value > 1:
            self._value = 1

    def to_max(self, value=None):
        self._value = 2
        if self.is_player_stance():
            self._special_value = value


    @property
    def type(self):
        return self._type

    @property
    def level(self):
        if self.value == 2 and self.is_player_stance():
            return self._special_value
        return Stance._types[self._type][self.value+1]


    def change_stance(self, stance):
        if stance not in Stance._types.keys():
            raise Exception("Wrong stance: %s"%(t))
        else:
            self._type = stance


