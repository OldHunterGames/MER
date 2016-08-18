# -*- coding: UTF-8 -*-
from random import *
import collections

import renpy.store as store
import renpy.exports as renpy

from features import Feature, Phobia
from skills import Skill, skills_data
from needs import init_needs
from copy import copy
from copy import deepcopy
from schedule import *
from relations import Relations
from stance import Stance
from genus import init_genus, available_genuses
from alignment import Alignment
from modifiers import ModifiersStorage
from factions import Faction
from buffs import Buff

class Inventory(object):
    def __init__(self):
        self.carried_weapons = collections.OrderedDict([('harness', None), ('belt1', None),
            ('belt2', None), ('armband', None), ('ankleband', None)])
        self.carried_armor = collections.OrderedDict([('underwear', None), ('garments', None), ('overgarments', None)])
        self._main_hand = None
        self._other_hand = None
        self.storage = []
    def weapon_slots(self):
        return self.carried_weapons.keys()
    def armor_slots(self):
        return self.carried_armor.keys()
    @property
    def main_hand(self):
        return self._main_hand
    
    @main_hand.setter
    def main_hand(self, weapon):
        if self._main_hand != None:
            self._main_hand.unequip()
            if self._main_hand not in self.storage:
                self.storage.append(self._main_hand)
        self._main_hand = weapon
    
    @property
    def other_hand(self):
        return self._other_hand
    
    @other_hand.setter
    def other_hand(self, weapon):
        if self._other_hand != None:
            self._other_hand.unequip()
            if self._other_hand not in self.storage:
                self.storage.append(self._other_hand)
        self._other_hand = weapon
    
    def available_for_slot(self, slot, storage=None):
        if storage == None:
            storage = self.storage
        slots = {
        'belt1': ['offhand', 'versatile'],
        'belt2': ['offhand', 'versatile'],
        'harness': ['offhand', 'versatile', 'shield', 'twohanded'],
        'armband': ['offhand'],
        'ankleband': ['offhand']
        }
        list_ = []
        if slot in self.armor_slots():
            for item in storage:
                if item.type == 'armor':
                    list_.append(item)
        else:
            for item in storage:
                if item.type != 'armor':
                    if item.size in slots[slot]:
                        list_.append(item)
        return list_

    def equip_on_slot(self, slot, item):
        slots = 'carried_armor' if slot in self.armor_slots() else 'carried_weapons'
        dict_ = getattr(self, slots)
        current_item = dict_[slot]
        if current_item != None:
            self.storage.append(current_item)
        if item in self.storage:
            self.storage.remove(item)
        dict_[slot] = item

    def equip_weapon(self, weapon, hand='main_hand'):
        if weapon in self.storage:
            self.storage.remove(weapon)
        if weapon.size == 'twohanded':
            self.main_hand = weapon
            self.other_hand = weapon
        else:
            other = 'other_hand' if hand=='main_hand' else 'main_hand'
            if getattr(self, other).size == 'twohanded':
                setattr(self, other, None)
            setattr(self, hand, weapon)

    def disarm_weapon(self, hand):
        setattr(self, hand, None)

    def equip_armor(self, armor, slot):
        if armor in self.storage:
            self.storage.remove(armor)
        if getattr(self, slot) != None:
            self.storage.append(getattr(self, slot))
        setattr(self, slot, armor)

    def is_slot_active(self, slot):
        slots = 'carried_armor' if slot in self.armor_slots() else 'carried_weapons'
        slots = getattr(self, slots)
        return any(self.available_for_slot(slot)) or slots[slot] != None



def get_avatars():
    all_ = renpy.list_files()
    avas = [str_ for str_ in all_ if str_.startswith('images/avatar')]
    return avas



def gen_random_person(genus=None):
    if genus != None:
        for g in available_genuses():
            if g.get_name() == genus:
                genus = g
                break
    else:
        genus = choice(available_genuses())
    try:
        gender = choice(genus.genders())
    except IndexError:
        gender = None
    try:
        age = choice(genus.ages())
    except IndexError:
        age = None
    p = Person(age, gender, genus.get_name())
    p.random_alignment()
    p.random_features()
    p.random_skills()
    return p

