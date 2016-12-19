# -*- coding: UTF-8 -*-
import collections


class Inventory(object):

    def __init__(self):
        self.carried_weapons = collections.OrderedDict([('harness', None), ('belt1', None),
                                                        ('belt2', None), ('armband', None), ('ankleband', None)])
        self.carried_armor = collections.OrderedDict(
            [('underwear', None), ('garments', None), ('overgarments', None)])
        self._main_hand = None
        self._other_hand = None
        self.storage = []

    def equiped_items(self):
        list_ = self.weapons()
        for value in self.carried_armor.values():
            if value is not None:
                list_.append(value)
        return list_

    def weapon_slots(self):
        return self.carried_weapons.keys()

    def armor_slots(self):
        return self.carried_armor.keys()

    @property
    def main_hand(self):
        return self._main_hand

    @main_hand.setter
    def main_hand(self, weapon):
        if weapon in self.storage:
            self.storage.remove(weapon)
        self.disarm_weapon('main_hand')
        if weapon.size == 'twohand':
            self.disarm_weapon('other_hand')
            self._other_hand = weapon
        self._main_hand = weapon

    @property
    def other_hand(self):
        return self._other_hand

    @other_hand.setter
    def other_hand(self, weapon):
        if weapon in self.storage:
            self.storage.remove(weapon)
        self.disarm_weapon('other_hand')
        if weapon.size == 'twohand':
            self.disarm_weapon('main_hand')
            self._main_hand = weapon
        self._other_hand = weapon

    def weapons(self):
        list_ = []
        if self.main_hand is not None:
            list_.append(self.main_hand)
        if self.other_hand is not None:
            list_.append(self.other_hand)
        return list(set(list_))

    def slots(self):
        return {
            'belt1': ['offhand', 'versatile'],
            'belt2': ['offhand', 'versatile'],
            'harness': ['offhand', 'versatile', 'shield', 'twohand'],
            'armband': ['offhand'],
            'ankleband': ['offhand']
        }

    def available_for_slot(self, slot, storage=None):
        if storage is None:
            storage = self.storage
        slots = self.slots()
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
        if current_item is not None:
            self.storage.append(current_item)
        if item in self.storage:
            self.storage.remove(item)
        dict_[slot] = item

    def equip_weapon(self, weapon, hand='main_hand'):
        if weapon in self.storage:
            self.storage.remove(weapon)
        if weapon.size == 'twohand':
            self.main_hand = weapon
            self.other_hand = weapon
        else:
            other = 'other_hand' if hand == 'main_hand' else 'main_hand'
            try:
                if getattr(self, other).size == 'twohand':
                    setattr(self, other, None)
            except AttributeError:
                pass
            setattr(self, hand, weapon)

    def disarm_weapon(self, hand):
        weapon = getattr(self, hand)
        
        if weapon not in self.storage and weapon not in self.equiped_weapons().values():
            self.storage.append(weapon) 
        try:
            weapon.unequip()
            if weapon.size == 'twohand':
                setattr(self, '_main_hand', None)
                setattr(self, '_other_hand', None)
        except AttributeError:
            pass
        setattr(self, '_'+hand, None)

    def equip_armor(self, armor, slot):
        if armor in self.storage:
            self.storage.remove(armor)
        if self.carried_armor[slot] is not None:
            self.storage.append(self.carried_armor[slot])
        self.carried_armor[slot] = armor

    def is_slot_active(self, slot):
        slots = 'carried_armor' if slot in self.armor_slots() else 'carried_weapons'
        slots = getattr(self, slots)
        return any(self.available_for_slot(slot)) or slots[slot] is not None

    def visible_weapon(self):
        weapons = self.carried_weapons
        if weapons['harness'] is not None or weapons[
                'belt1'] is not None or weapons['belt2'] is not None:
            return True
        return False

    def equiped_weapons(self):
        return dict([(slot, weapon) for slot,
                     weapon in self.carried_weapons.items() if weapon is not None])

    def in_hands(self, item):
        if self.main_hand == item or self.other_hand == item:
            return True
        return False
