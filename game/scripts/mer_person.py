# -*- coding: UTF-8 -*-
from random import *
import collections

import renpy.store as store
import renpy.exports as renpy

from features import Feature, Phobia
from skills import Skill
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
from background import Background
from inventory import Inventory
from mer_item import create_weapon, create_armor
import mer_utilities as utilities


def get_avatars(path):
    all_ = renpy.list_files()
    avas = [str_ for str_ in all_ if str_.startswith(path)]
    return avas


def gen_random_person(genus=None, age=None, gender=None, world=None, culture=None, family=None, education=None, occupation=None):
    if genus != None:
        for g in available_genuses():
            if g.get_name() == genus:
                genus = g
                break
    else:
        genus = choice(available_genuses())
    if gender is None:
        try:
            gender = choice(genus.genders())
        except IndexError:
            gender = 'male'
    if age is None:
        try:
            age = choice(genus.ages())
        except IndexError:
            age = 'adolescent'
    p = Person(age, gender, genus.get_name())
    background = Background(world, culture, family, education, occupation)
    p.apply_background(background)
    if gender == 'sexless':
        gender = 'male'
    elif gender == 'shemale':
        gender = 'female'
    try:
        names = store.firstname[background.culture.id][gender]
    except KeyError:
        names = store.firstname['default'][gender]
    p.firstname = choice(names)
    p.random_alignment()
    p.random_features()
    p.random_skills()
    return p

persons_list = []

class Modifiable(object):

    def init_modifiable(self):
        self.modifiers = ModifiersStorage()

    def add_modifier(self, name, stats_dict, source, slot=None):
        self.modifiers.add_modifier(name, stats_dict, source, slot)

    def count_modifiers(self, key):
        val = self.__dict__['modifiers'].count_modifiers(key)
        return val

    def modifiers_separate(self, modifier, names=False):
        return self.modifiers.get_modifier_separate(modifier)

class Skilled(object):

    def init_skilled(self):
        self.skills = []
        self.specialized_skill = None
        self.focused_skill = None
        self.skills_used = []

    def skill(self, skill_id):
        skill = None
        for i in self.skills:
            if i.id == skill_id:
                skill = i
                return skill

        if skill_id in store.skills_data:
            skill = Skill(self, skill_id)
            self.skills.append(skill)
            return skill
        else:
            raise Exception("No skill named %s in skills_data" % (skillname))

    def use_skill(self, id_):
        if isinstance(id_, Skill):
            self.skills_used.append(id_)
        else:
            self.skills_used.append(self.skill(id_))

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
                counted[skill.id] += 1
            maximum = max(counted.values())
            result = []
            for skill in counted:
                if counted[skill] == maximum:
                    result.append(skill)
            self.skill(choice(result)).set_focus()
        else:
            self.focused_skill = None

        self.skills_used = []

class InventoryWielder(object):

    def init_inventorywielder(self):
        self.inventory = Inventory()

    @property
    def items(self):
        return self.inventory.storage

    @property
    def main_hand(self):
        return self.inventory.main_hand

    @main_hand.setter
    def main_hand(self, weapon):
        self.inventory.main_hand = weapon

    @property
    def other_hand(self):
        return self.inventory.other_hand

    @other_hand.setter
    def other_hand(self, weapon):
        self.inventory.other_hand = weapon

    @property
    def armor(self):
        return self.inventory.carried_armor['overgarments']

    @armor.setter
    def armor(self, armor):
        self.inventory.equip_armor(armor, 'overgarments')

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

    def equip_on_slot(self, slot, item):
        self.inventory.equip_on_slot(slot, item)

class Attributed(Modifiable):

    def init_attributed(self):
        self.attributes = {
            'physique': 3,
            'mind': 3,
            'spirit': 3,
            'agility': 3,
            'sensitivity': 3
        }
        self.init_modifiable()

    def _get_modified_attribute(self, attr):
        value = self.attributes[attr]
        value += self.count_modifiers(attr)
        return max(0, min(5, value))

    @property
    def physique(self):
        return self._get_modified_attribute('physique')
    @physique.setter
    def physique(self, value):
        self.attributes['physique'] = value
    
    @property
    def mind(self):
        return self._get_modified_attribute('mind')
    @mind.setter
    def mind(self, value):
        self.attributes['mind'] = value
    
    @property
    def spirit(self):
        return self._get_modified_attribute('spirit')
    @spirit.setter
    def spirit(self, value):
        self.attributes['spirit'] = value
    
    @property
    def agility(self):
        return self._get_modified_attribute('agility')
    @agility.setter
    def agility(self, value):
        self.attributes['agility'] = value
    
    @property
    def sensitivity(self):
        return self._get_modified_attribute('sensitivity')
    @sensitivity.setter
    def sensitivity(self, value):
        self.attributes['sensitivity'] = value

