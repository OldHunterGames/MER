# -*- coding: UTF-8 -*-
from random import *
import collections

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import encolor_text

"""class Skill(object):

    def __init__(self, owner, id_):
        self.owner = owner
        self.id = id_
        self.data = store.skills_data[id_]
        self.training = False
        self.expirience = False
        self.specialization = False
        self.talent = False
        self.inability = False
        self.expirience_slot = 0
        self._focus = 0
    @property
    def name(self):
        return self.data['name']

    @property
    def attribute(self):
        return self.data['attribute']
    @property
    def level(self):
        level = 1
        if self.training:
            level += 1
        if self.expirience:
            level += 1
        if self.specialization:
            level += 1
        if self.talent:
            level += 1
        if self.inability:
            level -= 1
        return level

    @property
    def description(self):
        list_ = []
        if self.training:
            list_.append('training')
        if self.expirience:
            list_.append('expirience')
        if self.specialization:
            list_.append('specialization')
        if self.talent:
            list_.append('talent')
        if self.inability:
            list_.append('inability')
        return list_

    def show(self):
        return encolor_text(self.name, self.level)

    @property
    def focus(self):
        return min(5, self._focus)

    @focus.setter
    def focus(self, value):
        self._focus = value

    def set_focus(self):
        self.owner.focused_skill = self
        self.focus = 1

    def get_expirience(self, power):
        available_slots = [n for n in range(power, 0, -1)]
        for skill in self.owner.skills:
            if skill.expirience_slot in available_slots:
                available_slots.remove(skill.expirience_slot)
        if len(available_slots) > 0:
            self.expirience_slot = max(available_slots)
            self.expirience = True
        expirienced = {}
        for skill in self.owner.skills:
            if skill.expirience_slot != 0:
                expirienced[skill.expirience_slot] = skill
        if len(expirienced.keys()) > 1:
            max_skill = expirienced[max(expirienced.keys())]
            max_skill.specialize()


    def specialize(self):
        for i in self.owner.skills:
            i.specialization = False
        self.specialization = True
        self.owner.specialized_skill = self
    
    def profession(self, power=5):
        self.training = True
        self.get_expirience(power)

    def expert(self):
        slots = []
        self.training = True
        for skill in self.owner.skills:
            if skill.expirience:
                slots.append(skill.expirience_slot)
        minimum = 1
        while minimum in slots:
            minimum += 1
        self.get_expirience(minimum)

    def attribute_value(self):
        return getattr(self.owner, self.attribute)

    def is_focused(self):
        return self == self.owner.focused_skill"""


class Skilled(object):
    tokens_relations = {'physique': 'might', 'mind': 'wisdom', 'spirit': 'spirit',
                        'agility': 'finesse'}

    def init_skilled(self):
        self.inner_resources = []
        self.luck_tokens = []
        self.focus_dict = collections.defaultdict(int)
        self.resources_deck = []
        self.active_resources = []

    def drop_all_resources(self):
        for i in [i for i in self.active_resources]:
            self.resources_deck.append(i)
            self.active_resources.remove(i)

    def activate_resource(self, res):
        self.resources_deck.remove(res)
        self.active_resources.append(res)

    def activate_resource_by_name(self, name):
        for i in self.resources_deck:
            if i.name == name:
                self.activate_resource(i)
                return

    def use_resource(self, res):
        self.active_resources.remove(res)
        self.resources_deck.append(res)
        if res.attribute == 'physique':
            self.tonus += 1
        elif res.attribute == 'mind':
            self.tonus -= 1

    def get_all_resources(self):
        return self.resources_deck + self.active_resources

    def get_resource(self, attribute, difficulty, job=False):
        values = [
            i.value for i in self.active_resources if i.available(attribute)]
        if job:
            values = [i for i in values if i > difficulty]
        else:
            values = [i for i in values if i >= difficulty]
        try:
            min_value = min(values)
        except ValueError:
            values = [
                i.value for i in self.active_resources if i.available(attribute)]
            if job:
                values = [i for i in values if i > difficulty]
            else:
                values = [i for i in values if i >= difficulty]
            try:
                min_value = min(values)
            except ValueError:
                return None
            else:
                for i in self.active_resources:
                    if i.available(attribute) and i.value == min_value:
                        return i
        else:
            for i in self.active_resources:
                if i.available(attribute) and i.value == min_value:
                    return i

    def skill(self, attribute):
        attr = self.tokens_relations[attribute]
        value = self.count_modifiers(attr + '_skill')
        return max(0, min(3, value))

    def has_resource(self, id_):
        for i in self.active_resources:
            if i.name == id_:
                return i

    def add_card(self, name):
        # for test use
        for i in self.resources_deck:
            if i.name == name:
                self.activate_resource(i)
