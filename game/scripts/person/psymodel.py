# -*- coding: <UTF-8> -*-

import renpy.store as store
import renpy.exports as renpy
from alignment import Alignment
import mer_utilities


needs_names = ["nutrition", "wellness", "comfort", "activity", "communication",
        "amusement", "prosperity", "authority", "ambition", "eros"]

DEFAULT_NEED_LEVEL = 2

satisfy_chances = {
        'nutrition': 'taste',
        'wellness': 'health',
        'comfort': 'bliss',
        'activity': 'adrenaline',
        'eros': 'orgasm',
        'communication': 'intimacy',
        'amusement': 'entertainment',
        'prosperity': 'gain',
        'authority': 'respect',
        'ambition': 'accomplishment'
    }


def init_needs():
    dict_ = {}
    for name in needs_names:
        dict_[name] = (Need(name))
    return dict_

class Chance(object):


    def __init__(self, id_, value, negative=False, on_remove=None, remove_on_refresh=False, attributed=False):

        self.id = id_
        self.value = value
        self.negative = negative
        self.on_remove = on_remove
        self.remove_on_refresh = remove_on_refresh
        self.attributed = False

class Need(object):
    def __init__(self, name):
        self.name = name
        self.tokens = []
        self.tension_points = []
        self.satisfied = False

    def use_token(self, token):
        self.tokens.append(token)

    def token_used(self, token):
        return token in self.tokens
    
    def set_satisfaction(self, value):
        if self.satisfied:
            return False
        roll = mer_utilities.roll(value, 6)
        if roll:
            self.satisfied = True
            return True
        else:
            return False

    def set_tension(self, point):
        if self.has_tension(point):
            return
        self.tension_points.append(point)

    def has_tension(self, point):
        return point in self.tension_points

    def reset(self):
        self.satisfied = False

    def remove_tension(self, point):
        self.tension_points.remove(point)

    def tensed(self):
        return len(self.tension_points) > 0


class PsyModel(object):

    def init_psymodel(self):

        self.alignment = Alignment()
        self._chances = {}
        self.needs = init_needs()

    def moral_action(self, **kwargs):
        # checks moral like person.check_moral, but instantly affect selfesteem
        result = self.check_moral(**kwargs)
        return result

    def check_moral(self, **kwargs):
        act = {'ardent': 1, 'reasonable': None, 'timid': -1}
        moral = {'good': 1, 'selfish': None, 'evil': -1}
        order = {'lawful': 1, 'conformal': None, 'chaotic': -1}
        target = kwargs.get('target')
        action_tones = {
            'activity': act.get(kwargs.get('activity')),
            'morality': moral.get(kwargs.get('morality')), 
            'orderliness': order.get(kwargs.get('orderliness'))
        }
        relation_tones = {}
        if target is not None:
            for key in action_tones.keys():
                relation_tones[key] = getattr(
                    self.relations(target), self.alignment.relation_binding[key])
        else:
            for key in action_tones.keys():
                relation_tones[key] = 0

       
        
        for key, value in action_tones.items():
            if value is not None:
                valself = getattr(self.alignment, key)
                valact = value
                result = None
                if target is not None:
                    fake_value = valact
                else:
                    fake_value = None
                tone = relation_tones[key]
                
                if tone == 0:
                    if valself + valact == 0:
                        chance_value = 1
                        result = 'bad'
                    elif abs(valself + valact) == 2:
                        chance_value = 3
                        result = 'good'
                else:
                    
                    if valself == 0:
                        if tone + valact == 0:
                            chance_value = 2
                            result = 'bad'
                        elif abs(tone + valact) == 2:
                            chance_value = 4
                            result = 'good'
                    elif valself == tone:
                        if valact + tone == 0:
                            chance_value = 5
                            result = 'good'
                    elif valself != tone:
                        if abs(valact + tone) == 2:
                            chance_value = 3
                            result = 'bad'

                if result is not None:
                    self.add_moral_chance(key, result, chance_value, fake_value)

    def add_moral_chance(self, axis, kind, chance_value, fake_value=None):
        chance_name = self.alignment.get_chance_name(axis, kind, fake_value)
        negative = {'good': False, 'bad': True}[kind]
        self.add_chance(chance_value, chance_name, negative)


    def add_chance(self, value, name, negative=False, on_remove=None, remove_on_refresh=True, attributed=False):
        self._chances[name] = Chance(name, value, negative, on_remove, remove_on_refresh, attributed)

    def remove_chance(self, name):
        try:
            self._chances[name].on_remove()
        except TypeError:
            pass
        del self._chances[name]

    def get_need(self, name):
        return self.needs[name]

    def need_level(self, name):
        return max(0, min(3, DEFAULT_NEED_LEVEL + self.count_modifiers(name)))

    def tense_need(self, name, point):
        if self.need_level(name) == 0:
            return
        need_obj = self.needs[name]
        if need_obj.has_tension(point):
            return
        else:
            self.add_chance(self.need_level(name), point, True,
                lambda: need_obj.remove_tension(point),
                False)
            need_obj.set_tension(point)

    def satisfy_need(self, name, value):
        if self.need_level(name) == 0:
            return
        need_obj = self.needs[name]
        satisfied = need_obj.set_satisfaction(value)
        if satisfied:
            self.add_chance(3, satisfy_chances[name])

    def get_chances(self, bad=False):
        dict_ = {}
        for key, value in self._chances.items():
            if value.negative is bad:
                dict_[key] = value
        return dict_.values()

    def get_all_chances(self):
        dict_ = {}
        for key, value in self._chances.items():
            dict_[key] = value
        return dict_.values()

    def reset_psych(self):
        for key, value in self._chances.items():
            if value.remove_onrefresh:
                self.remove_chance(key)
        for need in self.needs.values():
            need.reset()

    def clear_chances(self, only_good=False):
        for key, value in self._chances.items():
            if only_good:
                if value.negative:
                    continue
            self.remove_chance(key)

    def chances_left(self):
        return len(self._chances.keys())
