# -*- coding: UTF-8 -*-


class Buff(object):
    def __init__(self, owner_person, name, modifiers_dict, slot, time=1):
        self.owner = owner_person
        self.name = name
        self.modifiers = modifiers_dict
        self.slot = slot
        self.time = time
        self.owner.add_modifier(name, modifiers_dict, self, self.slot)

    def tick_time(self):
        try:
            self.time -= 1
            if self.time < 1:
                self.remove()
        except TypeError:
            pass

    def remove(self):
        self.owner.modifiers.remove_modifier(self)