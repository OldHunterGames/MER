# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import collections
import copy

import renpy.store as store
import renpy.exports as renpy

from mer_person import *
from mer_event import events_list, Event
from mer_resources import Resources, BarterSystem
from factions import Faction
from mer_item import *
from mer_utilities import encolor_text


remembered_needs = collections.defaultdict(list)


def set_event_game_ref(game):
    Event.set_game_ref(game)


class UsedNeeds(object):


    def __init__(self, needs, owner):
        self.needs = copy(needs)
        self.owner = owner

    def is_used(self, needs, target):
        if target != self.owner:
            return True
        for need in needs:
            if need not in self.needs:
                return False
        return True


def remember_needs(target, token, needs):
    if not is_needs_used(target, token, needs):
        remembered_needs[token].append(UsedNeeds(needs, target))


def is_needs_used(target, token, needs):
    for used in remembered_needs[token]:
        if used.is_used(needs, target):
            return True
    return False


def get_max_need(target, *args):
    maxn_name = None
    maxn = 0
    needs = target.get_needs()
    for arg in args:
        if arg in needs.keys():
            level = needs[arg].level
            if level > maxn:
                maxn = level
                maxn_name = arg
    return maxn, maxn_name


class MistsOfEternalRome(object):
    """
    This is the engine of MER core module
    """

    def __init__(self):
        self._player = None  # Our main hero
        self._actor = None       # Our active character, hero by default but maybe someone else!
        self.sayer = None
        # The number of decades (turns) passed in ERome
        self.decade = 1
        # Number of happiness points player scored through the game
        self.score = 0
        self.events_seen = []           # Unique events seen by player in this game instance
        self.events_list = events_list  # List of all possible events in this game instance
        self.menues = []                # For custom RenPy menu screen
        self.evn_skipcheck = True
        self.resources = BarterSystem()
        self._factions = []
        self.current_world = "MER"
        self.characters = persons_list
        self.time = 0

    @property
    def factions(self):
        return [faction for faction in self._factions]

    def set_world(self, world):
        self.current_world = world
        Schedule.set_world(world.name)
        world.core = self

    def get_faction(self, id_):
        for i in self.factions:
            if i.id == id_:
                return i
        raise Exception("No faction with id: %s" % (id_))

    def add_faction(self, owner, name, id_=None):
        faction = Faction(owner, name, id_)
        self._factions.append(faction)
        return faction

    def is_member_of_faction(self, person, faction):
        return faction.has_member(person)

    def has_any_faction(self, person):
        return any([faction.has_member(person) for faction in self.factions])

    @property
    def protagonist(self):
        return self._player

    @property
    def player(self):
        if not self._player:
            raise Exception("Player person is not selected")
        return self._player

    @property
    def actor(self):
        return self._actor

    def set_player(self, person):
        self._player = person
        self._actor = person
        person.player_controlled = True

    def set_actor(self, person):
        self._actor = person

    def choose_study(self):
        if self.studies:
            study = choice(self.studies)
        else:
            study = False

        return study

    def can_skip_turn(self):
        return all([i.can_tick() for i in self.characters])

    def new_turn(self, label_to_jump=None):
        for person in self.characters:
            person.tick_time()
        self.end_turn_event()
        for person in self.characters:
            person.tick_schedule()
            person.rest()
        self.time += 1
        self.player.ap = 1

    def end_turn_event(self, skipcheck=False):
        shuffle(self.events_list)
        possible = self.events_list
        char = choice([char for char in self.characters if char.calculatable])
        for ev in possible:
            r = ev.trigger(char, skipcheck)
            if r:
                return

    def suggestion(self, target, power):
        if power > target.suggestion_check():
            return True
        return False

    def token_difficulty(self, target, token, *args):
        d = {'conquest': 'spirit', 'convention': 'mind',
             'contribution': 'sensitivity'}

        check = getattr(target, d[token])
        if target.vitality < 1:
            check -= 1
        if target.mood < 0:
            check -= 1
        check += (3 - get_max_need(target, *args)[0])
        check -= target.stance(self.player).value
        harmony = target.relations(self.player).harmony()[0]
        if harmony > 0:
            check -= harmony
        if check < 0:
            check = 0
        return check

    def threshold_skillcheck(self, actor, skill, difficulty=0, tense_needs=[], satisfy_needs=[], beneficiar=None,
                             morality=0, success_threshold=0, special_motivators=[]):
        # success_threshold += 1
        result = self.skillcheck(actor, skill, difficulty, tense_needs, satisfy_needs,
                                 beneficiar, morality, special_motivators, success_threshold)
        if success_threshold <= result:
            threshold_result = True
        else:
            threshold_result = False
        return threshold_result, result

    def skillcheck(self, actor, skill, difficulty=0, tense_needs=[], satisfy_needs=[], beneficiar=None,
                   morality=0, special_motivators=[], threshold=None):
        skill = actor.skill(skill)
        motivation = actor.motivation(
            skill.name, tense_needs, satisfy_needs, beneficiar)
        # factors['attraction'] and equipment bonuses not implemented yet
        factors = {'level': skill.level,
                   skill.attribute: skill.attribute_value(),
                   'focus': skill.focus,
                   'mood': actor.mood,
                   'motivation': motivation,
                   'vitality': actor.vitality,
                   'bonus': actor.count_modifiers(skill.name)}
        result = skill.level
        used = []
        found = False
        while result != 0:
            difficulty_check = 1
            used = []
            for k, v in factors.items():
                if difficulty < difficulty_check:
                    found = True
                elif k != 'level' and v >= result:
                    difficulty_check += 1
                    used.append(k)
            if difficulty < difficulty_check:
                found = True
            if not found:
                result -= 1
            else:
                break
        if motivation < 1:
            result = -1
        renpy.call_in_new_context(
            'lbl_skillcheck_info', result, factors, skill, used, threshold, difficulty)
        if result >= 0:
            for need in tense_needs:
                getattr(actor, need).set_tension()
            for need in satisfy_needs:
                getattr(actor, need).satisfaction = result
            actor.use_skill(skill)
            if actor == self.player and beneficiar == actor.master:
                if result > actor.merit:
                    actor.merit = result
            actor.moral_action(morality)
        return result

    def discover_world(self, worlds):
        return choice(worlds)().point_of_arrival


