# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from features import Feature
from modifiers import ModifiersStorage
class Item(object):
    type_ = 'item'
    def __init__(self, data_dict, *args, **kwargs):
        self.data = data_dict
        self.features_data_dict = '%s_features'%(self.type)
        self.equiped = False
        self.features = []
        self.modifiers = ModifiersStorage()
        try:
            self._init_features()
        except AttributeError:
            pass
    def add_feature(self, id_):
        Feature(self, id_, self.features_data_dict)

    def remove_feature(self, feature):
        if isinstance(feature, str):
            for feature in self.features:
                if feature.id == feature:
                    feature.remove()
        else:
            try:
                while True:
                    i = self.features.index(feature)
                    self.features[i].remove()
            except ValueError:
                return

    def feature_by_slot(self, slot):
        for feature in self.features:
            if feature.slot == slot:
                return feature

    def count_modifiers(self, attribute):
        return self.modifiers.count_modifiers(attribute)

    @property
    def quality(self):
        return self.data['quality']+self.count_modifiers('quality')
    @property
    def name(self):
        return self.data['name']
    @property
    def type(self):
        return self.type_
    def equip(self):
        self.equiped = True
    def unequip(self):
        self.equiped = False

class Weapon(Item):
    type_ = 'weapon'
    def _init_features(self):
        self.add_feature(self.size)
        self.add_feature(self.damage_type)
    @property
    def size(self):
        return self.data['size']
    @property
    def damage_type(self):
        return self.data['damage_type']

class Armor(Item):
    type_ = 'armor'
    def _init_features(self):
        self.add_feature(self.protection_type)
    @property
    def protection_type(self):
        return self.data['protection_type']

def gen_item(item_type, item_id):
    stats = getattr(store, item_type+'_data')[item_id]
    item_type = item_type.title()
    cls = globals()[item_type]
    item = cls(data_dict=stats)
    return item