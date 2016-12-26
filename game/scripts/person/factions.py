# -*- coding: UTF-8 -*-


class Faction(object):

    def __init__(self, owner, name, id_=None):
        self.name = name
        self.id = id_
        self.members = []
        self.event_type = 'faction'
        self.roles = {}
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


    def add_member(self, person):
        if not self.has_member(person):
            self.members.append(person)
            person.add_faction(self)

    def remove_member(self, person):
        for i in self.members:
            if person == i:
                self.members.remove(person)
            if person == self.owner:
                self.owner = None
        person.remove_faction(self)

    def has_member(self, person):
        if person in self.members:
            return True
        return False

    def get_members(self):
        list_ = [self.owner]
        roles = sorted(self.roles.keys())
        for key in roles:
            if self.roles[key] not in list_:
                list_.append(self.roles[key])
        members = [i for i in self.members if i not in list_]
        members_names = {}
        for i in members:
            if i.name not in members_names:
                members_names[i.name] = [i]
            else:
                members_names[i.name].append(i)
        keys = sorted(members_names.keys())
        for key in keys:
            for i in members_names[key]:
                list_.append(i)
        return list_

    def set_member_to_role(self, person, role):
        self.roles[role] = person
        self.add_member(person)

    def get_common_members(self):
        return [member for member in self.members if member != self.owner and member not in self.roles.values()]
