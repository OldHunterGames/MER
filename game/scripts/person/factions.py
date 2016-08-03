# -*- coding: UTF-8 -*-

class Faction(object):
    def __init__(self, name):
        self.name = name
        self.owner = None
        self.members = []
        self.event_type = 'fraction'
    

    def set_owner(self, owner):
        self.owner = owner
        self.add_member(owner)

    
    def add_member(self, person):
        if person not in self.members:
            self.members.append(person)

    
    def remove_member(self, person):
        for i in self.members:
            if person == i:
                self.members.remove(person)
            if person == self.owner:
                self.owner = None

    
    def is_member(self, person):
        if person in self.members:
            return True
        return False
