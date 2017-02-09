# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import renpy.store as store
import renpy.exports as renpy

from modifiers import Modifiable
import mer_utilities


class Feature(Modifiable):
    

    def __init__(self, id_, data_dict='person_features', time=None, *args, **kwargs):
        try:
            data_dict = getattr(store, data_dict)
            stats = data_dict[id_]
        except KeyError:
            raise KeyError("no feature named %s in %s" % (id_, data_dict))
        self.init_modifiable()
        self.id = id_
        self.stats = stats
        self._time = time
        self._revealed = False   # true if the feature is revealed to player
        self.add_modifier(self.id, self.modifiers, self, self.slot)

    def __getattr__(self, key):
        try:
            value = self.stats[key]
        except KeyError:
            raise AttributeError(key)
        else:
            return value
    @property
    def name(self):
        return self.stats['name']

    def set_time(self, time):
        self._time = time

    @property
    def slot(self):
        try:
            slot = self.stats['slot']
        except KeyError:
            slot = None
        return slot

    @property
    def modifiers(self):
        try:
            return self.stats['modifiers']
        except KeyError:
            return dict()

    @property
    def visible(self):
        return self.stats['visible']

    @property
    def time(self):
        return self._time

    @property
    def value(self):
        return self.stats['value']

    @property
    def revealed(self):
        return self._revealed and self.visible

    def reveal(self):
        self._revealed = True

    def tick_time(self):
        try:
            self._time -= 1
            if self._time < 1:
                self.remove()
        except TypeError:
            pass


class Phobia(Feature):

    def __init__(self, owner, id_, fear_obj, *args, **kwargs):
        stats = person_phobias[id_] if id_ in person_phobias else None
        super(Phobia, self).__init__(owner, id_)
        self.object_of_fear = fear_obj


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

    def __init__(self, name):
        super(Blood, self).__init__(name)
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
