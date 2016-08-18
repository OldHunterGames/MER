# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from mer_utilities import encolor_text

def make_menu(location):
    locations = edge.get_locations('grim_battlefield')
    menu_list = [(location.name + ' ' + location.owner, location) for location in locations]
    choice = renpy.display_menu(menu_list)
    return edge.go_to(choice)
ownerable = ['charity_mission']
unique = ['outpost', 'shifting_mist']
class EdgeEngine(object):
    """
    This is the main script of Edge of Mists core module for Mists of Eternal Rome.
    """

    def __init__(self):
        self.locations = []
        self.house = None
        self.loc_max = 0
    
    def explore_location(self):
        location = choice(renpy.store.edge_locations.items())
        while self.has_location(location[0]) and location[0] in unique:
            location = choice(renpy.store.edge_locations.items())
        location = EdgeLocation(location[0])
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
            return self.make_locations_menu()
        return self.go_to(choice)

    def remove_location(self, location):
        self.locations.remove(location)

    def is_maximum_scouted(self):
        if len(self.locations) < self.loc_max:
            return False
        return True

    def locations_tick(self):
        for location in self.locations:
            location.increase_cache()

    def player_has_cache(self):
        for location in self.locations:
            if location.player_cache:
                return True

cache_locations = ['echoing_hills', 'hazy_marsh', 'dying_grove']

class EdgeLocation(object):
    def __init__(self, id_, permanent=False):
        self.id = id_
        self.lbl_to_go = 'lbl_edge_' + self.id
        self.owner = None
        self.job = None
        self.permanent = permanent
        self.cache = 0 if self.id in cache_locations else None
        self.player_cache = False
        self.just_created = True
    @property
    def name(self):
        name = renpy.store.edge_locations[self.id].format(self.show_owner())
        if self.cache == None:
            return name
        else:
            return encolor_text(name, self.cache)

    def gen_owner(self):
        self.owner = choice(renpy.store.house_names.keys())

    def show_owner(self):
        try:
            value = renpy.store.house_names[self.owner]
            return value
        except KeyError:
            return

    def go_to(self):
        renpy.call(self.lbl_to_go, self)

    def increase_cache(self):
        if self.just_created:
            self.just_created = False
            return
        try:
            self.cache += 1
        except TypeError:
            return

    def explore_cache(self):
        self.cache = 0

    def make_cache(self):
        self.player_cache = True

