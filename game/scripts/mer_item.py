# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

class Item(object):
    type_ = 'item'
    def __init__(self, data_dict=None, *args, **kwargs):
        self.data = data_dict
        self.equiped = False
    @property
    def quality(self):
        return self.data['quality']
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
    @property
    def size(self):
        return self.data['size']
    @property
    def damage_type(self):
        return self.data['damage_type']

class Armor(Item):
    type_ = 'armor'
    @property
    def protection_type(self):
        return self.data['protection_type']

def gen_item(item_type, item_id):
    if item_type == 'weapon':
        stats = store.items_data['weapon'][item_id]
        weapon = Weapon(data_dict=stats)
        return weapon
    elif item_type == 'armor':
        stats = store.items_data['armor'][item_id]
        armor = Armor(data_dict=stats)
        return armor