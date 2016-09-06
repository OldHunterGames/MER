# -*- coding: UTF-8 -*-
import collections


class Inventory(object):
    def __init__(self):
        self.carried_weapons = collections.OrderedDict([('harness', None), ('belt1', None),
            ('belt2', None), ('armband', None), ('ankleband', None)])
        self.carried_armor = collections.OrderedDict([('underwear', None), ('garments', None), ('overgarments', None)])
        self._main_hand = None
        self._other_hand = None
        self.storage = []
    def weapon_slots(self):
        return self.carried_weapons.keys()
    def armor_slots(self):
        return self.carried_armor.keys()
    @property
    def main_hand(self):
        return self._main_hand
    
    @main_hand.setter
    def main_hand(self, weapon):
        if self._main_hand != None:
            self._main_hand.unequip()
            if self._main_hand not in self.storage:
                self.storage.append(self._main_hand)
        self._main_hand = weapon
    
    @property
    def other_hand(self):
        return self._other_hand
    
    @other_hand.setter
    def other_hand(self, weapon):
        if self._other_hand != None:
            self._other_hand.unequip()
            if self._other_hand not in self.storage:
                self.storage.append(self._other_hand)
        self._other_hand = weapon
    
    def available_for_slot(self, slot, storage=None):
        if storage == None:
            storage = self.storage
        slots = {
        'belt1': ['offhand', 'versatile'],
        'belt2': ['offhand', 'versatile'],
        'harness': ['offhand', 'versatile', 'shield', 'twohanded'],
        'armband': ['offhand'],
        'ankleband': ['offhand']
        }
        list_ = []
        if slot in self.armor_slots():
            for item in storage:
                if item.type == 'armor':
                    list_.append(item)
        else:
            for item in storage:
                if item.type != 'armor':
                    if item.size in slots[slot]:
                        list_.append(item)
        return list_

    def equip_on_slot(self, slot, item):
        slots = 'carried_armor' if slot in self.armor_slots() else 'carried_weapons'
        dict_ = getattr(self, slots)
        current_item = dict_[slot]
        if current_item != None:
            self.storage.append(current_item)
        if item in self.storage:
            self.storage.remove(item)
        dict_[slot] = item

    def equip_weapon(self, weapon, hand='main_hand'):
        if weapon in self.storage:
            self.storage.remove(weapon)
        if weapon.size == 'twohanded':
            self.main_hand = weapon
            self.other_hand = weapon
        else:
            other = 'other_hand' if hand=='main_hand' else 'main_hand'
            if getattr(self, other).size == 'twohanded':
                setattr(self, other, None)
            setattr(self, hand, weapon)

    def disarm_weapon(self, hand):
        setattr(self, hand, None)

    def equip_armor(self, armor, slot):
        if armor in self.storage:
            self.storage.remove(armor)
        if self.carried_armor[slot] != None:
            self.storage.append(self.carried_armor[slot])
        self.carried_armor[slot] = armor

    def is_slot_active(self, slot):
        slots = 'carried_armor' if slot in self.armor_slots() else 'carried_weapons'
        slots = getattr(self, slots)
        return any(self.available_for_slot(slot)) or slots[slot] != None