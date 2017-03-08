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
from mer_relations_shift import ShiftRelations


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


class QuestTracker(object):

    def __init__(self):
        self.active_quests = []

    def add_quest(self, quest):
        self.active_quests.append(quest)

    def remove_quest(self, quest):
        self.active_quests.remove(quest)

    def quest_targets_achieved(self, quest):
        return quest.check()

    def finish_quest(self, quest):
        finished = quest.finish()
        if finished:
            self.remove_quest(quest)


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
        self.tokens_game = None
        self.quest_tracker = QuestTracker()

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

    def get_lifestyle(self, person):
        try:
            value = self.current_world.get_lifestyle(person)
        except AttributeError:
            value = "DEFAULT"
        return value

    def services(self):
        if self.current_world == self:
            return store.services_data
        else:
            return self.current_world.services()

    def accommodations(self):
        if self.current_world == self:
            return store.accomodations_data
        else:
            return self.current_world.accommodations()

    def overtimes(self):
        if self.current_world == self:
            return store.overtimes_data
        else:
            return self.current_world.overtimes()

    def feeds(self):
        if self.current_world == self:
            return store.feeds_data
        else:
            return self.current_world.feeds() 


    @property
    def factions(self):
        return [i for i in self._factions]

    def get_factions_by_type(self, type):
        return [i for i in self.factions if i.type == type]

    def set_world(self, world):
        self.current_world = world
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
        if self._player is not None:
            self.characters.remove(self._player)
        self.characters.append(person)
        self._player = person
        self._actor = person
        person.trade_level = 0
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
        self.tokens_game = store.TokensGame(self.player)
        self.tokens_game.start()

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
             'contribution': 'agility'}

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
        difficulty = max(0, difficulty)
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

    def shift_relations(self, person):
        ShiftRelations(self.player, person)

    def start_tokens_game(self, person):
        if self.tokens_game is None:
            self.tokens_game = store.TokensGame(person)
        self.tokens_game.start()

    def is_tokens_game_active(self):
        if self.tokens_game is not None:
            return self.tokens_game.chance is not None and not self.tokens_game.blocked
        else:
            return self.player.chances_left() > 0


    def make_sex(actor, target, type_):
        data = store.sex_types[type_]
        actor_value = get_sex_value(actor, 'actor')
        target_value = get_sex_value(target, 'target')
    def get_sex_value(data, target, target_type):
        value = 0
        for i in data[target_type]:
            value += i(target)
        if value > 0:
            target.satisfy_need('eros', value)
        #elif value < 0:
            #target.tense_need('eros', '?')
        return value