# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import renpy.store as store
import renpy.exports as renpy


class Meter(object):

    def __init__(self, owner):
        self.name = ""
        self.owner = owner
        self.lng = 3 + owner.attribute("spirit")
        self.bar = []
        for i in range(self.lng):
            self.bar.append(0)

    def increase(self, number=1):
        i = number
        if 0 in self.bar:
            self.bar[self.bar.index(0)] = 1
            i -= 1
        elif -1 in self.bar:
            self.bar[self.bar.index(-1)] = 0
            i -= 1
        else:
            return
        if i <= 0:
            return
        else:
            self.increase(i)

    def decrease(self, number=1):
        i = number
        if 0 in self.bar:
            self.bar[self.bar.index(0)] = -1
            i -= 1
        elif 1 in self.bar:
            self.bar[self.bar.index(1)] = -1
            i -= 1
        else:
            return
        if i <= 0:
            return
        else:
            self.decrease(i)

    def state(self):
        if 0 not in self.bar:
            if 1 not in self.bar:
                state = "downgrade"
            elif -1 not in self.bar:
                state = "upgrade"
            else:
                state = "stable"
        else:
            state = "stable"

        return state








