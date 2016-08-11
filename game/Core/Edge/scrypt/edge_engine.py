# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

def make_menu(location):
    locations = edge.get_locations('grim_battlefield')
    menu_list = [(location.name + ' ' + location.owner, location) for location in locations]
    choice = renpy.display_menu(menu_list)
    return edge.go_to(choice)
ownerable = ['charity_mission']
class EdgeEngine(object):
    """
    This is the main script of Edge of Mists core module for Mists of Eternal Rome.
    """

    def __init__(self):
        self.locations = []

    def explore_location(self):
        location = choice(renpy.store.edge_locations.items())
        location = EdgeLocation(location[0], location[1])
        if location.id in ownerable:
            location.gen_owner()
        self.locations.append(location)
    
    def has_location(self, location_id):
        for location in self.locations:
            if location.id == location_id:
                return True
        return False
    
    def explore(self):
        renpy.notify('test123')

    def get_locations(self, location_id):
        list_ = []
        for location in self.locations:
            if location.id == location_id:
                list_.append(location)
        return list_

    def go_to(self, location):
        location.go_to()

    def make_menu(self, location):
        locations = self.get_locations(location)
        menu_list = []
        for location in locations:
            displayed = location.name
            if location.owner != None:
                displayed += ' ' + location.owner
            menu_list.append((displayed, location))
        choice = renpy.display_menu(menu_list)
        return self.go_to(choice)

class EdgeLocation(object):
    def __init__(self, id_, displayed):
        self.id = id_
        self.name = displayed
        self.lbl_to_go = 'lbl_edge_' + self.id
        self.owner = None
        self.job = None

    def gen_owner(self):
        self.owner = choice(renpy.store.house_names.keys())

    def show_owner(self):
        return renpy.store.house_names[self.owner]

    def go_to(self):
        renpy.call(self.lbl_to_go, self)

    def job_available(self):
        pass

