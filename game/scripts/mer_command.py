# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy

from mer_utilities import Observable, empty_card

class Command(object):

    
    def _run(self):
        return NotImplemented

    @Observable
    def run(self):
        return self._run()

    @classmethod
    def add_observer(self, func):
        self.run.add_callback(func)


class Card(Command):


    def image(self):
        return NotImplemented

    def description(self):
        return NotImplemented

    def name(self):
        return NotImplemented


class MenuCard(Card):


    def __init__(self, name, description, label, image, *args, **kwargs):
        self._name = name
        self._description = description
        self._image = image
        self._label = label

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


class RelationsCard(MenuCard):


    def __init__(self, target, player, *args, **kwargs):
        super(RelationsCard, self).__init__(*args, **kwargs)
        self.target = target
        self.player = player


class MakeCardsFromDict(Command):


    def __init__(self, dict):
        pass        


class MakeRelationsCards(Command):


    def __init__(self, target, player):
        self.target = target
        self.player = player

    def _run(self):
        return [RelationsCard(self.target, self.player, 
            i['name'], i['description'], i['label'], i['image']) for i in store.relations_cards]



class SatisfySex(Command):


    def __init__(self, target, value):
        self.target = target
        self.value = value

    def _run(self):
        pass
