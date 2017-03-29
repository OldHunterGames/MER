# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy

from mer_utilities import Observable, empty_card, get_files
from mer_quest import *


class Command(object):
    """Basic class for commands in mer"""
    #Maybe need special allocator for commands created in modules?
    def _run(self):
        raise NotImplementedError()

    @Observable
    def run(self):
        return self._run()

    @classmethod
    def add_observer(self, func):
        self.run.add_callback(func)


class Card(Command):

    def image(self):
        return empty_card()

    def description(self):
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()


class MenuCard(Card):
    """Basic class for card-styled menu cards"""
    def __init__(self, name=None, description=None,
                 label=None, image=None, id=None, **kwargs):
        self._name = name
        self._description = description
        self._image = image
        self._label = label
        self._context_data = dict()
        self._id = id
        self.set_context(**kwargs)

    def get_image(self):
        # testing image getting system
        path = 'images/%s/%s' % (self._image, self._id)
        images = get_files(path)
        try:
            img = images[0]
        except IndexError:
            img = None
        return img

    def image(self):
        img = self.get_image()
        if img is None:
            return empty_card()
        return img

    def description(self):
        return self._description

    def name(self):
        return self._name

    def label(self):
        return self._label

    def _run(self):
        return renpy.call_in_new_context(self._label, self)

    def __getattr__(self, key):
        try:
            value = self._context_data[key]
        except KeyError:
            raise AttributeError(key)
        else:
            return value

    def set_context(self, **kwargs):
        # sets not 'static' data if needed in card's label
        # mostly common called before run()
        for key, value in kwargs.items():
            self._context_data[key] = value
        return self


class CardsMaker(Command):
    """Factory for easy cards creation"""
    def __init__(self, dict_=None, card_cls=None):
        self.data = dict()
        self._context_data = dict()
        if card_cls is None:
            self.card_cls = MenuCard
        else:
            self.card_cls = card_cls
        if dict_ is not None:
            for key, value in dict_.items():
                if not value.get('hidden', False):
                    self.add_entry(key, value)

    def _run(self):
        list_ = []
        for key, value in self.data.items():
            card = self.card_cls(id=key, **value)
            list_.append(card.set_context(**self._context_data))
        return list_

    def add_entry(self, key, value):
        data = value[key]
        self.data[key] = data

    def remove_entry(self, key):
        try:
            del self.data[key]
        except KeyError:
            print 'No entry named %s' % key

    def set_context(self, **kwargs):
        # sets not 'static' data if needed in card's label
        # mostly common called before run()
        for key, value in kwargs.items():
            self._context_data[key] = value


class SatisfySex(Command):

    def __init__(self, target, value):
        self.target = target
        self.value = value

    def _run(self):
        pass


class MakeBasicRelationsQuests(Command):

    def __init__(self, person, *args, **kwargs):
        self.person = person
        self.data = kwargs

    def _run(self):
        list_ = []
        for key, value in store.basic_quests['relations'].items():
            list_.append(BasicRelationsQuest(
                employer=self.person, point=key, **value))
        return list_
