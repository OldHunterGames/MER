# -*- coding: UTF-8 -*-
from random import choice
import renpy.store as store
import renpy.exports as renpy

def init_genus(caller, genus):
    for sub in Genus.__subclasses__():
        if sub.get_name() == genus:
            try:
                if caller.genus.get_name() != sub.get_name():
                    caller.genus.remove()
            except AttributeError:
                pass
            genus = sub(caller)
            genus.invoke()
            return genus
    raise Exception("No genus named %s"%(genus))

def available_genuses():
    return [genus for genus in Genus.__subclasses__()]

class Genus(object):
    _available_ages_ = ['junior', 'adolescent', 'mature', 'elder']
    _available_genders_ = ['male', 'female', 'sexless', 'shemale']
    _features_ = []
    head_type = None
    def __init__(self, owner):
        self.owner = owner

    def remove(self):
        for feature in self._features_:
            self.owner.remove_feature(feature)
        self.owner.remove_feature(self.head_type)
    def invoke(self):
        for feature in self._features_:
            self.owner.add_feature(feature)
        self.owner.add_feature(self.head_type)
        return self
    @classmethod
    def genders(cls):
        return cls._available_genders_
    @classmethod
    def ages(cls):
        return cls._available_ages_
    @classmethod
    def get_name(cls):
        return cls._name_
class Human(Genus):
    _name_ = 'human'
    head_type = 'human'
class Vampire(Genus):
    _available_ages_ = []
    _name_ = 'vampire'
    head_type = 'undead'
class Werewolf(Genus):
    _available_ages_ = []
    _name_ = 'werewolf'
    head_type = 'canine'
class Lupine(Genus):
    _available_ages_ = []
    _name_ = 'lupine'
    head_type = 'canine'
class Slime(Genus):
    _available_ages_ = []
    _available_genders_ = []
    head_type = 'slime'
    _name_ = 'slime'