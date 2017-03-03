# -*- coding: UTF-8 -*-

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import empty_card


class ShiftRelations(object):
    _tokens_relations = {
        'conquest': 'congruence',
        'convention': 'distance',
        'contribution': 'fervor'
    }
    _needs = {
                'conquest': 'authority',
                'convention': 'ambition',
                'contribution': 'communication'
            }

    def __init__(self, player, person):

        self.token = person.token
        self.person = person
        self.player = player
        if self.token not in self._tokens_relations.keys():
            renpy.call_in_new_context('lbl_communicate', person)
        else:
            self.axis = self._tokens_relations[self.token]
            self.left = empty_card()
            self.middle = empty_card()
            self.right = empty_card()
            self.relations = person.player_relations()
            renpy.call_in_new_context('lbl_shift_relations', self)

    def act_left(self):
        self.person.player_relations().change(self.axis, '-')
    
    def is_left_active(self):
        return self.person.player_relations().axis[self.axis] != -1

    def act_right(self):
        self.person.player_relations().change(self.axis, '+')

    def is_right_active(self):
        return self.person.player_relations().axis[self.axis] != 1

    def act_middle(self):
        self.player.satisfy_need(self._needs[self.token], 4)

    def left_card(self):
        if self.is_left_active():
            return empty_card()
        else:
            return renpy.display.im.Grayscale(empty_card())

    def right_card(self):
        if self.is_right_active():
            return empty_card()
        else:
            return renpy.display.im.Grayscale(empty_card())

    def middle_card(self):
        return empty_card()

    def left_text(self):
        value = self.relations.axis[self.axis]
        if self.is_left_active():
            return getattr(self.relations, 'show_%s'%self.axis)(False, False, value-1)
        else:
            return getattr(self.relations, 'show_%s'%self.axis)(False)

    def right_text(self):
        value = self.relations.axis[self.axis]
        if self.is_right_active():
            return getattr(self.relations, 'show_%s'%self.axis)(False, False, value+1)
        else:
            return getattr(self.relations, 'show_%s'%self.axis)(False)

    def middle_text(self):
        return self.player.get_need(self._needs[self.token]).name