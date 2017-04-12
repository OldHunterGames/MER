from random import *

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import make_sex_card, encolor_text
from mer_command import SatisfySex
from mer_quest import Quest, QuestTarget


def make_cards(dict_):
    cards = []
    for key, value in dict_.items():
        for i in range(-1, 2):
            for n in value['suite']:
                cards.append(SexEffect(value['implement'], value['target'],
                                       n, i, value['action_type'], value['name']))
    return cards


class SimpleSex(object):

    actions = None

    def __init__(self, *args):
        if len(args) < 2 or len(args) > 5:
            raise Exception('Incorrect participants count')
        if self.actions is None:
            self.actions = make_cards(store.simple_sex_actions_data)
        self.participants = [SexParticipant(participant[0], participant[1]) for participant in args]
        self.target_picker = None
        self.target = None
        self.current_card = None
        self.current_actions = []
        self.npc_act()
        self.active_act()
        renpy.call_screen('sc_simplesex_final', self)

    def get_player(self):
        return next((i for i in self.participants if i.player_controlled))

    def set_target(self, target):
        self.target = target

    def swap(self, new_card):
        index = self.current_actions.index(new_card)
        self.current_actions.remove(new_card)
        self.current_actions.insert(index, self.current_card)
        self.set_card(new_card)

    def active_act(self):
        actives = self.get_actives()
        while len(actives) > 0:
            if len(actives) < 2:
                self.set_target_picker(self.get_actives()[0])
            if len(self.participants) > 2:
                renpy.call_screen('sc_simplesex_picktarget', self)
            else:
                for i in self.participants:
                    if i != self.target_picker:
                        self.set_target(i)
            actions = self.get_actions(self.target_picker, self.target)
            self.current_actions = actions[0:4]
            self.set_card(actions[4])
            renpy.call_screen('sc_pick_sexaction', self)
            actives.remove(self.target_picker)
            self.target_picker.act(self.current_card, self.target)
            self.target_picker.lock()
            self.clear()

    def get_actives(self):
        return [i for i in self.participants if i.modus == 'controlled' and not i.acted()]

    def set_target_picker(self, participant):
        self.target_picker = participant
        self.set_target(None)
        targets = self.available_targets(participant)
        if len(targets) > 1:
            return
        else:
            self.set_target(targets[0])

    def npc_act(self):
        for i in self.participants:
            if i.modus == 'wishful':
                self.target_picker = i
                target = self.get_npc_target(i)
                self.target = target
                card = self.get_npc_card(i, target)
                self.set_card(card)
                i.act(card, target)
                renpy.call_screen('sc_show_turn', self)
                i.lock()
                self.clear()

    def get_actions(self, participant, target):
        shuffle(self.actions)
        actions = [i for i in self.actions if i.can_be_used(
            participant, target)]
        actions = actions[0:5]
        return actions

    def get_npc_card(self, participant, target):
        actions = self.get_actions(participant, target)
        return max(actions, key=lambda action: action.calc_result(participant, target)[0])

    def get_npc_target(self, participant):
        participants = [i for i in self.participants]
        participants.remove(participant)
        return max(participants, key=lambda participant: participant.allure())

    def available_targets(self, participant):
        targets = [i for i in self.participants]
        targets.remove(participant)
        return targets

    def clear(self):
        self.target = None
        self.target_picker = None
        self.current_card = None
        self.current_actions = []

    def set_card(self, card):
        self.current_card = card

    def get_target_rating(self):
        value = self.current_card.calc_result(
            self.target_picker, self.target)[1]
        return self.target.get_rating_description(value)

    def get_actor_rating(self):
        value = self.current_card.calc_result(
            self.target_picker, self.target)[0]
        return self.target_picker.get_rating_description(value)

    def calc_result(self, participant):
        rating = participant.calc_rating()

        return encolor_text(store.sex_quality_rate[rating], rating)

    def finish(self):
        for i in self.participants:
            SatisfySex(i, i.calc_rating()).run()

    def get_results(self):
        return [(i.person, i.calc_rating()) for i in self.participants]


