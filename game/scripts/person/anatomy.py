# -*- coding: <UTF-8> -*-

import renpy.store as store
import renpy.exports as renpy
from features import Feature

class BodyPart(object):


    def __init__(self, basis):
        self.features = []
        self.basis = Feature(basis, 'anatomy_features')
        self.add_feature(self.basis)
        self.wetness = 0
        self.stretch = 0

    @property
    def size(self):
        return sum([i.count_modifiers('size') for i in self.features])

    def add_feature(self, id_, time=None):
        if self.has_feature(id_):
            return
        try:
            feature = Feature(id_, 'anatomy_features')
        except KeyError:
            pass
        else:
            if feature.slot is not None:
                self.remove_feature_by_slot(feature.slot)
            self.features.append(feature)

    def feature_by_slot(self, slot):        # finds feature which hold needed slot
        for f in self.features:
            if f.slot == slot:
                return f
        return None

    def feature(self, id_):                # finds feature with needed name if exist
        for f in self.features:
            if f.id == id_:
                return f
        return None

    def has_feature(self, id_):
        return self.feature(id_) is not None

    def remove_feature(self, feature):
        if isinstance(feature, str):
            for i in self.features:
                if i.id == feature:
                    self.features.remove(i)
        else:
            try:
                self.features.remove(feature)
            except ValueError:
                return

    def remove_feature_by_slot(self, slot):
        for f in self.features:
            if f.slot == slot:
                self.features.remove(f)
                return

    def __getattr__(self, key):
        for f in self.__dict__['features']:
            if f.slot == key:
                value = f
                break
        else:
            value = None
        if value is None:
            raise AttributeError(key)
        else:
            return value

    def description(self):
        basis = self.basis.description
        basis = basis.format(self=self)
        return basis


class Anatomy(object):


    def __init__(self):
        self.parts = dict()