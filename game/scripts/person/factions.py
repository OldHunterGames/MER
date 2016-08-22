# -*- coding: UTF-8 -*-
factions_list = []
class Faction(object):
    def __init__(self, owner, name, id_=None):
        self.name = name
        self.id = None
        self.members = []
        self.event_type = 'fraction'
        self.set_owner(owner)
        factions_list.append(self)
    
    
    def set_owner(self, owner):
        self.add_member(owner)
        self.owner = owner

    
    def add_member(self, person):
        if not self.has_member(person):
            self.members.append(person)

    def remove_member(self, person):
        for i in self.members:
            if person == i:
                self.members.remove(person)
            if person == self.owner:
                self.owner = None

    def has_member(self, person):
        if person in self.members:
            return True
        return False