def get_random_combatant():
    return choice(store.combatant_data.keys())

def get_random_item_set():
    return choice(store.equip_sets.keys())

def make_combatant(id_=None):
    if id_ is None:
        id_ = get_random_combatant()
    data = store.combatant_data[id_]
    name = data['name']
    combatant = Combatant(name)
    combatant.set_avatar(data['avatar_folder'])
    for key, value in data['attributes'].items():
        setattr(combatant, key, value)
    return combatant

def equip_combatant(combatant, equip_set_id=None):
    if equip_set_id is None:
        equip_set_id = get_random_item_set()
    data = store.equip_sets[equip_set_id]
    for key, value in data.items():
        if key == 'main_hand' or key == 'other_hand':
            item = create_weapon(**value)
        elif key == 'armor':
            item = create_armor(**value)
        setattr(combatant, key, item)

class Combatant(Skilled, InventoryWielder, Attributed):
    def __init__(self, name):
        super(Combatant, self).__init__()
        self.init_inventorywielder()
        self.init_skilled()
        self.init_attributed()
        self.name = name
    
    def set_avatar(self, avatar_folder):
        path = 'images/avatar/combatants/'
        path += avatar_folder
        avatars = get_avatars(path)
        try:
            avatar = choice(avatars)
        except IndexError:
            self.avatar_path = utilities.default_avatar_path()
            return 
        else:
            self.avatar_path = avatar


class FoodSystem(object):
    
    features_list = ['emaciated', 'slim', None, 'chubby', 'obese']
    def __init__(self, owner):
        self.owner = owner
        self.satiety = 0
        self.quality = 0
        self.quality_changed = False
        self.amount = 0

    def set_starvation(self):
        self.quality = 0
        self.quality_changed = False
        self.amount = 0

    def set_food(self, amount, quality):
        self.quality_changed = True
        self.amount = max(self.amount, amount)
        if self.quality_changed:
            self.quality = min(self.quality, quality)
        else:
            self.quality = quality

    def food_info(self):
        amount = store.food_amount_dict[self.amount]
        if self.quality < 0:
            quality_encolor = 0
        else:
            quality_encolor = self.quality
        quality = store.food_quality_dict[self.quality]
        text = '%s'%(utilities.encolor_text(quality, quality_encolor))
        if self.amount != 2:
            amount = utilities.encolor_text(amount, self.amount)
            text += '(%s)'%(amount)
        if self.amount < 1:
            return utilities.encolor_text(amount, 0)
        else:
            return text
    
    def increase_shape(self, index):
        flist = self.features_list
        self.owner.remove_feature('emaciated')
        try:
            new_shape = flist[index]
        except IndexError:
            new_shape = 'max'
        if new_shape != 'max':
            if new_shape is None:
                self.owner.remove_feature_by_slot('shape')
            else:
                self.owner.add_feature(new_shape)
        else:
            if not self.owner.has_feature('dyspnoea'):
                self.owner.add_feature('dyspnoea')
            else:
                random_num = randint(1, 10)
                satiety = min(satiety, self.owner.physique)
                if random_num <= satiety:
                    self.owner.add_feature('diabetes')

    def decrease_shape(self, index):
        flist = self.features_list
        self.owner.remove_feature('dyspnoea')
        try:
            new_shape = flist[index]
        except IndexError:
            new_shape = 'min'
        if new_shape != 'min':
            if new_shape is None:
                self.owner.remove_feature_by_slot('shape')
            else:
                self.owner.add_feature(new_shape)
        else:
            if not self.owner.has_feature('emaciated'):
                self.owner.add_feature('emaciated')
            elif self.amount < 1:
                self.owner.die()

    def is_good_feed(self):
        return (not self.owner.has_feature('diabetes')
                or not self.owner.has_feature('obese'))

    def is_bad_feed(self):
        return (self.owner.has_feature('slim') or
                self.owner.has_feature('emaciated'))
    
    def fatness_change(self):
        flist = self.features_list
        shape = self.owner.feature_by_slot('shape')
        if self.owner.has_condition('workout'):
            self.satiety -= 1
        if shape is not None:
            shape = shape.name
        index = flist.index(shape)
        
        if self.amount < 1:
            total = 0
        elif self.quality < 0:
            total = 0 
        else:
            total = max(0, min(5, self.quality + self.amount - 2))
        if total > 0:
            self.owner.nutrition.set_satisfaction(total)
        else:
            self.owner.nutrition.set_tension()
        if self.amount == 3:
            self.satiety += self.amount - 2
        elif self.amount == 1:
            self.satiety = -1
        elif self.amount == 0:
            if self.satiety > 0:
                self.satiety = -1
            else:
                self.satiety += self.satiety - 1
        
        if self.satiety > self.owner.physique:
            index += 1
            self.increase_shape(index)
            if not self.owner.has_feature('dyspnoea'):
                self.satiety = 0
            else:
                self.satiety = min(self.satiety, self.owner.physique)
            
        if self.satiety < -(6 - self.owner.physique):
            index -= 1
            self.decrease_shape(index)
            if not self.owner.has_feature('emaciated'):
                self.satiety = 0
            else:
                self.satiety = max(self.satiety, -(6-self.owner.physique))
            
        if self.satiety > 0 and self.is_good_feed():
            self.owner.add_buff('overfeed')
        elif self.satiety < 0 or self.is_bad_feed():
            self.owner.add_buff('underfeed')
        self.set_starvation()

