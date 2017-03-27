# -*- coding: UTF-8 -*-
import renpy.store as store

class Faction(object):

    def __init__(self, owner, name, type='unbound', id=None):
        self.name = name
        self.id = id
        self.members = []
        self.event_type = 'faction'
        self.type = type
        self.roles = {}
        self.roles_names = {}
        self.set_owner(owner)

    def set_owner(self, owner):
        self.add_member(owner)
        self.roles['owner'] = owner

    @property
    def owner(self):
        return self.roles.get('owner')

    @owner.setter
    def owner(self, owner):
        self.set_owner(owner)


    def add_member(self, person, role=False):
        if person is None:
            return
        if not self.has_member(person):
            self.members.append(person)
            person.set_faction(self)

    def remove_member(self, person):
        for i in self.members:
            if person == i:
                self.members.remove(person)
        for k, v in self.roles.items():
            if v == person:
                self.roles[k] == None
        person.remove_faction(self)

    def has_member(self, person):
        if person in self.members:
            return True
        return False

    def get_members(self):
        list_ = [(self.owner, 'owner')]
        roles = sorted(self.roles.keys())
        for key in roles:
            if (self.roles[key], key) not in list_:
                list_.append((self.roles[key], key))
        members = [i for i in self.members if i not in self.roles.values()]
        members_names = {}
        for i in members:
            if i.name not in members_names:
                members_names[i.name] = [i]
            else:
                members_names[i.name].append(i)
        keys = sorted(members_names.keys())
        for key in keys:
            for i in members_names[key]:
                list_.append((i, 'member'))
        return list_

    def set_member_to_role(self, person, role):
        self.roles[role] = person
        self.add_member(person)
        person.set_nickname(self.get_rol(role))

    def get_role_name(self, role):
        return store.factions_roles.get(role, role)

    def get_common_members(self):
        return [member for member in self.members if member != self.owner and member not in self.roles.values()]

    def get_role(self, role):
        try:
            role = self.roles[role]
        except KeyError:
            role = None
        return role
