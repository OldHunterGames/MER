# -*- coding: UTF-8 -*-
from copy import copy
from collections import OrderedDict

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import encolor_text


class Relations(object):
    """Represents relations between npc and player"""
    _fervor = {-1: "delicate", 0: "straight", 1: "passionate"}
    _distance = {-1: "intimate", 0: "fair", 1: "formal"}
    _congruence = {-1: "hater", 0: "associate", 1: "admirer"}
    # some things here has strong dependency on npc's alignment
    _fervor_alignment = 'activity'
    _distance_alignment = 'orderliness'
    _congruence_alignment = 'morality'

    def __init__(self, person1, person2):
        self.persons = [person1, person2]
        self._axis = OrderedDict({
            'fervor': 0,
            'distance': 0,
            'congruence': 0
        })
        self.stability = 0
        self.first_impression = False
        self.is_player_relations()
        self._type = 'neutral'
        self._stance = 0
        self._special_value = None
        self._used = set()

    @property
    def axis(self):
        return copy(self._axis)

    def axis_str(self, axis):
        return getattr(self, axis+'_str')()

    def is_player_relations(self):
        if self.persons[0].player_controlled or self.persons[
                1].player_controlled:
            if not hasattr(self, 'player') and not hasattr(self, 'npc'):
                for p in self.persons:
                    if p.player_controlled:
                        self.player = p
                    else:
                        self.npc = p
            return True
        else:
            return False

    @property
    def type(self):
        return self._type

    def change_type(self, name):
        self._type = name

    @property
    def stance(self):
        value = self._stance
        for key in self.axis.keys():
            if self.dissonance(key):
                value -= 1
        return max(-1, min(2, value))

    def colored_stance(self, protected=False):
        value = self.stance
        if value == -1:
            color = 0
        elif value == 0:
            color = 2
        elif value == 1:
            color = 4
        else:
            color = 5
        return encolor_text(self.show_stance(), color, protected)

    @stance.setter
    def stance(self, value):
        self._value = value
        if self._stance < -1:
            self._stance = -1

        elif self._stance > 1:
            self._stance = 1
        else:
            self._stance = value

    def make_max_stance(self, value=None):
        self._stance = 2
        if self.is_player_relations():
            if value is None:
                return
            self._special_value = value

    def show_stance(self):
        value = self.attitude_tendency()
        return store.relations_name[self.stance][value]

    def attitude_tendency(self):
        if self.type == 'master' or self.type == 'slave':
            return self.type
        value = 'neutral'
        if self._axis['congruence'] == 1 and self.npc.token != 'antagonism':
            value = 'friendly'
        if self.npc.token == 'contribution':
            value = 'friendly'
        if self._axis['congruence'] == -1  or self.npc.token == 'antagonism' or \
                (self.npc.token == 'conquest' and self._axis['congruence'] != 1):
            value = 'hostile'
        return value

    def is_max_stance(self):
        return self.stance == 2

    def is_max(self, axis, border):
        d = {'-': -1, '+': 1}
        if getattr(self, axis) == d[border]:
            return True
        return False

    @property
    def fervor(self):
        value = self._axis['fervor']
        if self.is_player_relations():
            return value
        fervor = value + \
            self.persons[0].alignment.activity + \
            self.persons[1].alignment.activity
        if fervor < -1:
            fervor = -1
        elif fervor > 1:
            fervor = 1
        return fervor

    def show_fervor(self, colorise=False, protected=False, value=None):
        text = self._translate('fervor', value)
        if colorise:
            return self._colorise(text, 'fervor', protected)
        else:
            return text

    def fervor_str(self):
        return Relations._fervor[self.fervor]

    @property
    def distance(self):
        value = self._axis['distance']
        if self.is_player_relations():
            return value
        distance = value + \
            self.persons[0].alignment.orderliness + \
            self.persons[1].alignment.orderliness
        if distance < -1:
            distance = -1
        elif distance > 1:
            distance = 1
        return distance

    def distance_str(self):
        return Relations._distance[self.distance]

    def show_distance(self, colorise=False, protected=False, value=None):
        text = self._translate('distance', value)
        if colorise:
            return self._colorise(text, 'distance', protected)
        else:
            return text

    def _colorise(self, text, axis, protected=False):
        color = None
        if self.dissonance(axis):
            color = 'red'
        elif self.used(axis):
            color = 'cyan'
        elif self.resonance(axis):
            color = 'gold'
        elif self.active(axis):
            color = 'green'
        if color is None:
            return text
        else:
            return encolor_text(text, color, protected)

    def _translate(self, axis, value=None):
        if value is not None:
            return store.relations_translation[axis][value]
        return store.relations_translation[axis][self._axis[axis]]

    @property
    def congruence(self):
        value = self._axis['congruence']
        if self.is_player_relations():
            return value
        congruence = value + \
            self.persons[0].alignment.morality + \
            self.persons[1].alignment.morality
        if congruence < -1:
            congruence = -1
        elif congruence > 1:
            congruence = 1
        return congruence

    def congruence_str(self):
        return Relations._congruence[self.congruence]

    def show_congruence(self, colorise=False, protected=False, value=None):
        text = self._translate('congruence', value)
        if colorise:
            return self._colorise(text, 'congruence', protected)
        else:
            return text

    def description(self, colorise=False, protected=False):
        return (self.show_fervor(colorise, protected), self.show_distance(colorise, protected),
                self.show_congruence(colorise, protected))

    def set_axis(self, axis, value):
        if value in range(-1, 2):
            self._axis[axis] = value

    def change(self, axis, direction):
        if not self.is_player_relations():
            return
        ax = self.axis[axis]
        if direction == "+":
            ax += 1
            if ax > 1:
                ax = 1
        elif direction == '-':
            ax -= 1
            if ax < -1:
                ax = -1
        self.set_axis(axis, ax)

    def dissonance(self, axis):
        value = self._axis[axis]
        alignment_value = getattr(
            self.npc.alignment, getattr(self, '_%s_alignment' % (axis)))
        if value == 0 or alignment_value == 0:
            return False

        if value != alignment_value:
            return True
        else:
            return False

    def resonance(self, axis):
        value = self._axis[axis]
        alignment_value = getattr(
            self.npc.alignment, getattr(self, '_%s_alignment' % (axis)))
        if value == 0 or alignment_value == 0:
            return False

        return not self.dissonance(axis)

    def used(self, axis):
        return (axis, self._axis[axis]) in self._used

    def use(self, axis):
        self._used.add((axis, self._axis[axis]))

    def active(self, axis):
        return (self._axis[axis] != 0 and not self.dissonance(axis) and
                not self.used(axis))

    def neutral(self, axis):
        return self._axis[axis] == 0
