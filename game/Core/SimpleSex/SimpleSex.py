from random import *

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import make_sex_card


class SimpleSex(object):


    def __init__(self, player, participants):

        self.participants = [SexParticipant(player[0], player[1])]
        self.participants.extend([SexParticipant(i[0], i[1]) for i in participants])
        self.target_picker = None
        renpy.call_in_new_context('lbl_simplesex', self)

    def set_target_picker(self, participant):
        self.target_picker = participant

    def set_target(self, target):
        if self.target_picker is not None:
            self.target_picker.set_target(target)

    def npc_act(self):
        for i in self.participants:
            if i.modus == 'wishful':
                i.set_target(self.participants[0])
                i.act(self.get_npc_card(i))
                renpy.call_screen('sc_show_npc_turn', i)

    def get_npc_card(self, participant):
        shuffle(participant.actions)
        actions = participant.actions[0:5]
        return max(actions, key=lambda action: action.calc_result(participant, participant.target)[0])


class SexParticipant(object):


    def __init__(self, person, modus):
        
        self.person = person
        self.modus = modus
        self.ratings = []
        self.actions = []
        self.target = None
        self.action = None

    def get_rating_description(self):
        return 'Lorem Ipsum'
    
    def acted(self):
        if self.modus == 'unwilling':
            return True
        else:
            return self.action is not None

    def act(self, action):
        self.action = action
        action.use(self, self.target)

    def avatar(self):
        ava = renpy.display.im.Scale(self.person.avatar_path, 200, 200)
        if self.acted():
            return renpy.display.im.Grayscale(ava)
        return ava


    def set_target(self, target):
        self.target = target

    def __getattr__(self, key):
        try:
            value = getattr(self.person, key)
        except AttributeError:
            raise AttributeError(key)
        else:
            return value

    def fix_rating(self, rating):
        self.ratings.append(rating)

    def gender(self):
        gender = self.person.gender
        if gender == 'shemale' or gender == 'female':
            return 'female'
        else:
            return 'male'

class SexEffect(object):

    INITIAL_RATING = 0
    def __init__(self, active_organ, passive_organ, suite, quality, contact_type, name):
        self.active = active_organ
        self.passive = passive_organ
        self.suite = suite
        self.quality = quality
        self._image = None
        self.contact_type = contact_type

    def image(self):
        if self._image is None:
            self._image = make_sex_card(self.quality+2, self.suite, self.contact_type)
        return self._image

    def use(self, actor, taker):
        actor_rating, target_rating = self.calc_result(actor, taker)
        actor.fix_rating(actor_rating)
        taker.fix_rating(target_rating)

    def _calc_orientation(self, actor, taker, actor_rating, target_rating):
        actor_rating = self._change_rating(actor_rating, actor.count_modifiers(taker.gender()))
        target_rating = self._change_rating(target_rating, taker.count_modifiers(actor.gender()))
        return actor_rating, target_rating

    def _calc_suite(self, actor, taker, actor_rating, target_rating):
        actor_value = actor.sexual_suite['active'][self.suite]
        actor_rating = self._change_rating(actor_rating, actor_value)
        taker_value = taker.sexual_suite['active'][self.suite]
        target_rating = self._change_rating(target_rating, taker_value)
        return actor_rating, target_rating


    def _calc_penetration(self, actor, taker, actor_rating, target_rating):
        actor_organ = actor.get_body_part(self.active)
        taker_organ = taker.get_body_part(self.passive)
        if actor_organ.penetration == 'penetrative':
            penetrator = actor_organ
            penetrator_owner = 'actor_rating'
        elif taker_organ.penetration == 'penetrative':
            penetrator = taker_organ
            penetrator_owner = 'target_rating'
        else:
            penetrator = None

        if actor_organ.penetration == 'receiving':
            receiver = actor_organ
            receiver_owner = 'actor_rating'
        elif taker_organ.penetration == 'receiving':
            receiver = taker_organ
            receiver_owner = 'target_rating'
        else:
            receiver = None

        if penetrator is not None and receiver is not None:
            if (penetrator.size == 0 or receiver.size == 0) and penetrator.size != receiver.size:
                value = self._calc_zero_size(penetrator, receiver, penetrator_owner, receiver_owner)
                locals()[value] = self._change_rating(locals()[value], 1)
            friction = penetrator.size - receiver.size
            wetness = max(penetrator, receiver, key=lambda organ: organ.wetness)
            if friction < 0:
                locals()[penetrator_owner] = self._change_rating(locals()[penetrator_owner], -1)
            elif friction > 0:
                locals()[penetrator_owner] = self._change_rating(locals()[penetrator_owner], 1)
                receiver.stretch += friction
                if friction < wetness+1:
                    locals()[receiver_owner] = self._change_rating(locals()[receiver_owner], 1)
                elif friction > wetness+2:
                    locals()[receiver_owner] = self._change_rating(locals()[receiver_owner], -1)
        return actor_rating, target_rating



    def _calc_zero_size(self, penetrator, receiver, penetrator_owner, receiver_owner):
        if penetrator.size == 0:
            return 'target_rating'
        elif receiver.size == 0:
            return 'actor_rating'

    def _change_rating(self, value, new_value):
        if value < 0:
            return value
        else:
            return value + new_value

    def calc_result(self, actor, taker):
        actor_rating = self._change_rating(self.INITIAL_RATING, self.quality)
        target_rating = self._change_rating(self.INITIAL_RATING, self.quality) 
        actor_rating, target_rating = self._calc_orientation(actor, taker, actor_rating, target_rating)
        actor_rating, target_rating = self._calc_suite(actor, taker, actor_rating, target_rating)
        actor_rating, target_rating = self._calc_penetration(actor, taker, actor_rating, target_rating)
        return actor_rating, target_rating

test1 = SexEffect('vagina', 'penis', 'bizarre', 2, 'afuck', 'test1')