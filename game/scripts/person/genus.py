# -*- coding: UTF-8 -*-
from random import choice

from mer_utilities import weighted_random

import renpy.store as store


_available_ages_ = ['junior', 'adolescent', 'mature', 'elder']


def available_genuses():
    return [name for name in store.genuses_data.keys()]


class Genus(object):
    _available_ages = ['adolescent', 'mature']
    _available_genders = ['male', 'female', 'sexless', 'shemale']
    head_type = None

    def __init__(self, id_):
        self._owner = None
        self.id = id_
        self.data = store.genuses_data[id_]

    def __getattr__(self, key):
        try:
            value = self.data[key]
        except KeyError:
            raise AttributeError(key)
        else:
            if callable(value):
                return value(self._owner)
            return value

    def remove(self):
        for feature in self._features:
            self._owner.remove_feature(feature)
        self._owner.remove_feature(self.head_type)
        self._owner = None

    def apply(self, owner):
        self._owner = owner
        for feature in self._features:
            self._owner.add_feature(feature)
        self._owner.add_feature(self.head_type)

    @property
    def genders(self):
        try:
            genders = self.data['genders']
        except KeyError:
            genders = self._available_genders
        return genders

    def get_gender(self):
        try:
            gender = weighted_random(self.genders)
        except ValueError:
            gender = choice(self.genders)
        return gender

    def genders_names(self):
        return [i[0] for i in self.genders]

    def get_age(self):
        try:
            age = weighted_random(self.ages)
        except ValueError:
            age = choice(self.ages)
        return age

    @property
    def ages(self):
        try:
            ages = self.data['ages']
        except KeyError:
            ages = self._available_ages
        return ages

    def ages_names(self):
        return [i[0] for i in self.ages]

    @property
    def head_type(self):
        return self.data['head_type']

    @property
    def _features(self):
        try:
            features = self.data['features']
        except KeyError:
            features = []
        return features

    @property
    def name(self):
        return self.data['name']

    @property
    def type(self):
        return self.data['type']