class Person(Skilled, InventoryWielder, Attributed):

    def __init__(self, age=None, gender=None, genus='human'):
        super(Person, self).__init__()
        self.player_controlled = False
        self.init_inventorywielder()
        self.init_skilled()
        self.init_attributed()
        self._event_type = 'person'
        self.firstname = u"Anonimous"
        self.surname = u""
        self.nickname = u"Anon"
        self.alignment = Alignment()
        # gets Feature() objects and their child's. Add new Feature only with
        # self.add_feature()
        self.features = []
        self.tokens = []             # Special resources to activate various events
        self.relations_tendency = {'convention': 0,
                                   'conquest': 0, 'contribution': 0}
        # obedience, dependecy and respect stats
        self._stance = []
        self.avatar_path = ''

        self.master = None          # If this person is a slave, the master will be set
        self.supervisor = None
        self.slaves = []
        self.subordinates = []
        self.ap = 1
        self.schedule = Schedule(self)
        # init starting features

        self.availabe_actions = []  # used if we are playing slave-part

        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.sparks = 0
        self.ration = {
            # 'unlimited', 'limited' by price, 'regime' for figure, 'starvation' no food
            "amount": 'unlimited',
            "food_type": "cousine",   # 'forage', 'sperm', 'dry', 'canned', 'cousine'
            "target": 0,           # figures range -2:2
            "limit": 0,             # maximum resources spend to feed character each turn
            "overfeed": 0,
        }
        self.factors = []
        self.restrictions = []
        self._needs = init_needs(self)

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
        self.merit = 0  # player only var for storing work result

        # Other persons known and relations with them, value[1] = [needed
        # points, current points]
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
        self.cards_list = []
        self.default_cards = False
        self.deck = None
        self._calculatable = False
        self.factions = []
        self.background = None
        self.food_system = FoodSystem(self)
        self.favor = 0

    def apply_background(self, background):
        self.background = background
        background.apply(self)

    def add_faction(self, faction):
        if not faction in self.factions:
            self.factions.append(faction)

    def remove_faction(self, faction):
        try:
            self.factions.remove(faction)
        except IndexError:
            pass

    def eat(self, amount, quality):
        self.food_system.set_food(amount, quality)

    def food_info(self):
        return self.food_system.food_info()

    @property
    def calculatable(self):
        return self._calculatable or self.player_controlled

    @calculatable.setter
    def calculatable(self, value):
        self._calculatable = value

    def add_default_cards(self, list_):
        if not self.default_cards:
            self.cards_list += list_
        return

    def set_deck(self, deck):
        self.deck = deck

    def set_resources_storage(self, storage):
        self.resources_storage = storage

    def formidability(self):
        value = 0
        weapons = self.inventory.equiped_weapons()
        armor = self.inventory.carried_armor['overgarments']
        shape = self.feature_by_slot('shape')
        if self.gender == 'male':
            value += 1
        elif self.gender == 'female':
            value -= 1
        if armor is not None:
            if armor.protection_type == 'heavy':
                value += 1
        else:
            value -= 1
        if not self.inventory.visible_weapon():
            value -= 1
        for weapon in weapons:
            if weapon.size == 'versatile':
                value += 1
                break
        for weapon in weapons:
            if weapon.size == 'twohanded':
                value += 1
                break
        if self.age == 'junior' or self.age == 'elder':
            value -= 1
        elif self.age == 'mature':
            value += 1
        value += self.physique - 3
        if shape is not None:
            if shape.id == 'slim' or shape.id == 'emaciated':
                value -= 1
            elif shape.id == 'obese':
                value += 1
        if self.skill('combat').level > 2:
            value += 1
        return max(0, min(5, value))

    def alure(self):
        value = 0
        shape = self.feature_by_slot('shape')
        if self.gender == 'male':
            value -= 1
        elif self.gender == 'female':
            value += 1
        value += self.sensitivity - 3
        if shape is not None:
            if shape.id == 'slim' or shape.id == 'obese':
                value += 1
            elif shape.id == 'emaciated':
                value -= 1
        if self.age == 'adolescent':
            value += 1
        elif self.age == 'elder':
            value -= 1
        if self.skill('expression').level > 2:
            value += 1
        return max(0, min(5, value))

    def set_avatar(self, avatar=None):
        if avatar is not None:
            if avatar in renpy.list_files():
                self.avatar_path = avatar
            else:
                self.avatar_path = utilities.default_avatar_path()
            return
        path = 'images/avatar/'
        path += self.genus.head_type + '/'
        if self.gender is not None:
            if self.gender == 'sexless':
                gender = 'male'
            elif self.gender == 'shemale':
                gender = 'female'
            else:
                gender = self.gender
            path += gender + '/'
        if self.age is not None:
            path += self.age + '/'
        this_avas = get_avatars(path)
        try:
            avatar = choice(this_avas)
        except IndexError:
            self.avatar_path = utilities.default_avatar_path()
            return
        avatar_split = avatar.split('/')
        for str_ in avatar_split:
            if 'skin' in str_:
                skin_color = str_.split('_')[0]
                self.add_feature(skin_color)
            if 'hair' in str_:
                hair_color = str_.split('_')[0]
                self.hair_color = hair_color
        self.avatar_path = avatar

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
        skilltree = list(store.skills_data.keys())
        skilltree.append(None)
        if talent_skill is not None:
            self.skill(talent_skill).talent = True
        else:
            roll = choice(skilltree)
            if roll:
                self.skill(roll).talent = True

        if pro_skill is not None:
            self.skill(pro_skill).profession()
        else:
            roll = choice(skilltree)
            if roll:
                self.skill(roll).profession()
        return

    def random_features(self):
        # constitution
        const = choice(('athletic', 'brawny',  'large',
                        'small', 'lean', 'crooked', 'clumsy'))
        roll = randint(1, 100)
        if roll > 40:
            self.add_feature(const)

        # soul
        soul = choice(('brave', 'shy', 'smart', 'dumb',
                       'sensitive', 'cool', None))
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

    

    def get_buff_storage(self):
        return self._buffs

    def add_buff(self, id_, time=1, slot=None):
        if slot is not None:
            self.remove_buff(slot)
        Buff(self, id_, time)

    def remove_buff(self, id_):
        for buff in self._buffs:
            if buff.id == id_:
                buff.remove()
        

    def remove_buff_by_slot(self, slot):
        for buff in self._buffs:
            if buff.slot == slot:
                buff.remove()
    
    def has_buff(self, id_):
        for buff in self._buffs:
            if buff.id == id_:
                return True
        return False

    def tick_buffs_time(self):
        for buff in self._buffs:
            buff.tick_time()


    @property
    def focus(self):
        try:
            return self.focused_skill.focus
        except AttributeError:
            return 0

    @property
    def job(self):
        job = self.schedule.find_by_slot('job')
        if job is None:
            return 'idle'
        else:
            return job.name

    @property
    def accommodation(self):
        accomodation = self.schedule.find_by_slot('accommodation')
        if accomodation is None:
            raise Exception(
                'Person %s do not have accommodation' % (self.name))
        return accomodation.name

    @property
    def overtime(self):
        overtime = self.schedule.find_by_slot('overtime')
        if overtime is None:
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
        n = {}
        if '_needs' in self.__dict__:
            for need in self.__dict__['_needs']:
                n[need.name] = need
        if key in n.keys():
            return n[key]
        raise AttributeError(key)

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

    def vitality_info(self):
        d = {'physique': self.physique, 'shape': self.count_modifiers('shape'), 'fitness': self.count_modifiers('fitness'),
             'mood': self.mood, 'therapy': self.count_modifiers('therapy')}
        list_ = self.modifiers_separate('vitality', True)
        list_ = [(value.name, value.value) for value in list_]
        return d, list_

    @property
    def vitality(self):
        list_ = [self.physique, self.count_modifiers('shape'), self.count_modifiers('fitness'), self.mood,
                 self.count_modifiers('therapy')]
        vitality_mods = self.modifiers_separate('vitality')
        list_.extend([modifier.value for modifier in vitality_mods])
        print list_
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
        try:
            for i in range(bad):
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

    # show methods returns strings, to simplify displaying various stats to
    # player
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
            s += "{name}({skill.level}, {skill.attribute}({value}))".format(
                name=skill.name, skill=skill, value=skill.attribute_value())
            if skill != self.skills[len(self.skills) - 1]:
                s += ', '
        return s

    def show_mood(self):
        m = {-1: '!!!CRUSHED!!!', 0: 'Gloomy', 1: 'Tense',
             2: 'Content', 3: 'Serene', 4: 'Jouful', 5: 'Enthusiastic'}
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
                s += '%s: ' % (k)
                try:
                    l = [i for i in v]
                    try:
                        for i in l:
                            s += '%s, ' % (i.name())
                    except AttributeError:
                        for i in l:
                            s += '%s, ' % (i)
                except TypeError:
                    try:
                        s += '%s, ' % (v.name())
                    except AttributeError:
                        s += '%s, ' % (v)
                if k not in job.special_values.items()[-1]:
                    s += '\n'
            return '%s, %s' % (job.name, s)

    @property
    def name(self):
        s = self.firstname + " " + self.surname
        return s

    def tick_features(self):
        for feature in self.features:
            feature.tick_time()

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
            renpy.call_in_new_context('mood_recalc_result', dissapointments_inf,
                                      satisfactions_inf, determination, anxiety, True, self)
        if hlen > dlen:
            dissapointment = []
            for i in range(dlen):
                happines.pop(0)
            threshold = happines.count(5)
            sens = 5 - self.sensitivity
            if threshold > sens:
                mood = 5
            elif threshold + happines.count(4) > sens:
                mood = 4
            elif threshold + happines.count(4) + happines.count(3) > sens:
                mood = 3
            elif threshold + happines.count(4) + happines.count(3) + happines.count(2) > sens:
                mood = 2
            elif threshold + happines.count(4) + happines.count(3) + happines.count(2) + happines.count(1) > sens:
                mood = 1
        elif hlen < dlen:
            axniety_holder = self.anxiety
            happines = []
            for i in range(hlen):
                dissapointment.pop(0)
            dissapointment = [i for i in dissapointment if i > 1]
            despair = 6 - self.sensitivity - dissapointment.count(2)
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
        self.mood = mood

    # needs should be a list of tuples[(need, shift)]
    def motivation(self, skill=None, tense_needs=[], satisfy_needs=[], beneficiar=None, morality=0, special=[]):
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

    # adds features to person, if mutually exclusive removes old feature
    def add_feature(self, id_):
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

    def has_feature(self, id_):
        return self.feature(id_) is not None

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
        if not self.calculatable:
            return
        self.food_system.fatness_change()
        self.recalculate_mood()
        self.reset_needs()
        self.calc_focus()
        self.reduce_esteem()
        self.gain_favor()
    def tick_time(self):
        if not self.calculatable:
            return
        self.conditions = []
        self.tick_buffs_time()
        self.tick_features()
    def tick_schedule(self):
        if not self.calculatable:
            return
        self.schedule.use_actions()
        self.schedule.add_action('job_idle')
        self.schedule.add_action('overtime_nap')

    #testing new food system, food methods are unused for some time
    #and maybe we'll remove them
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
        flist = ['emaciated', 'slim', None, 'chubby', 'obese']
        val = flist.index(fatness)
        if self.ration['amount'] == 'starvation':
            food_consumed = 0

        if self.ration['amount'] == 'limited':
            if food_consumed > self.ration["limit"]:
                food_consumed = self.ration["limit"]

        if self.ration['amount'] == 'regime':
            food_consumed = self.food_demand()
            if self.ration['target'] > val:
                food_consumed += 1 + self.appetite
            if self.ration['target'] < val:
                food_consumed = self.food_demand() - 1
            if self.ration['target'] == val:
                food_consumed = self.food_demand()
        return food_consumed

    def fatness_change(self):
        consumed = self.get_food_consumption()
        demand = self.food_demand()
        desire = self.food_desire()
        calorie_difference = consumed - demand
        if consumed < desire:
            self.nutrition.set_tension()
        if consumed > 0:
            d = {'sperm': -4, 'forage': 0, 'dry': -2, 'canned': 0, 'cousine': 3}
            if d[self.ration['food_type']] < 0:
                self.nutrition.set_tension()
            else:
                self.nutrition.satisfaction = d[self.ration['food_type']]
        self.calorie_storage += calorie_difference
        fatness = self.feature_by_slot('shape')
        if fatness is not None:
            fatness = fatness.name
        flist = ['emaciated', 'slim', None, 'chubby', 'obese']
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
                        self.die()
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
    #end of food methods


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
        if person == self:
            raise Exception("relations: target and caller is same person")
        if isinstance(person, Faction):
            return self.relations(person.owner)
        elif not isinstance(person, Person):
            raise Exception("relations called with not valid arg: %s" % person)
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
        if person == self:
            raise Exception("stance: target and caller is same person")
        if isinstance(person, Faction):
            return self.stance(person.owner)
        elif not isinstance(person, Person):
            raise Exception("relations called with not valid arg: %s" % person)
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
            return "%s has no token named %s" % (self.name(), token)

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

    def player_stance(self):
        for i in self._stance:
            if i.is_player_stance():
                return i

    def moral_action(self, *args, **kwargs):
        # checks moral like person.check_moral, but instantly affect selfesteem
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
        action_tones = {'activity': None,
                        'morality': None, 'orderliness': None}
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
                    target = arg
        toned = False
        for arg in args:
            if isinstance(arg, list):
                toned = True
                for i in arg:
                    if i in act.keys():
                        activity = i
                    if i in moral.keys():
                        morality = i
                    if i in order.keys():
                        orderliness = i
        if not toned:
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
        val = 5 - self.sensitivity
        if self.selfesteem > 0:
            self.purporse.set_satisfaction(self.selfesteem)
            self.selfesteem -= val
            if val < 0:
                val = 0
        elif self.selfesteem < 0:
            self.purporse.set_tension()
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
        list_ = [self.alignment.morality_str(), self.alignment.orderliness_str(),
                 self.alignment.activity_str()]
        return [d.get(x) for x in list_]

    def willing_available(self):
        if not self.master:
            return []
        rel_check = False
        rel = self.desirable_relations()
        types = [x[1] for x in rel if isinstance(x, tuple)]
        check = [x[0] for x in rel if isinstance(x, tuple)]
        relations = self.relations(self.master)
        for rel in [relations.fervor_str(), relations.distance_str(), relations.congruence_str()]:
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
        if self.player_controlled:
            raise Exception("attitude_tendency called at player character")
        n = 0
        token = None
        for k, v in self.relations_tendency.items():
            if v > n:
                n = v
                token = k
        if self.relations_tendency.values().count(n) > 1:
            return 'complicated'
        return token

    def gain_favor(self, value):
        if self.player_controlled:
            return
        value = self.favor + value
        if value < 0:
            self.favor = 0
            return
        hard_max = 5
        soft_max = 3+self.player_stance().value()
        self.favor = min(hard_max, min(soft_favor, value))

    def favor_income(self):
        relations = self.player_relations()
        if relations is None:
            return
        value = 0
        stance = self.player_stance().value()
        actual_relations = [relations.fervor_str(), relations.congruence_str(), relations.distance_str()]
        tendency = self.attitude_tendency
        if tendency == 'conquest':
            needed_relations = ['passionate', 'intimate', 'contradictor']
            for i in actual_relations:
                if i in needed_relations:
                    value += 1
            value += 2-stance
        elif tendency == 'contribution':
            needed_relations = ['passionate', 'intimate', 'supporter']
            value += stance
            for i in actual_relations:
                if i in needed_relations:
                    value += 1
        elif tendency == 'convention':
            needed_relations = ['formal', 'delicate', 'supporter']
            bad_relations = ['passionate', 'intimate', 'contradictor']
            value += stance
            for i in actual_relations:
                if i in needed_Relations:
                    value += 1
                elif i in bad_relations:
                    value -= 1
        elif tendency is None:
            value += stance
            value += relations.harmony()[0]
        self.gain_favor(value)

    # methods for conditions, person.conditions list cleared after person.rest
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

    def die(self):
        if self.player_controlled:
            renpy.call('lbl_gameover')
        self.add_feature('dead')

    def is_dead(self):
        if self.feature('dead') is not None:
            return True
        return False
