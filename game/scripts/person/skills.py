# -*- coding: UTF-8 -*-

skills_data = {
    'coding': 'mind',
    'sport': 'physique',
    'sex': 'sensitivity',
    'conversation': 'spirit',
}


class Skill(object):
    def __init__(self, owner, name, attribute='spirit'):
        self.owner = owner
        self.name = name
        self.attribute = attribute
        self.training = False
        self.expirience = False
        self.specialization = False
        self.talent = False
        self.inability = False
        self.expirience_slot = 0
        self._focus = 0

    @property
    def level(self):
        level = 0
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
        expirienced = {skill.expirience_slot: skill for skill in self.owner.skills if skill.expirience_slot != 0}
        if len(expirienced.keys()) > 1:
            max_skill = expirienced[max(expirienced.keys())]
            ind = self.owner.skills.index(max_skill)
            self.owner.skills[ind].specialization = True
            self.owner.specialized_skill = max_skill
    

    def profession(self, power=5):
        self.training = True
        self.expirience = True
        self.specialization = True
        self.expirience_slot = power
    def expert(self):
        slots = []
        self.training = True
        for skill in self.owner.skills:
            if skill.expirience:
                slots.append(skill.expirience_slot)
        minimum = 1
        while minimum in slots:
            minimum += 1
        self.expirience = True
        self.expirience_slot = minimum


    def attribute_value(self):
        return getattr(self.owner, self.attribute)


