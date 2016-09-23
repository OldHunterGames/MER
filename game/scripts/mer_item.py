# -*- coding: <UTF-8> -*-
from random import *

import renpy.store as store
import renpy.exports as renpy

from features import Feature
from modifiers import ModifiersStorage
from mer_utilities import encolor_text


class Item(object):
    type_ = 'item'

    def __init__(self, *args, **kwargs):
        self._name = ""
        if 'quality' in kwargs.keys():
            self._quality = kwargs['quality']
        else:
            self._quality = 1
        self.equiped = False
        self.features = []
        self.modifiers = ModifiersStorage()
        self.features_data_dict = 'item_features'

    def add_feature(self, id_):
        Feature(self, id_, self.features_data_dict)

    def remove_feature(self, feature):
        if isinstance(feature, str):
            for feature in self.features:
                if feature.id == feature:
                    feature.remove()
        else:
            try:
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

    def set_name(self, name):
        self._name = name

    def set_quality(self, quality):
        self._quality = quality

    def make(self):
        try:
            self._init_features()
        except AttributeError:
            pass

    def make_from_dict(self, properties_dict):
        for key, value in properties_dict.items():
            setter = 'set_' + key
            try:
                getattr(self, setter)(value)
            except AttributeError:
                pass

    @property
    def quality(self):
        return min(5, self._quality + self.count_modifiers('quality'))

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self.type_

    def equip(self):
        self.equiped = True

    def unequip(self):
        self.equiped = False


class Weapon(Item):
    type_ = 'weapon'

    def __init__(self, size, damage_type, *args, **kwargs):
        super(Weapon, self).__init__(*args, **kwargs)
        self.set_size(size)
        self.set_damage_type(damage_type)

    def _init_features(self):
        self.add_feature(self.size)
        self.add_feature(self.damage_type)

    @property
    def size(self):
        return self.feature_by_slot('wpn_size').id

    def set_size(self, size):
        self.add_feature(size)

    @property
    def damage_type(self):
        return self.feature_by_slot('wpn_dmg').id

    def set_damage_type(self, wpn_dmg):
        self.add_feature(wpn_dmg)

    @property
    def description(self):
        damage_type = self.feature_by_slot('wpn_dmg').name
        size = self.feature_by_slot('wpn_size').name
        if self.size != 'shield':
            text = '{damage_type} {size}'.format(
                size=size, damage_type=damage_type)
        else:
            text = 'shield'.format(size=size, damage_type=damage_type)
        return encolor_text(text, self.quality)


class Armor(Item):
    type_ = 'armor'

    def __init__(self, armor_rate, *args, **kwargs):
        super(Armor, self).__init__(*args, **kwargs)
        self.set_armor_rate(armor_rate)

    def _init_features(self):
        self.add_feature(self.armor_rate)

    @property
    def armor_rate(self):
        return self.feature_by_slot('armor_rate').id

    def set_armor_rate(self, armor_rate):
        self.add_feature(armor_rate)

    @property
    def description(self):
        text = '{self.armor_rate}'.format(self=self)
        return encolor_text(text, self.quality)

def get_weapon_sizes():
    list_ = []
    for key, value in store.item_features.items():
        if value['slot'] == 'wpn_size':
            list_.append(key)
    return list_

def get_weapon_damage_types():
    list_ = []
    for key, value in store.item_features.items():
        if value['slot'] == 'wpn_dmg':
            list_.append(key)
    return list_

def get_armor_rates():
    list_ = []
    for key, value in store.item_features.items():
        if value['slot'] == 'armor_rate':
            list_.append(key)
    return list_

def create_weapon(size=None, damage_type=None, quality=1):
    if size is None:
        size = random.choice(get_weapon_sizes())
    if damage_type is None:
        damage_type = random.choice(get_weapon_damage_types())
    weapon = Weapon(size, damage_type, quality=quality)
    return weapon

def create_armor(armor_rate=None, quality=1):
    if armor_rate is None:
        armor_rate = random.choice(get_armor_rates())
    armor = Armor(armor_rate, quality=quality)
    return armor

def create_item():
    creator_item_properties = {'type': None}
    renpy.call_screen('sc_item_creator', creator_item_properties)
    item_type = creator_item_properties['type']
    if item_type == 'armor':
        item = Armor(creator_item_properties['armor_rate'])
    elif item_type == 'weapon':
        item = Weapon(creator_item_properties[
                      'size'], creator_item_properties['damage_type'])
    item.set_quality(1)
    return item
