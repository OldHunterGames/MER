# -*- coding: <UTF-8> -*-
import renpy.store as store
import renpy.exports as renpy
from copy import copy

events_list = []

def register_event(location, *args, **kwargs):
    event = Event( location, location)
    for key in kwargs.keys():
        if key == 'tags':
            event.tags = kwargs['tags']
        if key == 'unique':
            event.unique = kwargs['unique']
        if key == 'restrictions':
            event.restrictions = kwargs['restrictions']
    events_list.append(event)

def get_event(name):
    for event in events_list:
        if event.name == name:
            return event


def registration_check():
    l = renpy.get_all_labels()
    ll = []
    for label in l:
        if label.split('_')[0] == 'evn':
            ll.append(label)
    names = [event.name for event in events_list]
    bad = []
    for name in ll:
        if name not in names:
            bad.append(name)
    if len(bad) > 0:
        txt = ""
        for name in bad:
            txt += "label for event(%s) is created, but not registered\n"%(name)
        raise Exception(txt)
class Event(object):
    _game_ref = None
    def __init__(self, name, location):
        self.name = name
        self.goto = location     # RenPy location to start an event
        self.tags = []              # tags for filtering "gay", "lolicon", "bestiality", "futanari" etc
        self.restrictions = None
        self.unique = False         # Unique events shown once in a game instance
        self.seen = 0               # Number of times this event seen
        self.skipcheck = False
        self.target = None
    @classmethod
    def set_game_ref(cls, game):
        cls._game_ref = game
    @property
    def core(self):
        return self._game_ref
    def trigger(self, target=None, skipcheck=False):
        """
        On event activation
        """
        if self.seen > 0 and self.unique:
            return False
        self.skipcheck = skipcheck
        self.target = target
        if self.restrictions == 'player':
            try:
                if not target.player_controlled:
                    return False
            except AttributeError:
                return False
        elif self.restrictions != None and self.restrictions != target.event_type:
            return False
        result = renpy.call_in_new_context(self.goto, self)
        if result:
            self.seen += 1
        self.skipcheck = False
        self.target = None
        return result



class EVGeneric(Event):
    """
    Generic event for test
    """

    def __init__(self, env, location):
        super(EVUnique, self).__init__(env, location)
        self.goto = "evn_blank"
        self.natures = ["triggered", "turn_end", "faction"]


class EVUnique(Event):
    """
    Unique event for test
    """

    def __init__(self, env, location):
        super(EVGeneric, self).__init__(env, location)
        self.natures = ["triggered", "turn_end", "faction"]





