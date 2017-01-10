# -*- coding: UTF-8 -*-
from random import *
import collections

import renpy.store as store
import renpy.exports as renpy
actions = {}
def register_actions():
    lbl_list = renpy.get_all_labels()
    l = []
    for label in lbl_list:
        lb = label.split('_')
        if lb[0] == 'shd':
            l.append(lb)
    for action in l:
        key = '{world}_{slot}_{name}'.format(world=action[1], slot=action[2], name=action[3])
        z = '_'
        z = z.join(action)
        try:
            special = action[4]
        except IndexError:
            special = None
        if action[1].lower() == 'none':
            action[1] = None
        if special is None:
            actions[key] = {'label': z, 'slot': action[2], 'name': action[3], 'world': action[1]}

def check_world(dict_):
    return dict_['world'] == Schedule._world

def check_availability(slot):
    act_dict = {}
    for key, value in actions.items():
        if check_world(value) and value['slot'] == slot:
            act_dict[key] = value
    return act_dict

def available_jobs():
    return check_availability('job')

def available_services():
    return check_availability('service')


class ScheduledAction(object):
    def __init__(self, actor, name, lbl, slot, store_name, single=True, special_values=None):
        self.actor = actor
        self.slot = slot
        self.name = name
        self.store_name = store_name
        self.lbl = lbl
        self.single = single
        self.special_values = dict()
        self.used = False
        self.spends = 0
        if special_values:
            for key in special_values:
                self.special_values[key] = special_values[key]

    def call(self):
        if not self.used:
            renpy.call_in_new_context(self.lbl, self)
            self.used = True



    def call_on_remove(self):
        removal_label = self.lbl + '_' + 'remove'
        if renpy.has_label(removal_label):
            renpy.call_in_new_context(removal_label, self)




class Schedule(object):
    _default_world = 'core'
    _world = 'core'
    def __init__(self, person):
        self.actions = []
        self.owner = person
    @classmethod
    def set_world(cls, world):
        cls._world = world
    def add_action(self, action, single=False, special_values=None, spends=0):
        world = Schedule._world
        action_ = Schedule._world + '_' + action
        if not renpy.has_label('shd_%s'%(action_)):
            action_ = Schedule._default_world + '_' + action
            world = Schedule._default_world
        if action_ in actions.keys():
            action = actions[action_]
            act = ScheduledAction(self.owner, world + '_' +action['name'], action['label'], action['slot'], action_, single, special_values)
            
            if act.slot is not None:
                if act.slot != 'service':
                    for a in self.actions:
                        if a.slot == act.slot:
                            self.remove_by_handle(a)
            act.spends = spends
            self.actions.append(act)
            return act
        else:
            raise Exception("There is no %s action at current world(%s) or at core"%(action, self._world))
    
    def use_actions(self):
        to_remove = []
        for action in self.actions:
            action.call()
            if action.single:
                to_remove.append(action)
            action.used = False
        for a in to_remove:
            self.remove_by_handle(a)
    
    def remove_by_handle(self, action):
        action.call_on_remove()
        self.actions.remove(action)
    
    def remove_action(self, action):
        for a in self.actions:
            if a.store_name == self._world + "_%s"%action:
                self.remove_by_handle(a)
    def remove_by_slot(self, slot):
        for a in self.actions:
            if a.slot == slot:
                self.remove_by_handle(a)


    def find_by_slot(self, slot):
        for a in self.actions:
            if a.slot==slot:
                return a


    def find_by_name(self, name):
        for a in self.actions:
            if a.store_name == name:
                return a

    def use_action(self, name):
        action = self.find_by_name(name)
        if action is None:
            return
        action.call()
        if action.single:
            self.remove_by_handle(action)

    def use_by_slot(self, slot):
        action = self.find_by_slot(slot)
        if action is None:
            return
        action.call()
        if action.single:
            self.remove_by_handle(action)


    




