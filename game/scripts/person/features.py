# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import renpy.store as store
import renpy.exports as renpy
from features_data import person_features

class Feature(object):

    def __init__(self, owner=None, name="generic", *args, **kwargs):
        stats = None
        if not stats:
            stats = person_features[name] if name in person_features else None
        if not stats:
            return 
        self.name = name
        self.slot = stats['slot'] if 'slot' in stats else None        # There can be only one feature for every feature slot
        self.revealed = False   # true if the feature is revealed to player      
        self.owner = owner    # the Person() who owns this feature
        self.value = stats['value'] if 'value' in stats else 0    # value for feature-based actions
        self.modifiers = stats['modifiers'] if 'modifiers' in stats else None     # parameter in key will be modified by value. Example: "agility": -1
        self.visible = stats['visible'] if 'visible' in stats else False
        self.time = kwargs['time'] if 'time' in kwargs else None
        self.add()

    def remove(self):
        if self.modifiers:
            name = self.slot if self.slot else self.name
            self.owner.modifiers.del_item(name)
        self.owner.features.remove(self)

    def add(self):
        if self in self.owner.features:
            return
        if self.slot == None:
            self.owner.features.append(self)
            if self.modifiers:
                slot = self.slot if self.slot else self.name
                self.owner.modifiers.add_modifier(self.name, self.modifiers, self, slot)
            return
        else:
            for feature in self.owner.features:
                if feature.slot == self.slot:
                    feature.remove()
            if self.modifiers:
                slot = self.slot if self.slot else self.name
                self.owner.modifiers.add_modifier(self.name, self.modifiers, self, slot)
            self.owner.features.append(self)


    def tick_time(self):
        try:
            self.time -= 1
            if self.time < 1:
                self.remove()
        except TypeError:
            pass
            
class Phobia(Feature):
    def __init__(self, owner, name, fear_obj, *args, **kwargs):
        stats = person_phobias[name] if name in person_phobias else None
        super(Phobia, self).__init__(owner, name)
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









