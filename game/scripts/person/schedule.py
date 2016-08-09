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
        if special == None:
            actions[key] = [z, action[2], action[3]]


class ScheduledAction(object):
    def __init__(self, actor, name, lbl, slot, store_name, single=True, special_values=None):
        self.actor = actor
        self.slot = slot
        self.name = name
        self.store_name = store_name
        self.lbl = lbl
        self.single = single
        self.special_values = collections.defaultdict(list)
        if special_values:
            for key in special_values:
                self.special_values[key] = special_values[key]

    def call(self):
        renpy.call_in_new_context(self.lbl, self)


    def call_on_remove(self):
        removal_label = self.lbl + '_' + 'remove'
        if renpy.has_label(removal_label):
            renpy.call_in_new_context(removal_label, self)


    def add_special_list_value(self, key, value):
        if value not in self.special_values[key]:
            self.special_values[key].append(value)



class Schedule(object):
    _default_world = 'core'
    _world = 'core'
    def __init__(self, person):
        self.actions = []
        self.owner = person
    @classmethod
    def set_world(cls, world):
        cls._world = world
    def add_action(self, action, single=True, special_values=None):
        action_ = Schedule._world + '_' + action
        if not renpy.has_label('shd_%s'%(action_)):
            print 'kek'
            action_ = Schedule._default_world + '_' + action

        if action_ in actions.keys():

            act = ScheduledAction(self.owner, actions[action_][2], actions[action_][0], actions[action_][1], action_, single, special_values)
            
            if act.slot != None:
                for a in self.actions:
                    if a.slot == act.slot:
                        self.remove_by_handle(a)
            
            self.actions.append(act)
        else:
            raise Exception("There is no %s action at current world(%s) or at core"%(action, self._world))
    def use_actions(self):
        to_remove = []
        for action in self.actions:
            action.call()
            if action.single:
                to_remove.append(action)
        for a in to_remove:
            self.remove_by_handle(a)
    def remove_by_handle(self, action):
        action.call_on_remove()
        self.actions.remove(action)
    def remove_action(self, action):
        for a in self.actions:
            if a.store_name == action:
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


    




