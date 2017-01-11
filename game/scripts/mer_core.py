# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import collections
import copy

import renpy.store as store
import renpy.exports as renpy

from mer_person import *
from mer_event import events_dict, Event
from mer_resources import Resources, BarterSystem
from factions import Faction
from mer_item import *
from mer_utilities import encolor_text


remembered_needs = collections.defaultdict(list)


def set_event_game_ref(game):
    Event.set_game_ref(game)

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
        self.events_dict = events_dict  # List of all possible events in this game instance
        self.menues = []                # For custom RenPy menu screen
        self.evn_skipcheck = True
        self.resources = BarterSystem()
        self._factions = []
        self.current_world = self
        self.characters = persons_list
        self.time = 0

        self.allow_shemales = True
        self.allow_sexless = True
        self.hero_gender_options = ['male', 'female', 'shemale', 'sexless']
        self.orientation = {
           'male': ['female', 'incest', 'furry', 'corpses'],
           'female': ['female', 'male', 'shemale', 'incest', 'elders', 'furry', 'animals', 'monsters'],
           'shemale': ['female', 'male', 'shemale', 'sexless', 'incest', 'elders', 'furry', 'animals', 'monsters', 'corpses'],
           'sexless': ['male', 'shemale', 'incest', 'elders', 'furry', 'animals', 'monsters'],
        }
        ## all partner options: ['female', 'male', 'shemale', 'sexless', 'related', 'underage', 'elders', 'furry', 'animals', 'monsters', 'corpses']


    def jobs(self):
        if self.current_world == self:
            return store.jobs_data
        else:
            return self.current_world.jobs()

    def services(self):
        if self.current_world == self:
            return store.services_data
        else:
            return self.current_world.services()

    def accomodations(self):
        if self.current_world == self:
            return store.accomodations_data
        else:
            return self.current_world.accomodations()

    def overtimes(self):
        if self.current_world == self:
            return store.overtimes_data
        else:
            return self.current_world.overtimes() 


    @property
    def factions(self):
        return [i for i in self._factions]

    def get_factions_by_type(self, type):
        return [i for i in self.factions if i.type == type]

    def set_world(self, world):
        self.current_world = world
        Schedule.set_world(world.name)
        world.core = self

    def get_faction(self, id_):
        for i in self.factions:
            if i.id == id_:
                return i
        raise Exception("No faction with id: %s" % (id_))

    def add_faction(self, owner, name, type='unbound', id=None):
        faction = Faction(owner, name, type, id)
        self._factions.append(faction)
        return faction

    def add_ready_faction(self, faction):
        if not faction in self._factions:
            self._factions.append(faction)

    def remove_faction(self, faction):
        self._factions.remove(faction)

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
        renpy.restart_interaction()

    def end_turn_event(self, skipcheck=False):
        events = self.events_dict.values()
        shuffle(events)
        char = choice([char for char in self.characters if char.calculatable])
        for ev in events:
            r = ev.trigger(char, skipcheck)
            if r:
                return

    def suggestion(self, target, power):
        if power > target.suggestion_check():
            return True
        return False

    def token_difficulty(self, target, token):
        d = {'conquest': 'spirit', 'convention': 'mind',
             'contribution': 'sensitivity'}

        check = getattr(target, d[token])
        check += target.relations(self.player).stability
        if target.token != 'power':
            check += 1
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


    def skillcheck(self, person, attribute, difficulty):
        skill = person.skill(attribute)
        difficulty -= skill
        return renpy.call_in_new_context('lbl_skillcheck_mini', person=person, attribute=attribute, difficulty=difficulty)


    def discover_world(self, worlds):
        return choice(worlds)().point_of_arrival


    def gain_ctoken(self, target, actor, token, skill_name):
        skill = actor.skill(skill_name)
        difficulty = self.token_difficulty(target, token)
        result = self.skillcheck(actor, skill_name, difficulty)
        if result:
            target.set_token(token)
        else:
            target.set_token('antagonism')
        return result

    def use_token(self):
        pass

#Alternate Skillcheck

class Skillcheck(object):


    def __init__(self, person, skill, morality=None, difficulty=0, tense=None, satisfy=None, beneficiar=None, delayed=False):
        self.skill = person.skill(skill)
        self.person = person
        self.skill_level = self.skill.level
        self.difficulty = difficulty
        self.morality = morality if morality is not None else []
        self.resources = {}
        self.cons = []
        self.beneficiar = beneficiar
        self.sabotaged = False
        self.satisfy = satisfy if satisfy is not None else []
        self.tense = tense if tense is not None else []
        if not delayed:
            self.activate()

    def init_cons(self):
        self.cons = []
        for i in range(1, self.difficulty+1):
            self.cons.append(('difficulty', 5-self.skill_level))
        if self.person.anxiety > 0:
            self.cons.append(('anxiety', min(self.person.anxiety, 5)))
        if self.motivation < 0:
            self.cons.append(('motivation', 6 - self.person.spirit))

    def sabotage(self):
        self.sabotaged = True

    def init_resources(self):
        self.resources = {}
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
        if person.has_inner_resource('motivation'):
            if self.motivation > 0:
                self.resources['motivation'] = self.motivation

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
                    break
        else:
            if value > self.skill_level:
                self.skill_level += 1

        del self.resources[resource]
        self.person.use_inner_resource(resource)

    @property
    def result(self):
        if self.sabotaged:
            return -1
        if len(self.cons) > 0:
            return 0
        else:
            return self.skill_level

    def activate(self):
        self.morality = self.person.check_moral(*self.morality)
        self.motivation = self.person.motivation(
            self.skill, self.tense, self.satisfy, self.beneficiar, self.morality)
        self.init_resources()
        self.init_cons()
        if self.person.player_controlled:
            renpy.call_in_new_context('lbl_skillcheck', self)
        else:
            self.npc_check()

    def end(self):
        if self.result >= 0:
            for i in self.satisfy:
                getattr(self.person, i).set_satisfaction(self.result)
            for i in self.tense:
                getattr(self.person, i).set_tension()
            self.person.moral_action(self.morality)

    def has_cons(self):
        return len(self.cons) > 0

    def cons_values(self):
        return [i[1] for i in self.cons]

    def npc_check(self):
        if self.motivation < 0:
            self.sabotaged = True
            return
        elif self.motivation == 0:
            self.end()
            return
        
        for v in self.resources.values():
            cons = [i for i in self.cons]
            if not self.has_cons():
                return
            used = False
            if v >= min([i[1] for i in cons]):
                if not used:
                    for key, value in self.resources.items():
                        if value == v:
                            self.use_resource(key)
                            used = True
        self.end()




