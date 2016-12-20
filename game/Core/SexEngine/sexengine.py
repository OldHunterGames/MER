from random import shuffle

import renpy.store as store
import renpy.exports as renpy

from mer_utilities import encolor_text


class SexEngine(object):


    def __init__(self, player, persons):
        # player is a tuple (player, willing)
        # init takes list of (person, willing) tuples, willing=True/False

        self.participants = [SexParticipant(i[0], i[1]) for i in persons]
        self.participants.insert(0, SexParticipant(player[0], player[1]))
        self.participants[0].target = self.participants[1]
        self.participants[1].target = self.participants[0]
        for i in range(2, len(self.participants)):
            self.participants[i].target = self.participants[1]
        self.new_target = None
        self.get_actions()

    def player(self):
        return self.participants[0]

    def get_actions(self):
        if self.new_target is not None:
            self.change_target(self.new_target)
            self.new_target = None
        for i in self.participants:
            if i.active:
                i.get_actions()
            else:
                i.actions = []

    def active_participants(self):
        return [i for i in self.participants if i.active]

    def ended(self):
        return len(self.active_participants()) < 2 or not self.participants[0].active

    def change_target(self, target):
        participants = self.active_participants()
        for i in participants:
            i.target = target
        if target == self.player():
            target.target = participants[1]
        else:
            target.target = self.player()

    def set_target(self, target):
        self.new_target = target

    def inactive_targeted(self):
        participants = self.active_participants()
        for i in participants:
            if i.target not in participants:
                return True
        return False

    def clear_actions(self):
        for i in self.participants:
            i.actions = []
            for n in i.discovered_fetishes:
                renpy.call_in_new_context('lbl_discover_dirty', i, n)
            for n in i.discovered_taboos:
                renpy.call_in_new_context('lbl_discover_dirty', i, n)
            i.discovered_fetishes = []
            i.discovered_taboos = []

        self.get_actions()

    def apply_feelings(self):
        for i in self.participants:
            if i.feelings < 0:
                pass
            elif i.feelings > 0:
                pass
            if i.feelings > i.standart:
                i.person.sex_standart = i.feelings



class SexParticipant(object):


    def __init__(self, person, willing):

        self.person = person
        self.willing = willing
        try:
            self.standart = person.sex_standart
        except AttributeError:
            self.standart = 0

        self.active = True
        self.drive = 3
        self._stamina = 0
        self.stamina = max(self.person.vitality, self.person.physique)
        if self.person.vitality < 1:
            self.stamina -= 1

        self.feelings = 1
        
        self.max_actions = self.sex_level
        self.actions = []
        self.target = None
        self.discovered_fetishes = []
        self.discovered_taboos = []


    def show_feelings(self):
        if self.feelings < 0:
            return encolor_text('below zero', 'red')
        if self.feelings > 0:
            if self.feelings < self.standart:
                return encolor_text('above zero', 'green')
            else:
                return encolor_text('Standart', 5)
        else:
            return 'zero'


    @property
    def stamina(self):
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        self._stamina = value
        if self._stamina < 1:
            self._stamina = 0
            self.active = False

    @property
    def drive(self):
        return self._drive

    @drive.setter
    def drive(self, value):
        self._drive = value
        if self._drive < 1:
            self._drive = 0
            self.active = False
    
    @property
    def age(self):
        return self.person.age

    @property
    def kink(self):
        return self.person.kink
    
    @property
    def avatar(self):
        return self.person.avatar_path
    
    @property
    def sex_level(self):
        return self.person.skill('sex').level

    def anatomy(self):
        return [i for i in self.person.anatomy()]

    def has_anatomy_feat(self, name):
        return self.person.has_anatomy_feat(name)

    @property
    def physique(self):
        return self.person.physique
    
    @property
    def agility(self):
        return self.person.agility
    
    @property
    def mind(self):
        return self.person.mind
    
    @property
    def spirit(self):
        return self.person.spirit
    
    @property
    def sensitivity(self):
        return self.person.sensitivity

    @property
    def gender(self):
        return self.person.gender

    @property
    def genus(self):
        return self.person.genus

    def fetishes(self):
        return [i for i in self.person.fetishes()]

    def taboos(self):
        return [i for i in self.person.taboos()]

    def revealed_fetishes(self):
        return self.person.revealed('fetishes')

    def revealed_taboos(self):
        return self.person.revealed('taboos')

    @property
    def name(self):
        return self.person.name


    def use_action(self, action):
        self.send_markers(action, self.target, 'target')
        self.target.send_markers(action, self, 'actor')
        for key, value in action.pay.items():
            old_value = getattr(self, key)
            setattr(self, key, old_value - value)


    def send_markers(self, action, sender, type_):
        markers = [sender.gender, sender.genus.type]
        for i in action.markers[type_]:
            markers.append(i)
        for i in action.markers['both']:
            markers.append(i)
        value = self.apply_markers(markers)
        self.feelings += value * getattr(sender, action.attribute)

    def apply_markers(self, markers):
        value = 0
        taboos = self.taboos()
        fetishes = self.fetishes()
        for i in markers:
            if i in taboos:
                value = -1
                if i not in self.person.revealed('taboos'):
                    self.person.reveal('taboos', i)
                    self.discovered_taboos.append('Taboo discovered: %s'%i)
            elif i in fetishes:
                if value >= 0:
                    value += 1
                if i not in self.person.revealed('fetishes'):
                    self.person.reveal('fetishes', i)
                    self.discovered_fetishes.append('Fetish discovered: %s'%i)
        return value

    def set_drive(self, situation):
        pass

    def get_actions(self):
        actions = get_sex_actions()
        actions = [i for i in actions if i.can_be_used(self, self.target)]
        shuffle(actions)
        while len(actions) > self.max_actions:
            actions.pop()
        self.actions = actions

