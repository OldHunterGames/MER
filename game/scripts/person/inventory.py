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
        return [i for i in self.storage if i.equiped]

    def get_items(self, item_type):
        if item_type == 'all':
            return [i for i in self.storage]
        return [i for i in self.storage if i.type == item_type]

    def weapon_slots(self):
        return self.carried_weapons.keys()

    def armor_slots(self):
        return self.carried_armor.keys()

    @property
    def main_hand(self):
        return self._main_hand

    @main_hand.setter
    def main_hand(self, weapon):
        if not any([i == weapon for i in self.carried_weapons.values()]):
            for key in self.weapon_slots():
                if self.carried_weapons[key] is None and weapon.size in self.slots()[key]:
                    self.carried_weapons[key] = weapon
                    break
        self.add_item(weapon)
        weapon.equip()
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
        if not any([i == weapon for i in self.carried_weapons.values()]):
            for key in self.weapon_slots():
                if self.carried_weapons[key] is None and weapon.size in self.slots()[key]:
                    self.carried_weapons[key] = weapon
                    break
        self.add_item(weapon)
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
                if item.type == 'armor' and not item.equiped:
                    list_.append(item)
        else:
            for item in storage:
                if item.type != 'armor' and not item.equiped:
                    if item.size in slots[slot]:
                        list_.append(item)
        return list_

    def equip_on_slot(self, slot, item):
        slots = 'carried_armor' if slot in self.armor_slots() else 'carried_weapons'
        dict_ = getattr(self, slots)
        current_item = dict_[slot]
        if item is not None:
            item.equip()
        if current_item is not None:
            current_item.unequip()
            self.add_item(current_item)
        dict_[slot] = item

    def equip_weapon(self, weapon, hand='main_hand'):
        weapon.equip()
        self.add_item(weapon)
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
        try:
            weapon.unequip()
            if weapon.size == 'twohand':
                setattr(self, '_main_hand', None)
                setattr(self, '_other_hand', None)
        except AttributeError:
            pass
        setattr(self, '_'+hand, None)

    def equip_armor(self, armor, slot):
        self.add_item(armor)
        if self.carried_armor[slot] is not None:
            self.carried_armor[slot].unequip()
        self.carried_armor[slot] = armor
        armor.equip()

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

    def has_item(self, id_):
        for i in self.storage:
            if i.id == id_:
                return True
        return False

    def remove_item(self, item, value=1, return_item=True):
        get_item = None
        if isinstance(item, str):
            for i in self.storage:
                if i.id == item:
                    get_item = i
                    break
        else:
            for i in self.storage:
                if i == item:
                    get_item = i
                    break
        if get_item is not None:
            if hasattr(get_item, 'amount'):
                returned = get_item.decrease_amount(value)
                if get_item.amount <= 0:
                    self.storage.remove(get_item)
            else:
                self.storage.remove(get_item)
                returned = get_item
        for key, value in self.carried_weapons.items():
            if value == item:
                self.carried_weapons[key] = None
        for key, value in self.carried_armor.items():
            if value == item:
                self.carried_armor[key] = None
        if self.main_hand == item:
            self.main_hand = None
        if self.other_hand == item:
            self.other_hand = None
        if return_item:
            return returned

    def get_by_id(self, id_):
        for i in self.storage:
            if i.id == id_:
                return i

    def add_item(self, item, value=1):
        if value < 0:
            raise Exception('value < 0 use remove_item instead')
        if item is None:
            return
        if hasattr(item, 'amount'):
            current = self.get_by_id(item.id)
            if current is not None:
                current.increase_amount(value)
            else:
                self.storage.append(item)
                item.increase_amount(value-1)
        else:
            if item not in self.storage:
                self.storage.append(item)

    def weapon_slots(self):
        return self.carried_weapons

class InventoryWielder(object):

    def init_inventorywielder(self):
        self.inventory = Inventory()

    def equiped_items(self):
        return self.inventory.equiped_items()

    @property
    def items(self):
        return self.inventory.storage

    @property
    def main_hand(self):
        return self.inventory.main_hand

    @main_hand.setter
    def main_hand(self, weapon):
        self.inventory.main_hand = weapon

    @property
    def other_hand(self):
        return self.inventory.other_hand

    @other_hand.setter
    def other_hand(self, weapon):
        self.inventory.other_hand = weapon

    @property
    def armor(self):
        return self.inventory.carried_armor['overgarments']

    @armor.setter
    def armor(self, armor):
        self.inventory.equip_armor(armor, 'overgarments')

    def has_shield(self):
        try:
            main = self.inventory.main_hand
            other = self.inventory.other_hand
            if main.size == 'shield' or other.size == 'shield':
                return True
        except AttributeError:
            pass
        return False

    def equip_weapon(self, weapon, hand='main_hand'):
        self.inventory.equip_weapon(weapon, hand)

    def disarm_weapon(self, hand='main_hand'):
        self.inventory.disarm_weapon(hand)

    def add_item(self, item):
        self.inventory.storage.append(item)

    def equip_armor(self, item, slot):
        self.inventory.equip_armor(item, slot)

    def equip_item(self, item, slot):
        if item.type == 'armor':
            self.equip_armor(item, slot)
        elif item.type == 'weapon':
            self.equip_weapon(item, slot)

    def equip_on_slot(self, slot, item):
        self.inventory.equip_on_slot(slot, item)

    def weapons(self):
        return self.inventory.weapons()

    def has_item(self, item):
        return self.inventory.has_item(item)

    def remove_item(self, item, value=1, return_item=True):
        return self.inventory.remove_item(item, value, return_item)

    def add_item(self, item, value=1):
        self.inventory.add_item(item, value)

    def weapon_slots(self):
        return self.inventory.weapon_slots()

    def get_items(self, item_type):
        return self.inventory.get_items(item_type)

    @property
    def carried_weapons(self):
        return self.inventory.carried_weapons