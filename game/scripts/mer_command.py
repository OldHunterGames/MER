# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy

from mer_utilities import Observable, empty_card
from mer_quest import *


class Command(object):

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
        raise NotImplementedError()

    def description(self):
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()


class MenuCard(Card):

    def __init__(self, name=None, description=None,
                 label=None, image=None):
        self._name = name
        self._description = description
        self._image = image
        self._label = label
        self._context_data = dict()

    def image(self):
        if self._image is None or not renpy.exists(self._image):
            return empty_card()
        return self._image

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
        for key, value in kwargs.items():
            self._context_data[key] = value
        return self


class CardsMaker(Command):

    def __init__(self, dict_=None, card_cls=None):
        self.data = dict()
        self._context_data = dict()
        if card_cls is None:
            self.card_cls = MenuCard
        else:
            self.card_cls = card_cls
        if dict_ is not None:
            [self.add_entry(key, value) for key, value in dict_.items()]

    def _run(self):
        list_ = []
        for i in self.data.values():
            card = self.card_cls(**i)
            list_.append(card.set_context(self._context_data))
        return list_

    def add_entry(self, key, value):
        self.data[key] = value

    def remove_entry(self, key):
        try:
            del self.data[key]
        except KeyError:
            print 'No entry named %s' % key

    def set_context(self, **kwargs):
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
                employer=self.person, axis=key, **value))
        return list_
