import renpy.store as store
import renpy.exports as renpy


class SexEngine(object):


    def __init__(self, persons):
        # init takes list of (person, willing) tuples, willing=True/False

        self.participants = [SexParticipant(i[0], i[1]) for i in persons]


class SexParticipant(object):


    def __init__(self, person, willing):

        self.person = person
        self.willing = willing
        self.standart = 0

        self.drive = 0
        self.stamina = 0
        self.feelings = 0
        
        self.max_actions = self.sex_level
        self.actions = []

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
    success = (all([getattr(sex_participant, key) >= value for key, value in sex_participant_req_stats.items()]) and
            all([i in sex_participant.anatomy() for i in sex_participant_req_anatomy]))
    if willing:
        willing = sex_participant.willing
    else:
        willing = True
    return success and willing

def get_sex_actions():
    return [SexAction(key) for key in store.sex_actions_data.keys()]