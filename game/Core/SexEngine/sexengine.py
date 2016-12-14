import renpy.store as store
import renpy.exports as renpy

from random import shuffle

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
        self.get_actions()

    def get_actions(self):
        for i in self.participants:
            i.get_actions()



class SexParticipant(object):


    def __init__(self, person, willing):

        self.person = person
        self.willing = willing
        try:
            self.standart = person.standart
        except AttributeError:
            self.standart = 0


        self.drive = 0
        self.stamina = max(self.person.vitality, self.person.physique)
        if self.person.vitality < 1:
            self.stamina -= 1

        self.feelings = 1
        
        self.max_actions = self.sex_level
        self.actions = []
        self.target = None
    
    @property
    def avatar(self):
        return self.person.avatar_path
    
    @property
    def sex_level(self):
        return self.person.skill('sex').level

    def anatomy(self):
        return [i.attribute[8:] for i in self.person.anatomy()]

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

    def fetishes(self):
        return [i.attribute[8:] for i in self.person.fetishes()]

    def taboos(self):
        return [i.attribute[7:] for i in self.person.taboos()]


    def use_action(self, action):
        if action.type == 'twoway':
            self.send_markes(action, self.target, 'target')
            self.target.send_markes(action, self, 'actor')
        elif action.type == 'outward':
            self.target.send_markes(action, self, 'actor')
        elif action.type == 'inward':
            self.send_markes(action, target, 'target')
        else:
            raise Exception("Unknown sex action type %s"%(action.type))


    def send_markers(self, action, sender, type_):
        markers = [send.gender, sender.genus.name]
        for i in action.markers[type_]:
            markers.append(i)
        value = self.apply_markers(markers)

    def apply_markers(self, markers):
        value = 0
        taboos = self.taboos().keys()
        fetishes = self.fetishes().keys()
        for i in markers:
            if i in taboos:
                return -1
            elif i in fetishes:
                value += 1
        return value

    def set_drive(self, situation):
        pass

    def get_actions(self):
        actions = get_sex_actions()
        actions = [i for i in actions if i.can_be_used(self, self.target)]
        shuffle(actions)
        if len(actions) > self.max_actions:
            actions = actions[0:self.max_actions-1]
        self.actions = actions

class SexAction(object):


    def __init__(self, id_):
        self.id = id_
        self.data = store.sex_actions_data[id_]
    
    def __getattr__(self, attr):
        try:
            attr = self.data[attr]
        except KeyError:
            raise Exception('Have no key %s for SexAxtion %s'%(attr, self.id))
        else:
            return attr

    def can_be_used(self, actor, target):
        actor_success = _required_stats(actor, self, 'actor')
        target_success = _required_stats(target, self, 'target')
        return actor_success and target_success

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
        willing = False
    success = True
    for key, value in sex_participant_req_stats.items():
        if value[0] == '>=':
            success = value[1] >= getattr(sex_participant, key)
        elif value[0] == '<=':
            success = value[1] <= getattr(sex_participant, key)

    success = success and all([i in sex_participant.anatomy() for i in sex_participant_req_anatomy])
    if willing:
        willing = sex_participant.willing
    else:
        willing = True
    return success and willing

def get_sex_actions():
    return [SexAction(key) for key in store.sex_actions_data.keys()]