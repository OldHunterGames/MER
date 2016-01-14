# -*- coding: <UTF-8> -*-
__author__ = 'OldHuntsman'
from random import *
import renpy.store as store
import renpy.exports as renpy


class MistsOfEternalRome(object):
    """
    This is the engine of MER core module
    """

    def __init__(self, protagonist):
        self.protagonist = protagonist  # Our main hero
        self.actor = protagonist        # Our active character, hero by default but maybe someone else!
        self.decade = 1                 # The number of decades (turns) passed in ERome
        self.score = 0                  # Number of happiness points player scored through the game
        self.events_seen = []           # Unique events seen by player in this game instance
        self.event_list = []            # List of all possible events in this game instance
        self.menues = []                # For custom RenPy menu screen
        self.current_world = "MER"

    def end_turn_event(self):
        return choice(self.possible_events("turn_end")).trigger()

    def end_turn(self):
        self.decade += 1
        self.add_score_points()
        self.protagonist.rest()
        if self.protagonist.sparks < 0:
            return "game_over"
        else:
            return "new_turn"

    def discover_world(self, worlds):
        return choice(worlds)().point_of_arrival

    def add_score_points(self):
        if self.protagonist.mood() == "depressed":
            self.score += 1
        elif self.protagonist.mood() == "normal":
            self.score += 3
        elif self.protagonist.mood() == "content":
            self.score += 5
        elif self.protagonist.mood() == "happy":
            self.score += 10

    def possible_events(self, kind, who = None):
        """
        :param kind:
        "turn" - end-of-turn event
        "char" - event with one of player faction main characters
        "faction" - event for one of active factions beside player faction

        :return: the RenPu location with the choosen event
        """
        list_of_events = []
        for event in self.event_list:
            if event.check():
                if kind in event.natures:
                        list_of_events.append(event)

        return list_of_events

    def get_score(self):
        total = self.score / self.decade
        if total > 9:
            result = "CHEATER!"
        elif total > 7:
            result = "S+"
        elif total > 5:
            result = "A"
        elif total > 4:
            result = "B"
        elif total > 3:
            result = "C"
        elif total > 1:
            result = "D-"
        else:
            result = "miserable"

        return result




