# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from mer_utilities import encolor_text
from factions import Faction
from mer_person import gen_random_person
from mer_resources import BarterSystem

def make_menu(location):
    locations = edge.get_locations('grim_battlefield')
    menu_list = [(location.name + ' ' + location.owner, location) for location in locations]
    choice = renpy.display_menu(menu_list)
    return edge.go_to(choice)
ownerable = ['charity_mission', 'grim_battlefield', 'crimson_pit', 'junk_yard',
    'ruined_factory', 'squatted_slums']
unique = ['outpost', 'shifting_mist']

class EdgeEngine(object):
    """
    This is the main script of Edge of Mists core module for Mists of Eternal Rome.
    """


    gang_list = []

    def __init__(self):
        self.locations = []
        self.house = None
        self.loc_max = 0
        self.slums_mode = False
        self.faction_mode = False
        self.resources = BarterSystem()

    def explore_location(self):
        location = choice(renpy.store.edge_locations.items())
        while self.has_location(location[0]) or location[0] in unique:
            location = choice(renpy.store.edge_locations.items())
        location = EdgeLocation(location[0], engine_ref=self)
        if location.id in ownerable:
            location.gen_owner()
        self.locations.append(location)
        return location
    
    def has_location(self, location_id):
        for location in self.locations:
            if location.id == location_id:
                return True
        return False
    

    def get_locations(self, location_id):
        list_ = []
        for location in self.locations:
            if location.id == location_id:
                list_.append(location)
        return list_

    def go_to(self, location):
        location.go_to()

    def make_locations_menu(self):
        menu_list = []
        for location in self.locations:
            displayed = location.name
            menu_list.append((displayed, location))
        diff = self.loc_max - len(self.locations)
        for i in range(diff):
            menu_list.append(('???', 'pass'))
        menu_list.append(('Do not go anywhere', 'done'))
        choice = renpy.display_menu(menu_list)
        if choice == 'done':
            return renpy.call('lbl_edge_manage')
        if choice == 'pass':
            return renpy.call('lbl_edge_missed_location')
        return self.go_to(choice)

    def remove_location(self, location):
        self.locations.remove(location)

    def is_maximum_scouted(self):
        if len(self.locations) < self.loc_max:
            return False
        return True

    def locations_tick(self):
        for location in self.locations:
            location.increase_stash_difficulty()

    def player_has_cache(self):
        for location in self.locations:
            if location.player_cache:
                return True

    def go_to_mist(self):
        self.locations = []
        self.house = choice(store.house_names.values())
        trade_loc = EdgeLocation('outpost', True, engine_ref=self)
        trade_loc.gen_owner(choice(store.great_houses))
        mist_loc = EdgeLocation('shifting_mist', True, engine_ref=self)
        self.locations.append(trade_loc)
        self.locations.append(mist_loc)
    
    def in_any_gang(self, person):
        return any([gang for gang in self.gang_list if person in gang.members])
        

cache_locations = ['echoing_hills', 'hazy_marsh', 'dying_grove']

class EdgeLocation(object):
    def __init__(self, id_, permanent=False, engine_ref=None):
        self.id = id_
        self.lbl_to_go = 'lbl_edge_' + self.id
        self.owner = None
        self.job = None
        self.permanent = permanent
        self.stash = 0 if self.id in cache_locations else None
        self.richness = 0
        self.has_player_stash = False
        self.just_created = True
        self._engine = engine_ref
    
    @property
    def name(self):
        name = renpy.store.edge_locations[self.id].format(self.show_owner())
        if self.stash is None:
            return name
        else:
            return encolor_text(name, self.stash)

    def gen_owner(self, owner=None):
        if owner == None:
            person = gen_random_person('human')
            name = choice(store.gang_prefix_names) + ' ' + choice(store.gang_suffix_names)
            faction = Gang(person, name, self)
            self.owner = faction
        else:
            self.owner = owner

    def show_owner(self):
        try:
            value = self.owner.name
            return value
        except AttributeError:
            return

    def go_to(self):
        renpy.call(self.lbl_to_go, self)

    def make_stash(self):
        if not self.has_player_stash:
            self.has_player_stash = True
            self._engine.resources.spend(self._engine.resources.value)
            self.stash = self._engine.resources.value

    def empty_stash(self):
        if self.has_player_stash:
            self.has_player_stash = False
            self._engine.resources.income(self.stash)
            self.stash = 0
   
    def increase_stash_difficulty(self):
        if self.richness < 5:
            self.richness += 1




class Gang(Faction):
    def __init__(self, owner, name, location):
        super(Gang, self).__init__(owner, name)
        self.warlord = None
        self.medic = None
        self.chief = None
        self.madame = None
        self.locations_controlled = [location]
        EdgeEngine.gang_list.append(self)

    def set_member_to_role(self, person, role):
        setattr(self, role, person)
        self.add_member(person)

    def conquer_location(self, location):
        self.locations_controlled.append(location)