#Alternate Skillcheck

class Skillcheck(object):


    def __init__(self, person, skill, difficulty=0):
        self.skill = person.skill(skill)
        self.person = person
        self.skill_level = self.skill.level
        self.difficulty = difficulty
        self.resources = {}
        self.cons = []
        self.init_resources()
        self.init_cons()

    def init_cons(self):
        for i in range(1, self.difficulty+1):
            self.cons.append(('difficulty', i))
        if self.person.anxiety > 0:
            self.cons.append(('anxiety', min(self.person.anxiety, 5)))

    def init_resources(self):
        skill = self.skill
        person = self.person
        attribute = skill.attribute
        attribute_value = skill.attribute_value()
        is_focused = skill.is_focused()
        has_determination = person.determination > 0
        if person.has_inner_resource(attribute):
            self.resources[attribute] = attribute_value

        if person.has_inner_resource('focus') and is_focused:
            self.resources['focus'] = person.focus

        if person.has_inner_resource('determination') and has_determination:
            self.resources['determination'] = 5

        if person.has_inner_resource('vitality') and person.vitality > 0:
            self.resources['vitality'] = person.vitality
        if person.has_inner_resource('mood') and person.mood > 0:
            self.resources['mood'] = person.mood

    def use_resource(self, resource):
        value = self.resources[resource]
        cons_values = [i[1] for i in self.cons]
        cons_values = sorted(cons_values)
        remove = 0
        for i in reversed(cons_values):
            if i <= value:
                remove = i
                break
        if remove > 0:
            for i in self.cons:
                if i[1] == remove:
                    self.cons.remove(i)
        else:
            if value > self.skill_level:
                self.skill_level += 1

        del self.resources[resource]
        self.person.use_inner_resource(resource)

    @property
    def result(self):
        if len(self.cons) > 0:
            return 0
        else:
            return self.skill_level

    def has_cons(self):
        return len(self.cons) > 0