class SexAction(object):


    def __init__(self, id_):
        self.id = id_
        self.data = store.sex_actions_data[id_]
    
    def __getattr__(self, attr):
        try:
            attr = self.data[attr]
        except KeyError:
            raise Exception('Have no key %s for SexAction %s'%(attr, self.id))
        else:
            return attr

    def can_be_used(self, actor, target):
        actor_success = _required_stats(actor, self, 'actor')
        target_success = _required_stats(target, self, 'target')
        return actor_success and target_success

    def colored_markers(self, person, type_):
        list_ = [i for i in self.markers[type_]]
        list_.extend(self.markers['both'])
        new_list = []
        for i in list_:
            if i in person.revealed_taboos():
                new_list.append(encolor_text(i, 'red'))
            elif i in person.revealed_fetishes():
                new_list.append(encolor_text(i, 'green'))
            else:
                new_list.append(i)
        return new_list


def _required_stats(sex_participant, sex_action, type_):
    #type = 'actor' or 'target'
    sex_participant_required = sex_action.required[type_]
    try:
        sex_participant_req_stats = sex_participant_required['stats']
    except KeyError:
        sex_participant_req_stats = {}
    try:
        sex_participant_req_anatomy = sex_participant_required['anatomy']
    except KeyError:
        sex_participant_req_anatomy = []
    try:
        willing = sex_participant_required['willing']
    except KeyError:
        willing = None
    willing_part = sex_participant.willing
    success = True
    stats = []
    for key, value in sex_participant_req_stats.items():
        stats.append({'>=': lambda: getattr(sex_participant, key) >= value[1],
            '>': lambda: getattr(sex_participant, key) > value[1],
            '<=': lambda: getattr(sex_participant, key) <= value[1],
            '<': lambda: getattr(sex_participant, key) < value[1],
            '==': lambda: value[1] == getattr(sex_participant, key)}[value[0]]())
    success = all(stats)
    success = success and all([sex_participant.has_anatomy_feat(i) for i in sex_participant_req_anatomy])
    
    if willing is None:
        return success
    else:
        return success and (willing == willing_part)

def get_sex_actions():
    return [SexAction(key) for key in store.sex_actions_data.keys()]