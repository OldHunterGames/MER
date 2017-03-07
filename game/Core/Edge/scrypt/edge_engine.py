# -*- coding: <UTF-8> -*-
from random import *

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import encolor_text, roll
from factions import Faction
from mer_person import gen_random_person
from mer_resources import BarterSystem
from mer_itemsstorage import ItemsStorage
from mer_item import create_item
from schedule import ScheduleObject, ScheduleJob
from mer_command import Command, MenuCard

def make_menu(location):
    locations = edge.get_locations('grim_battlefield')
    menu_list = [(location.name + ' ' + location.owner, location) for location in locations]
    choice = renpy.display_menu(menu_list)
    return edge.go_to(choice)
ownerable = ['charity_mission', 'grim_battlefield', 'crimson_pit', 'junk_yard',
    'ruined_factory', 'squatted_slums']
unique = ['outpost', 'shifting_mist']

class MakeOpportunitiesCards(Command):

    def _run(self):

        return [MenuCard(i['name'], i['description'], i['label'], i['image'])
            for i in store.edge_option_cards.values()]

class EdgeEngine(object):
    """
    This is the main script of Edge of Mists core module for Mists of Eternal Rome.
    """

    def __init__(self):
        self.name = 'edge'
        self.locations = []
        self.house = None
        self.loc_max = 0
        self.slums_mode = False
        self.faction_mode = False
        self.resources = BarterSystem()
        self.gang_list = []
        self.explorations = None
        self.factions = self.gang_list
        self.stashes = {'echoing_hills': [False, ItemsStorage(), 0], 'hazy_marshes': [False, ItemsStorage(), 0],
            'dying_grove': [False, ItemsStorage(), 0]}
        self.options = []

    def get_lifestyle(self, person):
        keys = sorted([int(i) for i in store.edge_lifestyle_values.keys()])
        for i in keys:
            if store.edge_lifestyle_values[str(i)]['treshold'] <= person.decade_bill():
                value = encolor_text(store.edge_lifestyle_values[str(i)]['name'], i)
            else:
                break
        return value

    def explore_stash(self, name):
        self.stashes[name][0] = True
        self.options.append('treasure_hunt_%s'%name)

    def unexplore_stash(self, name):
        self.stashes[name][0] = False
        self.stashes[name][1] = ItemsStorage()
        self.stashes[name][2] = 0
        self.explorations.append(name)
        try:
            self.options.remove('treasure_hunt_%s'%name)
        except ValueError:
            pass

    def jobs(self):
        return store.edge_jobs_data

    def services(self):
        return store.edge_services_data

    def accommodations(self):
        return store.edge_accomodations_data

    def overtimes(self):
        return store.edge_overtimes_data

    def feeds(self):
        return store.edge_feeds_data


    def unexplore_all_stahses(self):
        for key in self.stashes.keys():
            self.unexplore_stash(key)

    def stash_quality(self, name):
        return self.stashes[name][2]

    def increase_stash_quality(self, name):
        self.stashes[name][2] += 1

    def is_stash_found(self, name):
        return self.stashes[name][0]

    def get_stash(self, name):
        return self.stashes[name][1]

    def active_stashes(self):
        return [key for key, value in self.stashes.items() if value[0]]

    def any_stash_found(self):
        return any([i[0] for i in self.stashes.values()])

    def robber_stash(self, name):
        storage = self.stashes[name][1]
        for i in storage.items():
            storage.remove_item(i, 'all')
        storage.remove_money(storage.money)

    def gen_treasures(self):
        chances = [(('gem', 'treasure'), 20), 
            (('notes', 'treasure'), 50), 
            (('knife', 'weapon'), 25),
            (('sword', 'weapon'), 20),
            (('shield', 'weapon'), 15),
            (('strudy_axe', 'weapon'), 20)]
        generated = []
        can_break = False
        while True:
            for i in chances:
                generate = roll(i[1], 100)
                if generate:
                    item = i[0]
                    generated.append(create_item(item[0], item[1]))
                    can_break = True
            if can_break:
                break
        return generated

    def _init_player_schedule(self, unlock_func, data_dict, setter_func, default_name, default_obj_id, cls):
        for i in data_dict:
            obj = ScheduleObject(i, data_dict[i])
            if not obj.hidden:
                unlock_func(i, obj)
            if i == default_obj_id:
                setter_func(default_name, obj)

    def init_player_schedule(self, player):
        self._init_player_schedule(player.schedule.unlock_accommodation, store.edge_accomodations_data,
                player.schedule.set_default, 'accommodation' , 'makeshift', ScheduleObject)
        self._init_player_schedule(player.schedule.unlock_ration, store.edge_feeds_data,
                player.schedule.set_default, 'ration', 'forage', ScheduleObject)
        self._init_player_schedule(player.schedule.unlock_job, store.edge_jobs_data, 
            player.schedule.set_default, 'job', 'idle', ScheduleJob)
        self._init_player_schedule(player.schedule.unlock_optional, store.edge_overtimes_data,
            None, None, None, ScheduleObject)


    def explore_all(self):
        for i in store.edge_locations.items():
            if i[0] not in unique:
                location = EdgeLocation(i[0], engine_ref=self)
                self.locations.append(location)
            if location.id in ownerable:
                location.gen_owner()
    
    def explore_location(self):
        """
        location = choice(renpy.store.edge_locations.items())
        while self.has_location(location[0]) or location[0] in unique:
            location = choice(renpy.store.edge_locations.items())
        location = EdgeLocation(location[0], engine_ref=self)
        if location.id in ownerable:
            location.gen_owner()
        self.locations.append(location)
        return location
        """
        pass
        
    def get_encounter(self, encounter=None):

        if encounter is None:
            encounter = random.choice(store.edge_encounters.values())
        else:
            encounter = store.edge_encounters[encounter]

        return encounter
    
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
        self.explore_all()
    
    def in_any_gang(self, person):
        return any([gang for gang in self.gang_list if person in gang.members])

    def new_turn(self):
        self.locations_tick()
        self.resources.tick_time()
        self.core.new_turn()
        for i in self.active_stashes():
            self.increase_stash_quality(i)

    
    def add_faction(self, owner, name, location, id=None):
        gang = Gang(owner, name, location, id=id)
        self.gang_list.append(gang)
        self.core.add_ready_faction(gang)
        return gang

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
        if owner is None:
            person = gen_random_person('human')
            name = choice(store.gang_prefix_names) + ' ' + choice(store.gang_suffix_names)
            faction = Gang(person, name, self)
            self.owner = faction
        else:
            self.conquer(owner)

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
            self.stash = self._engine.resources.value
            self._engine.resources.spend(self._engine.resources.value)

    def empty_stash(self):
        if self.has_player_stash:
            self.has_player_stash = False
            self._engine.resources.income(self.stash)
            self._engine.resources.decrease_tendency()
            self.stash = 0
   
    def increase_stash_difficulty(self):
        if self.richness < 5:
            self.richness += 1

    def conquer(self, gang):
        if self.owner is not None:
            try:
                self.owner.locations_controlled.remove(self)
            except AttributeError:
                pass
        try:
            gang.locations_controlled.append(self)
        except AttributeError:
            gang.locations_controlled = [self]
        self.owner = gang


class Gang(Faction):
    """roles{'warlord': None,
            'medic': None,
            'chief': None,
            'madame': None,}
    """
    def __init__(self, owner, name, location, id=None):
        super(Gang, self).__init__(owner, name, id=id)
        self.locations_controlled = [location]

    def set_member_to_role(self, person, role):
        self.roles[role] = person
        self.add_member(person)

    def get_common_members(self):
        return [member for member in self.members if member != self.owner and member not in self.roles.values()]
