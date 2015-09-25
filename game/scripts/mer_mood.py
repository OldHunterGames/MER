# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import renpy.store as store
import renpy.exports as renpy


class Moodlet(object):

    def __init__(self, owner):
        self.kind = "generic"  # Only one moodlet of each kind can be owned simultaneously by same person
        self.name = "lolz"
        self.owner = owner
        self.major = False      # True if moodlet is major, False if minor
        self.good = False       # True if moodlet is positive, False if negative
        self.natures = []       # Nature descriptors for moodlet origin like "pain" or "gain"
        self.report = ""        # Person will report this string when asked about mood


class MajorGood(Moodlet):

    def __init__(self, owner):
        super(MajorGood, self).__init__(owner)
        self.kind = "major"
        self.name = "Quadratish. Practish. Good."
        self.major = True
        self.good = True


class MajorBad(Moodlet):

    def __init__(self, owner):
        super(MajorBad).__init__(owner)
        self.kind = "major"
        self.name = "Kruglisch. Slojnisch. Bad."
        self.major = True


class MinorGood(Moodlet):

    def __init__(self, owner):
        super(MinorGood).__init__(owner)
        self.kind = "minor"
        self.name = "Simply good."
        self.good = True


class MinorBad(Moodlet):

    def __init__(self, owner):
        super(MinorBad).__init__(owner)
        self.kind = "minor"
        self.name = "Simply sad."



