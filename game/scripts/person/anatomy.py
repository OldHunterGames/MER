# -*- coding: <UTF-8> -*-

import renpy.store as store
import renpy.exports as renpy


class BodyPart(object):


    def __init__(self, id_, owner):
        self.basis = None





class Anatomy(object):


    def __init__(self):
        self.parts = dict()


    def add_part(self, owner, part):
        self.parts[part] = BodyPart(part, owner)

    def feature_dependencies(self, owner, feature):
        for i in feature.dependencies:
            self.add_part(owner, i)