persons_list = []
class Person(object):

    def __init__(self, age=None, gender=None, genus='human'):
        self.player_controlled = False
        self._event_type = 'person'
        self.firstname = u"Anonimous"
        self.surname = u"Anonim"
        self.nickname = u"Anon"
        self.alignment = Alignment()
        self.features = []          # gets Feature() objects and their child's. Add new Feature only with self.add_feature()
        self.tokens = []             # Special resources to activate various events
        self.relations_tendency = {'convention': 0, 'conquest': 0, 'contribution': 0}
        #obedience, dependecy and respect stats
        self._stance = []
        self.avatar_path = ''  

        self.master = None          # If this person is a slave, the master will be set
        self.supervisor = None
        self.slaves = []
        self.subordinates = []
        self.ap = 1
        self.schedule = Schedule(self)
        self.modifiers = ModifiersStorage()
        # init starting features
        
        self.availabe_actions = [] # used if we are playing slave-part


        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.sparks = 0
        self.ration = {
            "amount": 'unlimited',   # 'unlimited', 'limited' by price, 'regime' for figure, 'starvation' no food
            "food_type": "cousine",   # 'forage', 'sperm', 'dry', 'canned', 'cousine'
            "target": 0,           # figures range -2:2
            "limit": 0,             # maximum resources spend to feed character each turn
            "overfeed": 0,
        }
        self.skills = []
        self.specialized_skill = None
        self.focused_skill = None
        self.skills_used = []
        self.factors = []
        self.restrictions = []
        self._needs = init_needs(self)


        self.attributes = {
            'physique': 3,
            'mind': 3,
            'spirit': 3,
            'agility': 3,
            'sensitivity':3
        }
        self.university = {'name': 'study', 'effort': 'bad', 'auto': False}
        self.mood = 0
        self.fatigue = 0
        self._vitality = 0
        self.appetite = 0
        self.calorie_storage = 0
        self.money = 0
        self._determination = 0
        self._anxiety = 0
        self.rewards = []
        self.used_rewards = []
        self.merit = 0 # player only var for storing work result

        # Other persons known and relations with them, value[1] = [needed points, current points]
        self._relations = []
        self.selfesteem = 0
        self.conditions = []
        self.genus = init_genus(self, genus)
        self.add_feature(age)
        self.add_feature(gender)
        self.set_avatar()
        self._buffs = []
        persons_list.append(self)
        self._main_hand = None
        self._other_hand = None
        self.resources_storage = None
        self.inventory = Inventory()


    def set_resources_storage(self, storage):
        self.resources_storage = storage
    
    #while inventory isn't implemented we need this methods for some test cases
    #they will be removed when inventory system is done.
    @property
    def items(self):
        return self.inventory.storage
    
    @property
    def main_hand(self):
        return self.inventory.main_hand
    
    
    @property
    def other_hand(self):
        return self.inventory.other_hand

    @property
    def armor(self):
        return self.inventory.carried_armor['overgarments']
    
    def has_shield(self):
        try:
            main = self.inventory.main_hand
            other = self.inventory.other_hand
            if main.size == 'shield' or other.size == 'shield':
                return True
        except AttributeError:
            pass
        return False
    
    def equip_weapon(self, weapon, hand='main_hand'):
        self.inventory.equip_weapon(weapon, hand)
    
    def disarm_weapon(self, hand='main_hand'):
        self.inventory.disarm_weapon(hand)
    
    def add_item(self, item):
        self.inventory.storage.append(item)

    def equip_armor(self, item, slot):
        self.inventory.equip_armor(item, slot)

    def equip_item(self, item, slot):
        if item.type == 'armor':
            self.equip_armor(item, slot)
        elif item.type == 'weapon':
            self.equip_weapon(item, slot)
    #end of inventory methods
    
    def set_avatar(self):
        path = 'images/avatar/'
        path += self.genus.head_type + '/'
        if self.gender != None:
            if self.gender == 'sexless':
                gender = 'male'
            elif self.gender == 'shemale':
                gender = 'female'
            else:
                gender = self.gender
            path += gender + '/'
        if self.age != None:
            path += self.age + '/'
        this_avas = [ava for ava in get_avatars() if ava.startswith(path)]
        try:
            avatar = choice(this_avas)
            avatar_split = avatar.split('/')
            for str_ in avatar_split:
                if 'skin' in str_:
                    skin_color = str_.split('_')[0]
                    self.add_feature(skin_color)
                if 'hair' in str_:
                    hair_color = str_.split('_')[0]
                    self.hair_color = hair_color
            self.avatar_path = avatar
        except IndexError:
            self.avatar_path = 'images/avatar/none.jpg'

    def randomise(self, gender='female', age='adolescent'):
        self.add_feature(gender)
        self.add_feature(age)
        self.random_alignment()
        self.random_skills()
        self.random_features()
        return

    def random_alignment(self):
        # roll activity
        roll = randint(1, 100)
        if roll <= 20:
            self.alignment.activity = "timid"
        elif roll > 80:
            self.alignment.activity = "ardent"
        else:
            self.alignment.activity = "reasonable"

        # roll orderliness
        roll = randint(1, 100)
        if roll <= 20:
            self.alignment.orderliness = "chaotic"
        elif roll > 80:
            self.alignment.orderliness = "lawful"
        else:
            self.alignment.orderliness = "conformal"

        # roll morality
        roll = randint(1, 100)
        if roll <= 20:
            self.alignment.morality = "evil"
        elif roll > 80:
            self.alignment.morality = "good"
        else:
            self.alignment.morality = "selfish"

        return

    def random_skills(self, pro_skill=None, talent_skill=None):
        skilltree = list(skills_data.keys())
        skilltree.append(None)
        if talent_skill:
            self.skill(talent_skill).talent = True
        else:
            roll = choice(skilltree)
            if roll:
                self.skill(roll).talent = True

        if pro_skill:
            self.skill('pro_skill').profession()
        else:
            roll = choice(skilltree)
            if roll:
                self.skill(roll).profession()
        return

    def random_features(self):
        # constitution
        const = choice(('athletic', 'brawny',  'large', 'small', 'lean', 'crooked', 'clumsy'))
        roll = randint(1, 100)
        if roll > 40:
            self.add_feature(const)

        # soul
        soul = choice(('brave', 'shy', 'smart', 'dumb', 'sensitive', 'cool', None))
        if soul:
            self.add_feature(soul)

        # needs
        needstree = {'prosperity_feat': ('greedy', 'generous'),
                     'nutrition_feat': ('gourmet', 'moderate_eater'),
                     'wellness_feat': ('low_pain_threshold', 'high_pain_threshold'),
                     'comfort_feat': ('sybarite', 'ascetic'),
                     'activity_feat': ('energetic', 'lazy'),
                     'communication_feat': ('extrovert', 'introvert'),
                     'amusement_feat': ('curious', 'dull'),
                     'authority_feat': ('dominant', 'submissive'),
                     'ambition_feat': ('ambitious', 'modest'),
                     'eros_feat': ('lewd', 'frigid'), }
        for need in needstree:
            roll = randint(1, 100)
            if roll <= 20:
                self.add_feature(needstree[need][0])
            elif roll > 80:
                self.add_feature(needstree[need][1])

        return
    def change_genus(self, genus):
        self.genus = init_genus(self, genus)
    @property
    def known_characters(self):
        list_ = []
        for r in self._relations:
            persons = [p for p in r.persons if p != self]
            list_ += persons
        return list_
    
    def add_modifier(self, name, stats_dict, source, slot=None):
        self.modifiers.add_modifier(name, stats_dict, source, slot)

    def get_buff_storage(self):
        return self._buffs
    

    def add_buff(self, name, stats_dict, time=1, slot=None):
        self.remove_buff(name)
        Buff(self, name, stats_dict, slot, time)


    def remove_buff(self, name):
        for buff in self._buffs:
            if buff.name == name:
                buff.remove()

    def has_buff(self, name):
        for buff in self._buffs:
            if buff.name == name:
                return True
        return False

    def tick_buffs_time(self):
        for buff in self._buffs:
            buff.tick_time()

    def count_modifiers(self, key):
        val = self.__dict__['modifiers'].count_modifiers(key)
        return val
    
    @property
    def focus(self):
        try:
            return self.focused_skill.focus
        except AttributeError:
            return 0
    
    @property
    def job(self):
        job = self.schedule.find_by_slot('job')
        if job == None:
            return 'idle'
        else:
            return job.name
    
    @property
    def accommodation(self):
        accomodation = self.schedule.find_by_slot('accommodation')
        if accomodation == None:
            raise Exception('Person %s do not have accommodation'%(self.name))
        return accomodation.name
    
    @property
    def overtime(self):
        overtime = self.schedule.find_by_slot('overtime')
        if overtime == None:
            return 'idle'
        else:
            return overtime.name

    


    def job_object(self):
        job = self.schedule.find_by_slot('job')
        if not job:
            return None
        else:
            return job
    def __getattribute__(self, key):
        if not key.startswith('__') and not key.endswith('__'):
            try:
                genus = super(Person, self).__getattribute__('genus')
                value = getattr(genus, key)
                genus.last_caller = self
                return value
            except AttributeError:
                pass
        return super(Person, self).__getattribute__(key)

    def __getattr__(self, key):
        if 'attributes' in self.__dict__:
            if key in self.__dict__['attributes']:
                value = self.__dict__['attributes'][key]
                value += self.count_modifiers(key)
                if value < 1:
                    value = 1
                if value > 5:
                    value = 5
                return value
        n = {}
        if '_needs' in self.__dict__:
            for need in self.__dict__['_needs']:
                n[need.name] = need
        if key in n.keys():
            return n[key]
        raise AttributeError(key)


    def __setattr__(self, key, value):
        if 'attributes' in self.__dict__:
            if key in self.attributes:
                value -= self.count_modifiers(key)
                self.attributes[key] = value
                if self.attributes[key] < 0:
                    self.attributes[key] = 0
        super(Person, self).__setattr__(key, value)

    @property
    def determination(self):
        return self._determination
    @determination.setter
    def determination(self, value):
        self._determination = value
        if self._determination < 0:
            self._determination = 0
    @property
    def anxiety(self):
        return self._anxiety
    @anxiety.setter
    def anxiety(self, value):
        self._anxiety = value
        if self._anxiety < 0:
            self_anxiety = 0


    def modifiers_separate(self, modifier, names=False):
        return self.modifiers.get_modifier_separate(modifier)
    
    def vitality_info(self):
        d = {'physique': self.physique, 'shape': self.count_modifiers('shape'), 'fitness':self.count_modifiers('fitness'),
            'mood': self.mood, 'therapy': self.count_modifiers('therapy')}
        list_ = self.modifiers_separate('vitality', True)
        list_ = [(value.name, value.value) for value in list_]
        return d, list_
    
    @property
    def vitality(self):
        list_ = [self.physique, self.count_modifiers('shape'), self.count_modifiers('fitness'), self.mood,
            self.count_modifiers('therapy')]
        list_ += self.modifiers_separate('vitality')
        list_ = [i for i in list_ if i != 0]
        lgood = []
        lbad = []
        for i in list_:
            if i > 0:
                lgood.append(i)
            elif i < 0:
                lbad.append(i)
        val = 0
        bad = len(lbad)
        lgood.sort()
        for i in range(bad):
            try:
                lgood.pop(0)
            except IndexError:
                return 0
        while len(lgood) > 0:
            num = min(lgood)
            if num > val:
                val += 1
            lgood.remove(num)
        val += self._vitality
        if val > 5:
            val = 5
        return val

    # person gender relies on feature with slot 'gender'
    @property
    def gender(self):
        try:
            gender = self.feature_by_slot('gender').name
            return gender
        except AttributeError:
            return None

    # person gender relies on feature with slot 'age'
    @property
    def age(self):
        try:
            gender = self.feature_by_slot('age').name
            return gender
        except AttributeError:
            return None
    
    #maybe we won't need phobias any more
    def phobias(self):
        l = []
        for feature in self.features:
            if isinstance(feature, Phobia):
                l.append(feature.object_of_fear)
        return l
    
    # get needs with level > 0 aka turned on needs
    def get_needs(self):
        d = {}
        for need in self._needs:
            if need.level > 0:
                d[need.name] = need
        return d
    
    # get all needs person has
    def get_all_needs(self):
        d = {}
        for need in self._needs:
            d[need.name] = need
        return d
    
    # show methods returns strings, to simplify displaying various stats to player
    def show_taboos(self):
        s = ""
        for taboo in self.taboos:
            if taboo.value != 0:
                s += "{taboo.name}({taboo.value}), ".format(taboo=taboo)
        return s


    def show_needs(self):
        s = ""
        for need in self.get_needs().values():
            s += "{need.name}({need.level}), ".format(need=need)
        return s

    def show_features(self):
        s = ""
        for feature in self.features:
            if feature.visible:
                s += "{feature.name}, ".format(feature=feature)
        return s

    def show_focus(self):
        if isinstance(self.focused_skill, Skill):
            return self.focused_skill.name
        else:
            return "No focused skill"

    def show_skills(self):
        s = ""
        for skill in self.skills:
            s += "{name}({skill.level}, {skill.attribute}({value}))".format(name=skill.name, skill=skill, value=skill.attribute_value())
            if skill != self.skills[len(self.skills)-1]:
                s += ', '
        return s

    def show_mood(self):
        m = {-1: '!!!CRUSHED!!!', 0: 'Gloomy', 1: 'Tense', 2:'Content', 3: 'Serene', 4: 'Jouful', 5:'Enthusiastic'}
        mood = self.mood
        return "{mood}({val})".format(mood=m[mood], val=mood)


    def show_attributes(self):
        s = ""
        for key in self.attributes.keys():
            s += "{0}({1})".format(key, getattr(self, key))
        return s


    def show_tokens_difficulty(self):
        s = ""
        for key, value in self.tokens_difficulty.items():
            s += "{0}({1}), ".format(key, value)
        return s
    
    def show_job(self):
        job = self.schedule.find_by_slot('job')
        if not job:
            return 'idle'
        else:
            values = []
            s = ''
            for k, v in job.special_values.items():
                s += '%s: '%(k)
                try:
                    l = [i for i in v]
                    try:
                        for i in l:
                            s += '%s, '%(i.name())
                    except AttributeError:
                        for i in l:
                            s += '%s, '%(i)
                except TypeError:
                    try:
                        s += '%s, '%(v.name())
                    except AttributeError:
                        s += '%s, '%(v)
                if k not in job.special_values.items()[-1]:
                    s += '\n'
            return '%s, %s'%(job.name, s)
    
    @property
    def name(self):
        s = self.firstname + " " + self.surname
        return s
  
    def skill(self, skillname):
        skill = None
        for i in self.skills:
            if i.name == skillname:
                skill = i
                return skill
            
        if skillname in skills_data:
            skill = Skill(self, skillname, skills_data[skillname])
            self.skills.append(skill)
            return skill
        else:
            raise Exception("No skill named %s in skills_data"%(skillname))
        


    def tick_features(self):
        for feature in self.features:
            feature.tick_time()
    
    def use_skill(self, name):
        if isinstance(name, Skill):
            self.skills_used.append(name)
        else:
            self.skills_used.append(self.skill(name))
    def get_used_skills(self):
        l = []
        for skill in self.skills_used:
            if isinstance(skill, Skill):
                l.append(skill)
            else:
                l.append(self.skill(skill))
        return l
    def calc_focus(self):
        if self.focused_skill:
            if self.focused_skill in self.get_used_skills():
                self.focused_skill.focus += 1
                self.skills_used = []
                return
        try:
            self.focused_skill.focus = 0
        except AttributeError:
            pass

        if len(self.skills_used) > 0:
            from collections import Counter
            counted = Counter()
            for skill in self.get_used_skills():
                counted[skill.name]+=1
            maximum = max(counted.values())
            result = []
            for skill in counted:
                if counted[skill] == maximum:
                    result.append(skill)
            self.skill(choice(result)).set_focus()
        else:
            self.focused_skill = None
        
        self.skills_used = []

    def recalculate_mood(self):
        mood = 0
        happines = []
        dissapointment = []
        dissapointments_inf = []
        satisfactions_inf = collections.defaultdict(list)
        determination = []
        anxiety = []
        for need in self.get_needs().values():
            if need.tension and need.level > 0:
                dissapointment.append(need.level)
                dissapointments_inf.append(need)
            if need.satisfaction > 0:
                happines.append(need.satisfaction)
                satisfactions_inf[need.satisfaction].append(need)
                if need.level == 3:
                    happines.append(need.satisfaction)
                    satisfactions_inf[need.satisfaction].append(need)
        for i in range(self.determination):
            happines.append(1)
            determination.append('determination')
        for i in range(self.anxiety):
            dissapointment.append(1)
            anxiety.append('anxiety')
        hlen = len(happines)
        dlen = len(dissapointment)
        happines.sort()
        dissapointment.sort()
        if renpy.has_label('mood_recalc_result'):
            renpy.call_in_new_context('mood_recalc_result', dissapointments_inf, satisfactions_inf, determination, anxiety, True, self)
        if hlen > dlen:
            dissapointment = []
            for i in range(dlen):
                happines.pop(0)
            threshold = happines.count(5)
            sens = 5-self.sensitivity
            if threshold > sens:
                mood = 5
            elif threshold+happines.count(4) > sens:
                mood = 4
            elif threshold+happines.count(4)+happines.count(3) > sens:
                mood = 3
            elif threshold+happines.count(4)+happines.count(3)+happines.count(2) > sens:
                mood = 2
            elif threshold+happines.count(4)+happines.count(3)+happines.count(2)+happines.count(1) > sens:
                mood = 1

        elif hlen < dlen:
            axniety_holder = self.anxiety
            happines = []
            for i in range(hlen):
                dissapointment.pop(0)
            dissapointment = [i for i in dissapointment if i > 1]
            despair = 6-self.sensitivity-dissapointment.count(2)
            despair2 = dissapointment.count(3)
            if despair < 0:
                if abs(despair) > self.anxiety:
                    self.anxiety += 1
                    mood = -1
            else:
                despair2 -= despair
            if despair2 > 0:
                self.anxiety += despair2
                mood = -1

        
        else:
            mood = 0
        for key in satisfactions_inf:
            for need in satisfactions_inf[key]:
                need.satisfaction = 0
                need.tension = False
        for need in dissapointments_inf:
            need.satisfaction = 0
            need.tension = False
        self.mood = mood



    def motivation(self, skill=None, tense_needs=[], satisfy_needs=[], beneficiar = None, morality=0, special=[]):# needs should be a list of tuples[(need, shift)]
        motiv = 0
        motiv += morality
        for i in special:
            motiv += i
        if skill:
            if self.skill(skill).talent:
                motiv += 1
            elif self.skill(skill).inability:
                motiv -= 1

        intense = []
        self_needs = self.get_needs()
        for need in tense_needs:
            if need in self_needs.keys():
                motiv -= 1
        for need in satisfy_needs:
            if need in self_needs.keys():
                intense.append(self_needs[need].level)
        try:
            maximum = max(intense)
        except ValueError:
            maximum = 0
        motiv += maximum

        if beneficiar:
            if beneficiar == self:
                motiv += 2
            else:
                motiv += self.stance(beneficiar).value
                if self.stance(beneficiar) < 0:
                    motiv = 0
                if beneficiar == self.master or beneficiar == self.supervisor:
                    if self.stance(beneficiar).value == 0:
                        motiv = min(beneficiar.mind, beneficiar.spirit)
                    elif self.stance(beneficiar).value == 2:
                        motiv = 5
        if motiv < 0:
            motiv = 0
        if motiv > 5:
            motiv = 5

        return motiv

    def add_feature(self, id_):    # adds features to person, if mutually exclusive removes old feature
        Feature(self, id_)
    
    def add_phobia(self, id_):
        Phobia(self, id_)
    
    def feature_by_slot(self, slot):        # finds feature which hold needed slot
        for f in self.features:
            if f.slot == slot:
                return f
        return None

    def feature(self, id_):                # finds feature with needed name if exist
        for f in self.features:
            if f.id == id_:
                return f
        return None

    def remove_feature(self, feature):       # feature='str' or Fearutere()
        if isinstance(feature, str):
            for f in self.features:
                if f.name == feature:
                    f.remove()
        else:
            try:
                i = self.features.index(feature)
                self.features[i].remove()
            except ValueError:
                return

    def remove_feature_by_slot(self, slot):
        for f in self.features:
            if f.slot == slot:
                f.remove()
        
    def description(self):
        txt = self.firstname + ' "' + self.nickname + '" ' + self.surname
        txt += '\n'
        for feature in self.features:
            txt += feature.name
            txt += ','
        return txt
    
    def reset_needs(self):
        for need in self.get_all_needs().values():
            need.reset()
    
    def rest(self):
        self.conditions = []
        self.tick_buffs_time()
        self.tick_features()
        self.schedule.use_actions()
        self.fatness_change()
        self.recalculate_mood()
        self.reset_needs()
        self.calc_focus()
        self.reduce_esteem()
        self.schedule.add_action('job_idle')
        self.schedule.add_action('overtime_nap')

    def food_demand(self):
        """
        Evaluate optimal food consumption to maintain current weight.
        :return:
        """
        demand = self.physique
        demand += self.appetite
        demand += self.count_modifiers('food_demand')

        if demand < 1:
            demand = 1

        return demand

    def food_desire(self):
        """
        Evaluate ammount of food character likes to consume.
        :return:
        """
        desire = self.food_demand()
        if self.nutrition.level == 0:
            desire -= 1
        elif self.nutrition.level == 3:
            desire += 1
        if self.feature('obese'):
            desire -= 1
        elif self.feature('emaciated'):
            desire += 2
        elif self.feature('slim'):
            desire += 1
        desire += self.count_modifiers("food_desire")

        if desire < 1:
            desire = 1

        return desire

    def get_food_consumption(self, show_multi=False):
        types = {'sperm': 0, 'forage': 1, 'dry': 1, 'canned': 2, 'cousine': 2}
        value = self.consume_food()
        multiplier = types[self.ration['food_type']]
        value *= multiplier
        if show_multi:
            return value, self.ration['food_type']
        try:
            value = min(self.resources_storage.provision, value)
        except AttributeError:
            pass
        return value
    
    def consume_food(self):
        food_consumed = self.food_desire()
        fatness = self.feature_by_slot('shape')
        if fatness:
            fatness = fatness.name
        flist = ['emaciated' ,'slim', None, 'chubby', 'obese']
        val = flist.index(fatness)
        if self.ration['amount'] == 'starvation':
            food_consumed = 0

        if self.ration['amount'] == 'limited':
            if food_consumed > self.ration["limit"]:
                food_consumed = self.ration["limit"]

        if self.ration['amount'] == 'regime':
            food_consumed = self.food_demand()
            if self.ration['target'] > val:
                food_consumed += 1+self.appetite
            if self.ration['target'] < val:
                food_consumed = self.food_demand() - 1
            if self.ration['target'] == val:
                food_consumed = self.food_demand()
        return food_consumed

    def fatness_change(self):
        consumed = self.get_food_consumption()
        demand = self.food_demand()
        desire = self.food_desire()
        calorie_difference = consumed-demand
        if consumed < desire:
            self.nutrition.set_tension()
        if self.ration['amount'] != 'starvation':
            d = {'sperm': -4, 'forage': 0, 'dry': -2, 'canned': 0, 'cousine': 3}
            if d[self.ration['food_type']] < 0:
                self.nutrition.set_tension()
            else:
                self.nutrition.satisfaction = d[self.ration['food_type']]
        self.calorie_storage += calorie_difference
        fatness = self.feature_by_slot('shape')
        if fatness != None:
            fatness = fatness.name
        flist = ['emaciated' ,'slim', None, 'chubby', 'obese']
        ind = flist.index(fatness)
        if self.calorie_storage <= 0:
            self.remove_feature('dyspnoea')
        if self.calorie_storage >= 0:
            self.remove_feature('starving')
        if self.calorie_storage < 0:
            chance = randint(-10, -1)
            if self.calorie_storage <= chance:
                ind -= 1
                if self.feature('dyspnoea'):
                    self.remove_feature('dyspnoea')
                if ind < 0:
                    ind = 0
                    if self.feature('starving'):
                        self.add_feature('dead')
                    else:
                        self.add_feature('starving')
                f = flist[ind]
                if f:
                    self.add_feature(f)
                else:
                    self.feature_by_slot('shape').remove()
                if not self.feature('starving'):
                    self.calorie_storage = 0
                return 'fatness -'
        if self.calorie_storage > 0:
            chance = randint(1, 10)
            if self.calorie_storage >= chance:
                ind += 1
                if ind > 4:
                    ind = 4
                    if self.feature('dyspnoea'):
                        self.add_feature('diabetes')
                    else:
                        self.add_feature('dyspnoea')
                f = flist[ind]
                if f:
                    self.add_feature(f)
                else:
                    self.feature_by_slot('shape').remove()
                if not self.feature('dyspnoea'):
                    self.calorie_storage = 0
                return 'fatness +'
    def nutrition_change(self, food_consumed):
        if food_consumed < self.food_demand():
            self.ration["overfeed"] -= 1
            chance = randint(-10, -1)
            if self.ration["overfeed"] <= chance:
                self.ration["overfeed"] = 0

        return

    def know_person(self, person):
        if person in self.known_characters:
            return True
        return False
    def _set_relations(self, person):
        relations = Relations(self, person)
        person._relations.append(relations)
        self._relations.append(relations)
        return relations


    def relations(self, person):
        if person==self:
            raise Exception("relations: target and caller is same person")
        if isinstance(person, Faction):
            return self.relations(person.owner)
        if not self.know_person(person):
            relations = self._set_relations(person)
            self._set_stance(person)
            return relations
        for rel in self._relations:
            if self in rel.persons and person in rel.persons:
                return rel
    

    def _set_stance(self, person):
        stance = Stance(self, person)
        self._stance.append(stance)
        person._stance.append(stance)
        return stance

    
    def stance(self, person):
        if person==self:
            raise Exception("stance: target and caller is same person")
        if isinstance(person, Faction):
            return self.stance(person.owner)
        elif not self.know_person(person):
            self._set_relations(person)
            stance = self._set_stance(person)

        else:
            for s in self._stance:
                if self in s.persons and person in s.persons:
                    stance = s
        if person in self.slaves:
            stance._type = 'master'
        elif person == self.master:
            stance._type = 'slave'
        else:
            stance._type = 'neutral'
        return stance


    def use_token(self, token):
        if self.has_token(token):
            self.tokens.remove(token)
        else:
            return "%s has no token named %s"%(self.name(), token)


    def has_token(self, token):
        if token in self.tokens:
            return True
        return False


    def has_any_token(self):
        if len(self.tokens) > 0:
            return True
        return False

    
    def add_token(self, token, free=False):
        if not self.has_token(token):
            self.tokens.append(token)
            if token not in ('accordance', 'antagonism'):
                if not free:
                    self.player_relations().stability += 1
                self.relations_tendency[token] += 1
            renpy.call_in_new_context('lbl_notify', self, token)


    def player_relations(self):
        for rel in self._relations:
            if rel.is_player_relations():
                return rel
        return None

    def moral_action(self, *args, **kwargs):
        #checks moral like person.check_moral, but instantly affect selfesteem
        for arg in args:
            if isinstance(arg, int):
                self.selfesteem += arg
                return 
        result = self.check_moral(*args, **kwargs)
        self.selfesteem += result
        return result
        

    def check_moral(self, *args, **kwargs):
        result = 0
        act = {'ardent': 1, 'reasonable': 0, 'timid': -1}
        moral = {'good': 1, 'selfish': 0, 'evil': -1}
        order = {'lawful': 1, 'conformal': 0, 'chaotic': -1}
        action_tones = {'activity': None, 'morality': None, 'orderliness': None}
        activity = None
        morality = None
        orderliness = None
        target = None
        
        if 'target' in kwargs:
            if isinstance(kwargs['target'], Person):
                target = kwargs['target']
        
        else:
            for arg in args:
                if isinstance(arg, Person):
                    target=arg
        
        for arg in args:
            if arg in act.keys():
                activity = arg
            if arg in moral.keys():
                morality = arg
            if arg in order.keys():
                orderliness = arg
        for k, v in action_tones.items():
            if v:
                valself = getattr(self.alignment, k)
                valact = v
                if valself != 0:
                    if valself + valact == 0:
                        result -= 1
                    elif abs(valself + valact) == 2:
                        result += 1
                elif target:
                    if valact != 0:
                        if getattr(self.relations(target), Alignment.relation_binding[k]) != valact:
                            result -= 1
                        else:
                            result += 1
        return result

    def reduce_esteem(self):
        if self.selfesteem == 0:
            return
        val = 5-self.sensitivity
        if self.selfesteem > 0:
            self.selfesteem -= val
            if val < 0:
                val = 0
        elif self.selfesteem < 0:
            self.selfesteem += val
            if val > 0:
                val = 0


    def enslave(self, target):
        target.master = self
        target.set_supervisor(self)
        self.slaves.append(target)
        self.relations(target)

    def set_supervisor(self, supervisor):
        self.supervisor = supervisor

    def master_stance(self, target):
        if self.player_controlled:
            raise Exception('master_stance is only for npc')
        stance = self.stance(target).level
        l = ['cruel', 'opressive', 'rightful', 'benevolent']
        ind = l.index(stance)
        return ind

    def desirable_relations(self):
        d = {'lawful': ('formal', 'loyality'), 'chaotic': ('intimate', 'scum-slave'),
            'timid': ('delicate', 'worship'), 'ardent': ('intense', 'disciple'),
            'good': ('supporter', 'dedication'), 'evil': ('contradictor', 'henchman')}

        return [d.get(x) for x in self.alignment.description()]

    def willing_available(self):
        if not self.master:
            return []
        rel_check = False
        rel = self.desirable_relations()
        types = [x[1] for x in rel if isinstance(x, tuple)]
        check = [x[0] for x in rel if isinstance(x, tuple)]
        for rel in self.relations(self.master).description():
            if rel in check:
                rel_check = True
                break
        if self.stance(self.master).respect() < self.spirit:
            rel_check = False
        if not self.has_token('accordance'):
            rel_check = False
        if rel_check:
            return types
        else:
            return []


    def attitude_tendency(self):
        n = 0
        token = None
        for k, v in self.relations_tendency.items():
            if v > n:
                n = v
                token = k
        if self.relations_tendency.values().count(n) > 1:
            return None
        return token

    # methods for conditions, person.conditions list cleared after person.rest call
    def add_condition(self, condition):
        if not self.has_condition(condition):
            self.conditions.append(condition)


    def has_condition(self, condition):
        if condition in self.conditions:
            return True
        return False


    def remove_condition(self, condition):
        try:
            self.conditions.remove(condition)
        except ValueError:
            pass
