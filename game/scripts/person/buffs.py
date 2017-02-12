# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy

class Buff(object):

    def __init__(self, owner_person, id_, time=1):
        self.data = store.buffs_dict[id_]
        self.id = id_
        self.owner = owner_person
        self.storage = owner_person.get_buff_storage()
        if self.slot is not None:
            self.owner.remove_buff_by_slot(self.slot)
        self.time = time
        self.storage.append(self)
        self.owner.add_modifier(self.id, self.modifiers, self, self.slot)

    def color(self):
        if all([i > 0 for i in self.modifiers.values()]):
            return 4
        elif all([i < 0 for i in self.modifiers.values()]):
            return 0
        else:
            return 2

    @property
    def name(self):
        return self.data['name']
    @property
    def slot(self):
        try:
            slot = self.data['slot']
        except KeyError:
            slot = None
        return slot
        
    @property
    def modifiers(self):
        return self.data['modifiers']

    def tick_time(self):
        try:
            self.time -= 1
            if self.time < 1:
                self.remove()
        except TypeError:
            pass

    def remove(self):
        self.owner.remove_modifier(self)
        self.owner._buffs.remove(self)
