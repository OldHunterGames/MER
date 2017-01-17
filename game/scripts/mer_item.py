# -*- coding: <UTF-8> -*-
from random import *

import renpy.store as store
import renpy.exports as renpy

from features import Feature
from modifiers import ModifiersStorage
from mer_utilities import encolor_text

# sizes 'offhand', 'versatile', 'shield', 'twohand'
class Item(object):
    type_ = 'item'

    def __init__(self, data_dict, id_, *args, **kwargs):
        self.data = data_dict[id_]
        self.id = id_
        self.equiped = False
        
        self.features = []
        self.modifiers = ModifiersStorage()
        self.features_data_dict = 'item_features'
        if 'price' in kwargs.keys():
            self._price = kwargs['price']
        else:
            self._price = 1

        self.new_description = None
        self.new_name = None

    @property
    def price(self):
        return self.data.get('price', 1)

    @property
    def quality(self):
        value = self.data.get('quality', 0)
        value += self.count_modifiers('quality')
        return max(0, min(5, value))

    def set_quality(self, quality):
        self._quality = quality

    @property
    def name(self):
        if self.new_name is not None:
            return encolor_text(self.new_name, self.quality)
        name = self.data.get('name', 'Unnamed')
        return encolor_text(name, self.quality)

    @property
    def mutable_name(self):
        return self.data.get('mutable_name', False)

    def set_name(self, name):
        if not self.mutable_name:
            return
        self.new_name = name

    def reset_name(self):
        self.new_name = None

    @property
    def type(self):
        return self.type_
    
    @property
    def amount(self):
        return 1

    def description(self):
        if self.new_description is not None:
            return self.new_description
        return self.data.get('description', "No description")

    def set_description(self, value):
        if not self.mutable_description:
            return
        self.new_description = value

    @property
    def mutable_description(self):
        return self.data.get('mutable_description', False)

    def reset_description(self):
        self.new_description = None

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

    def get_all_modifiers(self):
        return self.modifiers.get_all_modifiers()

    def use(self):
        return

    def equip(self):
        self.equiped = True

    def unequip(self):
        self.equiped = False


    def stats(self):
        return ''

    def stackable(self):
        return False

    @property
    def present(self):
        return self.data.get('present', None)

       

class Stackable(Item):

    _type = 'stackable'

    def __init__(self, *args, **kwargs):
        if 'copy' in kwargs.keys():
            for key, value in kwargs['copy'].__dict__.items():
                setattr(self, key, value)
            return
        super(Stackable, self).__init__(*args, **kwargs)
        
        self._amount = 1
    
    def stackable(self):
        return True

    @property
    def amount(self):
        return self._amount
    
    def use(self):
        self._use()
        self._amount -= 1

    def _use(self):
        return

    def increase_amount(self, value):
        self._amount += value

    def decrease_amount(self, value):
        self._amount -= value
        new = Stackable(copy=self)
        if self._amount < 0:
            new._amount = value - abs(self._amount)
        else:
            new._amount = value
        return new


class Treasure(Stackable):

    _type = 'treasure'



class Weapon(Item):
    type_ = 'weapon'

    def __init__(self, *args, **kwargs):
        super(Weapon, self).__init__(*args, **kwargs)
        self.set_size(self.data['size'])
        self.set_damage_type(self.data['damage_type'])
        if self.wpn_range is not None:
            self.set_range(self.wpn_range)

    @property
    def wpn_range(self):
        return self.data.get('wpn_range')

    @property
    def size(self):
        return self.feature_by_slot('wpn_size').id

    def set_size(self, size):
        self.add_feature(size)

    @property
    def damage_type(self):
        return self.feature_by_slot('wpn_dmg').id

    def set_range(self, wpn_range):
        self.add_feature(wpn_range)

    def set_damage_type(self, wpn_dmg):
        self.add_feature(wpn_dmg)
    
    def stats(self):
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

    def __init__(self, *args, **kwargs):
        super(Armor, self).__init__(*args, **kwargs)
        self.set_armor_rate(self.data['armor_rate'])

    @property
    def armor_rate(self):
        return self.feature_by_slot('armor_rate').id

    def set_armor_rate(self, armor_rate):
        self.add_feature(armor_rate)

    def stats(self):
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


def create_item(id, type):
    types = {'armor': (Armor, store.armor_data),
        'weapon': (Weapon, store.weapon_data),
        'treasure': (Treasure, store.treasure_data)}
    item_properties = types[type]
    item = item_properties[0](item_properties[1], id)
    return item
