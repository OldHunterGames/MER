# -*- coding: UTF-8 -*-
import collections


class Skilled(object):
    tokens_relations = {'physique': 'might', 'mind': 'wisdom', 'spirit': 'spirit',
                        'agility': 'finesse'}

    def init_skilled(self):
        self.inner_resources = []
        self.luck_tokens = []
        self.focus_dict = collections.defaultdict(int)
        self.resources_deck = []
        self.active_resources = set()

    def drop_all_resources(self):
        for i in [i for i in self.active_resources]:
            self.active_resources.remove(i)

    def activate_resource(self, res):
        self.active_resources.add(res)

    def activate_resource_by_name(self, name):
        for i in self.resources_deck:
            if i.name == name:
                self.activate_resource(i)
                return

    def use_resource(self, res):
        self.active_resources.remove(res)
        if res.attribute == 'physique':
            self.tonus += 1
        elif res.attribute == 'mind':
            self.tonus -= 1

    def get_all_resources(self):
        return self.resources_deck

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
