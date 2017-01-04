# -*- coding: <UTF-8> -*-
import random

def encolor_text(text, value):
    if isinstance(value, str):
        colors = {'red': 'ff0000', 'green': '00ff00'}
    else:
        colors = ['ff0000', 'ff00ff', '00ffff',
            '0000FF', '00ff00', 'DAA520', '000000']
        if value < 0:
            value = 0
        if value > 6:
            value = 6
    
    return '{b}{color=#%s}%s{/color}{/b}' % (colors[value], text)


def default_avatar_path():
    return 'images/avatar/none.jpg'

def weighted_random(pairs):
   total = sum(w for c, w in pairs)
   r = random.uniform(0, total)
   upto = 0
   for c, w in pairs:
        if upto + w >= r:
            return c
        upto += w

def roll(value, max_):
    dice = random.randint(1, max_)
    if value < dice:
        return False
    return True

def change_needs(person, satisfy, tense, result):
    if result < 0:
        return
    for i in tense:
        getattr(person, i).set_tension()
    if result > 0:
        for i in satisfy:
            getattr(person, i).set_satisfaction(result)


def get_max_skill(person, skills):
    list_ = [person.skill(i) for i in skills]
    max_level = max([i.level for i in list_])
    for j in [i for i in list_]:
        if j.level < max_level:
            list_.remove(j)
    return random.choice(list_)



class Observable(object):


        def __init__(self, func, instance=None, observers=None):
            self.func = func
            self.instance = instance
            self.observers = [] if observers is None else observers

        def __get__(self, obj, cls=None):
            if obj is None:
                return self
            else:
                func = self.func.__get__(obj, cls)
            return Observable(func, obj, self.observers)

        def __call__(self, *args, **kwargs):
            result = self.func(*args, **kwargs)
            for observer in self.observers:
                observer(self.instance)
            return result

        def add_callback(self, callback):
            self.observers.append(callback)
