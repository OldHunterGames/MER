import renpy.store as store
import renpy.exports as renpy


class SexEngine(object):


    def __init__(self, player, persons):
        # player is a tuple (player, willing)
        # init takes list of (person, willing) tuples, willing=True/False

        self.participants = [SexParticipant(i[0], i[1]) for i in persons]
        self.participants.insert(0, SexParticipant(player[0], player[1]))
        self.participants[0].target = self.participants[1]
        for i in range(1, len(self.participants)):
            self.participants[i].target = self.participants[0]



class SexParticipant(object):


    def __init__(self, person, willing):

        self.person = person
        self.willing = willing
        self.standart = 0

        self.drive = 0
        self.stamina = max(self.person.vitality, self.person.physique)
        if self.person.vitality < 1:
            self.stamina -= 1

        self.feelings = 0
        
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
        return self.person.anatomy

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


    def use_action(self, action):
        markers = []
        for i in action.markers['actor']:
            if i == 'target':
                for n in self.target.markers:
                    markers.append(n)
            else:
                markers.append(i)
        value = self.apply_markers(markers)
        self.target.send_markers(action, self)


    def send_markers(self, action, sender):
        markers = []
        for i in action.markers['target']:
            if i == 'actor':
                for n in sender.markers:
                    markers.append(n)
            else:
                markers.append(i)
        value = self.apply_markers(markers)

    def apply_markers(self, markers):
        value = 0
        for i in markers:
            if i in self.taboos:
                return -1
            elif i in self.fetishes:
                value += 1
        return value

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