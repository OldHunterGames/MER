# -*- coding: <UTF-8> -*-

import renpy.store as store
import renpy.exports as renpy


class BodyPart(object):


    def __init__(self, id_, owner):
        self.id = id_
        self.data = store.anatomy_data[id_]
        self._size = None
        self.wetness = 0
        self.harndess = 0
        self.stretch = 0
        self._count = None
        self.add(owner)

    def add(self, owner):
        func = self.data.get('on_add', lambda owner, instance: None)
        func(owner, self)

    @property
    def count(self):
        if self._count is not None:
            return self._count
        return self.data.get('count', 1)

    def size_str(self):
        return store.anatomy_sizes[self.id][self.size]
    
    @property
    def size(self):
        if self._size is not None:
            return self._size
        return self.data.get('size', 1)

    def set_size(self, value):
        self._size = value

    def add_count(self, value):
        if self._count is None:
            self._count = 0
        self._count += value
    
    @property
    def name(self):
        return self.data.get('name', 'NOname')
    
    @property
    def description(self):
        return self.data.get('description', 'No description')
    
    @property
    def sensitive(self):
        return self.data.get('sensitive', False)
    
    @property
    def stimulating(self):
        return self.data.get('stimulating', False)
    
    @property
    def penetration(self):
        return self.data.get('penetration')






class Anatomy(object):


    def __init__(self):
        self.parts = dict()


    def add_part(self, owner, part):
        self.parts[part] = BodyPart(part, owner)

    def feature_dependencies(self, owner, feature):
        for i in feature.dependencies:
            print i
            self.add_part(owner, i)