class SexParticipant(object):

    def __init__(self, person, modus):

        self.person = person
        self.modus = modus
        self.ratings = []
        self.actions = []

        self._acted = False

    def calc_rating(self):
        try:
            max_ = max(self.ratings)
        except ValueError:
            return 0
        if self.ratings.count(max_) > 1:
            max_ += 1
        return max_

    def get_rating_description(self, value=0):
        return encolor_text(store.sex_quality_rate[value], value)

    def acted(self):
        if self.modus == 'unwilling':
            return True
        else:
            return self._acted

    def lock(self):
        self._acted = True

    def act(self, action, target):
        self.action = action
        action.use(self, target)

    def avatar(self, size=None, ungray=False):
        if size is None:
            size = (200, 200)
        ava = renpy.display.im.Scale(self.person.avatar_path, *size)
        if self.acted() and not ungray:
            return renpy.display.im.Grayscale(ava)
        return ava

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
        self.name = name
        self.passive = passive_organ
        self.suite = suite
        self.quality = quality
        self.contact_type = contact_type

    def image(self, size=None):
        return make_sex_card(self.quality + 2, self.suite, self.contact_type, size)

    def can_be_used(self, actor, taker):
        actor_organ = actor.has_body_part(self.active)
        taker_organ = taker.has_body_part(self.passive)
        return actor_organ and taker_organ

    def use(self, actor, taker):
        actor_rating, target_rating = self.calc_result(actor, taker)
        actor.fix_rating(actor_rating)
        taker.fix_rating(target_rating)

    def _calc_orientation(self, actor, taker, actor_rating, target_rating):
        actor_rating = self._change_rating(
            actor_rating, actor.sexual_orientation[taker.gender()])
        target_rating = self._change_rating(
            target_rating, taker.sexual_orientation[actor.gender()])
        return actor_rating, target_rating

    def _calc_suite(self, actor, taker, actor_rating, target_rating):
        actor_value = actor.sexual_suite['active'][self.suite]
        actor_rating = self._change_rating(actor_rating, actor_value)
        taker_value = taker.sexual_suite['receiving'][self.suite]
        target_rating = self._change_rating(target_rating, taker_value)
        return actor_rating, target_rating

    def _calc_penetration(self, actor, taker, actor_rating, target_rating):
        if self.passive is None or self.active is None:
            return actor_rating, target_rating
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
                value = self._calc_zero_size(
                    penetrator, receiver, penetrator_owner, receiver_owner)
                locals()[value] = self._change_rating(locals()[value], 1)
            friction = penetrator.size - receiver.size
            wetness = max(penetrator, receiver,
                          key=lambda organ: organ.wetness)
            if friction < 0:
                locals()[penetrator_owner] = self._change_rating(
                    locals()[penetrator_owner], -1)
            elif friction > 0:
                locals()[penetrator_owner] = self._change_rating(
                    locals()[penetrator_owner], 1)
                receiver.stretch += friction
                if friction < wetness + 1:
                    locals()[receiver_owner] = self._change_rating(
                        locals()[receiver_owner], 1)
                elif friction > wetness + 2:
                    locals()[receiver_owner] = self._change_rating(
                        locals()[receiver_owner], -1)
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
        actor_rating, target_rating = self._calc_orientation(
            actor, taker, actor_rating, target_rating)
        actor_rating, target_rating = self._calc_suite(
            actor, taker, actor_rating, target_rating)
        actor_rating, target_rating = self._calc_penetration(
            actor, taker, actor_rating, target_rating)
        return actor_rating, target_rating

test1 = SexEffect('vagina', 'penis', 'bizarre', 0, 'afuck', 'test1')


class SexualPleasureTarget(QuestTarget):
    """Target for satisfying person sexual pleasure"""
    # marks itself as completed if you please person for specified pleasure
    def __init__(self, person, pleasure=5, *args, **kwargs):
        super(SexualPleasureTarget, self).__init__(*args, **kwargs)
        self.target = person
        self.pleasure = 5
        self._completed = False
        SatisfySex.run.add_callback(self._satisfy_listener)

    def _satisfy_listener(self, satisfy, *args, **kwargs):
        if satisfy.target == self.target and satisfy.value >= self.pleasure:
            self._completed = True
        if self.completed(None):
            SatisfySex.run.remove_callback(self._satisfy_listener)

    def completed(self, performer):
        return self._completed


class SexualPleasureQuest(Quest):

    def __init__(self, person, pleasure=5, *args, **kwargs):
        super(SexualPleasureQuest, self).__init__(*args, **kwargs)
        self.target = person
        self.add_target(SexualPleasureTarget(person, pleasure))

    def _activate(self):
        self.target.add_interaction('quest_please', store.edge_quest_options)

    def _finish(self):
        self.target.remove_interaction('quest_please')
        return True
