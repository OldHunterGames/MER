# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

class Item(object):
    def __init__(self, data_dict=None, *args, **kwargs):
        self.data = data_dict
    @property
    def quality(self):
        return self.data['quality']
    @property
    def name(self):
        return self.data['name']

class Weapon(Item):
    @property
    def size(self):
        return self.data['size']
    @property
    def damage_type(self):
        return self.data['damage_type']

class Armor(Item):
    @property
    def type(self):
        return self.data['armor_type']

def gen_item(item_type, item_id):
    if item_type == 'weapon':
        stats = store.items_data['weapon'][item_id]
        weapon = Weapon(data_dict=stats)
        return weapon
    elif item_type == 'armor':
        stats = store.items_data['armor'][item_id]
        armor = Armor(data_dict=stats)
        return armor