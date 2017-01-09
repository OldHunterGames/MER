# -*- coding: UTF-8 -*-
from random import *
import collections

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import encolor_text

class Skill(object):

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
        return self == self.owner.focused_skill


class Skilled(object):
    _tokens_relations = {'physique': 'stamina', 'mind': 'idea', 'spirit': 'willpower',
        'agility': 'grace', 'sensitivity': 'emotion'}
    def init_skilled(self):
        self.skills = []
        self.specialized_skill = None
        self.focused_skill = None
        self.skills_used = []
        self.inner_resources = []
        self.luck_tokens = []
        self.focus_dict = collections.defaultdict(int)
        self.used_inner_resources = []

    def add_inner_resource(self, name, attribute, value=1):
        if attribute == 'focus':
            self.add_focus(name)
        elif name == 'luck':
            self.add_luck(value)
        else:
            self.inner_resources.append({'name': name, 'attribute': attribute, 'value': value})

    def get_related_token(self, skill_name):
        return self._tokens_relations[self.skill(skill_name).attribute]

    def add_luck(self, value):
        self.luck_tokens.append(value)

    def has_resources(self):
        return (any(self.inner_resources) or any([i > 0 for i in self.focus_dict.values()]) or
            len(self.luck_tokens) > 0)

    def use_resource(self, resource):
        if resource['name'] == 'insight':
            self.use_focus(resource['attribute'])
        else:
            self.inner_resources.remove(resource)

    def get_min_resource_token(self, skill_name, difficulty):
        token = None
        for i in self.inner_resources:
            if i['attribute'] == self.skill(skill_name).attribute and i['value'] >= difficulty:
                difficulty = i['value']
                token = i
        return token

    def get_min_luck(self, difficulty):
        value = 0
        try:
            value = min([i for i in self.luck_tokens if i >= difficulty])
        except ValueError:
            return value
        return value

    def use_luck(self, value):
        self.luck_tokens.remove(value)

    def apply_determination(self, resource, determination):
        resource['value'] += 1
        self.use_resource(determination)

    def can_upgrade_resource(self, resource, determination):
        if determination is None:
            return
        return resource['value'] < determination['value']

    def unite_determinations(self, determination1, determination2):
        value = max(determination1['value'], determination2['value'])
        value += 1
        self.add_inner_resource('determination', 'any', value)
        self.use_resource(determination1)
        self.use_resource(determination2)

    def add_focus(self, name):
        self.focus_dict[name] += 1

    def use_focus(self, name):
        try:
            del self.focus_dict[name]
        except KeyError:
            pass

    def get_focus(self, name):
        return self.focus_dict[name]

    def get_all_skills(self):
        return [i for i in self.skills]

    def skill(self, skill_id):
        skill = None
        for i in self.skills:
            if i.id == skill_id:
                skill = i
                return skill

        if skill_id in store.skills_data:
            skill = Skill(self, skill_id)
            self.skills.append(skill)
            return skill
        else:
            raise Exception("No skill named %s in skills_data" % (skill_id))

    def use_skill(self, id_):
        if isinstance(id_, Skill):
            self.skills_used.append(id_)
        else:
            self.skills_used.append(self.skill(id_))

    def get_used_skills(self):
        l = []
        for skill in self.skills_used:
            if isinstance(skill, Skill):
                l.append(skill)
            else:
                l.append(self.skill(skill))
        return l

    def calc_focus(self):
        self.used_inner_resources = []
        if self.focused_skill:
            if self.focused_skill in self.get_used_skills():
                self.focused_skill.focus += 1
                self.skills_used = []
                return
        try:
            self.focused_skill.focus = 0
        except AttributeError:
            pass

        if len(self.skills_used) > 0:
            from collections import Counter
            counted = Counter()
            for skill in self.get_used_skills():
                counted[skill.id] += 1
            maximum = max(counted.values())
            result = []
            for skill in counted:
                if counted[skill] == maximum:
                    result.append(skill)
            self.skill(choice(result)).set_focus()
        else:
            self.focused_skill = None
        self.skills_used = []

    def use_inner_resource(self, resource):
        self.used_inner_resources.append(resource)

    def has_inner_resource(self, resource):
        return resource not in self.used_inner_resources