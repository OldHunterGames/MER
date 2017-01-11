# -*- coding: UTF-8 -*-
from random import *
import collections
from copy import copy
from copy import deepcopy

import renpy.store as store
import renpy.exports as renpy

from features import Feature, Phobia
from skills import Skilled
from needs import init_needs

from schedule import *
from relations import Relations
from stance import Stance
from genus import available_genuses, Genus
from alignment import Alignment
from modifiers import ModifiersStorage, Modifiable
from factions import Faction
from buffs import Buff
from background import Background
from inventory import Inventory, InventoryWielder
from mer_item import create_weapon, create_armor
from mer_resources import BarterSystem
import mer_utilities as utilities
from mer_event import call_event


def get_avatars(path):
    all_ = renpy.list_files()
    avas = [str_ for str_ in all_ if str_.startswith(path)]
    return avas


def gen_random_person(genus=None, age=None, gender=None, world=None, culture=None, family=None, education=None, occupation=None):
    if genus != None:
        if genus not in available_genuses():
            raise Exception("gen_person with genus '%s' which not exists"%(genus))
    else:
        genus = choice(available_genuses())
    genus = Genus(genus)
    if gender is None:
        try:
            gender = choice(genus.genders)
        except IndexError:
            gender = 'male'
    if age is None:
        try:
            age = choice(genus.ages)
        except IndexError:
            age = 'adolescent'
    p = Person(age, gender, genus)
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
    gen_sex_traits(p)
    return p

persons_list = []

def gen_sex_traits(person):
    kink_data = store.kink_types
    kink = choice(kink_data.keys())
    person.kink = kink
    genders_data = store.gender_types
    gender = person.gender
    basic = store.basic_preferences
    get_traits_from_dict(person, kink_data[kink])
    get_traits_from_dict(person, genders_data[gender])
    get_traits_from_dict(person, basic)

def get_traits_from_dict(person, dict): 
    for key, value in dict.items():
        roll = trait_chance(*value)
        if roll == 'fetish':
            person.add_fetish(key)
        elif roll == 'taboo':
            person.add_taboo(key)




def trait_chance(fetish_value, taboo_value):
    roll = randint(1, 10)
    if roll <= fetish_value:
        return 'fetish'
    elif roll <= fetish_value + taboo_value:
        return 'taboo'
    else:
        return None


class Attributed(Modifiable):

    def init_attributed(self):
        self.init_modifiable()
        self.attributes = {
            'physique': 3,
            'mind': 3,
            'spirit': 3,
            'agility': 3,
        }

    def _get_modified_attribute(self, attr):
        value = self.attributes[attr]
        value += self.modifiers.count_modifiers(attr)
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

    def vitality_info(self):
        d = {'physique': self.physique, 'shape': self.modifiers.count_modifiers('shape'), 'fitness': self.modifiers.count_modifiers('fitness'),
             'mood': self.mood, 'therapy': self.modifiers.count_modifiers('therapy')}
        list_ = self.modifiers.get_modifier_separate('vitality')
        list_ = [(value.name, value.value) for value in list_]
        return d, list_
    @property
    def vitality(self):
        list_ = [self.physique, self.modifiers.count_modifiers('shape'), self.modifiers.count_modifiers('fitness'), self.mood,
                 self.modifiers.count_modifiers('therapy')]
        vitality_mods = self.modifiers.get_modifier_separate('vitality')
        list_.extend([modifier.value for modifier in vitality_mods])
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
        if val > 5:
            val = 5
        return val


"""class Wealth(object):


    def init_wealth(self):
        self.wealth = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.income = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.expense = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    def calc_expense(self):
        expense = copy(self.expense)
        for i in expense:
            try:
                expense[i+1] += int(expense[i]/2)
            except KeyError:
                break
        for i in reversed(sorted(expense.keys())):
            if expense[i] > 0:
                return i
        return 0

    def make_income(self):
        for key, value in self.income.items():
            self.add_wealth(key, value)

    def calc_budget(self):
        pass



    def add_wealth(self, quality, value):
        total = self.wealth[quality] + value
        self.wealth[quality] = total%2
        self.add_wealth(quality+1, int(total/2))

    def has_wealth(self, quality, value):
        return self.wealth[quality] >= value

    def spend_wealth(self, quality, value):
        self.wealth[quality] -= value"""



def get_random_combatant():
    return choice(store.combatant_data.keys())

def get_random_item_set():
    return choice(store.equip_sets.keys())

class Combatant(Skilled, InventoryWielder, Attributed):
    def __init__(self, combatant_id='any', equip_set_id='any'):
        super(Combatant, self).__init__()
        self.init_inventorywielder()
        self.init_skilled()
        self.init_attributed()
        if combatant_id == 'any':
            combatant_id = get_random_combatant()
        if equip_set_id == 'any':
            equip_set_id = get_random_item_set()
        try:
            data = store.combatant_data[combatant_id]
        except KeyError:
            raise Exception("No combatant with id: %s"%combatant_id)
        self.name = data['name']
        self.set_avatar(data['avatar_folder'])
        for key, value in data['attributes'].items():
            setattr(self, key, value)
        self._equip(equip_set_id)
    
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

    def _equip(self, id_):
        try:
            data = store.equip_sets[id_]
        except KeyError:
            raise Exception("No item set with id: %s"%(id_))
        for key, value in data.items():
            if key == 'main_hand' or key == 'other_hand':
                item = create_weapon(**value)
            elif key == 'armor':
                item = create_armor(**value)
        setattr(self, key, item)


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


    def ration_status(self):
        ration = self.owner.schedule.find_by_slot('feed')
        if ration is not None:
            try:
                amount = ration.special_values['amount']
                quality = ration.special_values['quality']
            except KeyError:
                amount = self.amount
                quality = self.quality
        else:
            amount = self.amount
            quality = self.quality
        if quality < self.quality and self.quality_changed:
            quality = self.quality
        amount = max(self.amount, amount)

        colorize_amount = amount
        amount = store.food_amount_dict[amount]
        colorize_quality = quality
        quality = store.food_quality_dict[quality]
        text = '%s'%(utilities.encolor_text(quality, colorize_quality))
        if colorize_amount != 2:
            amount = utilities.encolor_text(amount, colorize_amount)
            text += '(%s)'%(amount)
        if colorize_amount < 1:
            return utilities.encolor_text(amount, 0)
        else:
            return text
        
        

    def set_food(self, amount, quality):
        self.amount = max(self.amount, amount)
        if self.quality_changed:
            self.quality = min(self.quality, quality)
        else:
            self.quality = quality
        self.quality_changed = True

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
    game_ref = None
    @utilities.Observable
    def __init__(self, age=None, gender=None, genus='human'):
        super(Person, self).__init__()

        self.player_controlled = False
        self.init_inventorywielder()
        self.init_skilled()
        self.init_attributed()
        self._event_type = 'person'
        self._firstname = u"Anonimous"
        self.surname = u""
        self.nickname = u""
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
        self.overseer = None
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
        self.life_quality = 0
        self.life_level = 0
        self._stimul = 0
        self.discipline = 0

        self.university = {'name': 'study', 'effort': 'bad', 'auto': False}
        self.fatigue = 0
        self.appetite = 0
        self.calorie_storage = 0
        self.money = 0
        self._determination = 0
        self._anxiety = 0
        self.rewards = []
        self.used_rewards = []
        self.merit = 0  # player only var for storing work result
        self.sex_standart = 0

        # Other persons known and relations with them, value[1] = [needed
        # points, current points]
        self._relations = []
        self._selfesteem = None
        self.conditions = []
        if isinstance(genus, Genus):
            self.genus = genus
        else:
            self.genus = Genus(genus)
        self.genus.invoke(self)
        self.add_feature(age)
        self.add_feature(gender)
        self.set_avatar()
        self._buffs = []
        persons_list.append(self)
        self._main_hand = None
        self._other_hand = None
        self.resources_storage = None
        self.deck = None
        self._calculatable = False
        self.factions = []
        self.background = None
        self.food_system = FoodSystem(self)
        self._known_factions = []
        self._favor = BarterSystem()
        self.card_storage = None
        self.decks = []
        self.selfesteem_buffer = []

        self._taboos = []
        self._fetishes = []
        self.revealed_taboos = []
        self.revealed_fetishes = []

        self.renpy_character = store.Character(self.firstname)

        self._job = dict()
        self.job_buffer = []
        self.job_skill = None
        self.use_job_productivity = False
        self._job_productivity = 0
        self.productivity_raised = False

        self._accomodation = dict()
        self._overtime = dict()

        self.services = collections.defaultdict(dict)
        self.token = 'power'
        self.joy = 0
        self._spoil_number = 1
        self.success = 0
        self.purporse = 0

        self._energy = 0
        self.set_energy()
        self._current_job = None

    @property
    def energy(self):
        return self._energy

    @property
    def spoil_number(self):
        return self._spoil_number

    def spoil(self, need):
        self._spoil_number += 1
        if self._spoil_number > 10:
            self._spoil_number = 1
        for i in self._needs:
            if self._spoil_number in i.spoils:
                i.spoils.remove_spoil(self._spoil_number)
        need.add_spoil(self._spoil_number)

    def calc_life_level(self):
        if self.life_quality < -5+self.sensitivity:
            self.life_level = -1
        elif self.life_quality > 5-self.sensitivity:
            self.life_level = 1
        else:
            self.life_level = 0
        self.life_quality = 0

    @property
    def stimul(self):
        return self._stimul

    @stimul.setter
    def stimul(self, value):
        if self._stimul < 0:
            return
        else:
            self._stimul = value

    def armor_heavier_than(self, person):
        return self.count_modifiers('armor_weight') > person.count_modifiers('armor_weight')

    def check_your_privilege(self, victim):
        privilege = self.menace() - victim.menace()
        if privilege > 2:
            return True

        return False

    def owned_faction(self):
        for i in self.factions:
            if faction.owner == self:
                return i
        return None
    
    def count_modifiers(self, attribute):
        value = super(Person, self).count_modifiers(attribute)
        value += self.inventory.count_modifiers(attribute)
        return value

    def ration_status(self):
        return self.food_system.ration_status()

    def get_combat_style(self):
        #TODO: add beast combat style
        skill_level = self.skill('combat').level
        style = 'noncombatant'
        weapons = self.weapons()
        if len(weapons) > 0:
            if skill_level > 2:
                if any([i.type == 'twohand' for i in weapons]):
                    style = 'juggernaut'
                elif self.has_shield():
                    style = 'shieldbearer'
                else:
                    style = 'breter'
            elif skill_level > 1:
                style = 'rookie'
            else:
                style = 'desperado'
        else:
            if skill_level > 1:
                style = 'wrestler'
        return style

    @property
    def selfesteem(self):
        return self._selfesteem

    @selfesteem.setter
    def selfesteem(self, value):
        self._selfesteem = value


    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, name):
        self._firstname = name
        self.renpy_character.name = name
    
    def __call__(self, what, interact=True):
        self.game_ref.sayer = self
        self.renpy_character(what, interact=interact)

    def predict(self, what):
        self.renpy_character.predict(what)


    def apply_background(self, background):
        self.background = background
        background.apply(self)

    def add_faction(self, faction):
        if not faction in self.factions:
            self.factions.append(faction)

    def has_faction(self):
        return any(self.factions)

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
        mastered_by_player = False
        master_of_player = False
        supervisor_of_player = False
        try:
            mastered_by_player = self.master.player_controlled
        except AttributeError:
            pass
        master_of_player = any([i for i in self.slaves if i.player_controlled])

        return (self._calculatable or self.player_controlled or
            mastered_by_player or master_of_player)


    @calculatable.setter
    def calculatable(self, value):
        self._calculatable = value

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

    def anatomy(self):
        list_ = []
        for i in self.features:
            if i.anatomy:
                list_.append(i)
        return list_

    def has_anatomy_feat(self, name):
        if self.has_feature('polymorphous'):
            return True
        return any([i.id == name for i in self.anatomy()])

    def fetishes(self):
        list_ = [i for i in self._fetishes]
        list_.extend(self.revealed('fetishes'))
        return list_

    def add_taboo(self, taboo):
        self._taboos.append(taboo)

    def add_fetish(self, fetish):
        self._fetishes.append(fetish)

    def taboos(self):
        list_ = [i for i in self._taboos]
        list_.extend(self.revealed('taboos'))
        return list_

    def revealed(self, key):
        return getattr(self, 'revealed_'+key)

    def reveal(self, type_, name):
        list_ = getattr(self, '_'+type_)
        if name in list_:
            list_.remove(name)
        getattr(self, 'revealed_%s'%type_).append(name)

    def reveal_all_taboos(self):
        reveal = []
        for i in self._taboos:
            reveal.append(i)
        for i in reveal:
            self.reveal('taboos', i)

    def reveal_all_fetishes(self):
        reveal = []
        for i in self._fetishes:
            reveal.append(i)
        for i in reveal:
            self.reveal('fetishes', i)


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

    def random_features(self):
        # constitution
        const = choice(('athletic', 'brawny',  'large',
                        'small', 'lean', 'crooked', 'clumsy'))
        roll = randint(1, 100)
        if roll > 40:
            self.add_feature(const)

        # soul
        soul = choice(('brave', 'shy', 'smart', 'dumb', None))
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
        self.genus.remove()
        self.genus = Genus(genus)
        self.genus.invoke(self)

    @property
    def known_characters(self):
        list_ = []
        for r in self._relations:
            persons = [p for p in r.persons if p != self]
            list_ += persons
        return list_

    

    def get_buff_storage(self):
        return self._buffs

    def add_buff(self, id_, time=1):
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
        for buff in [i for i in self._buffs]:
            buff.tick_time()

    def get_buffs(self):
        return [i for i in self._buffs]


    @property
    def job(self):
        try:
            values = self._job.values()
            if len(values) > 0:
                name = self._job.values()[0]['name']
            else:
                name = 'idle'
        except KeyError:
            name = 'idle'
        return name

    def job_description(self):
        try:
            values = self._job.values()
            if len(values) > 0:
                description = self._job.values()[0]['description']
            else:
                description = 'No description'
        except KeyError:
            description = 'No description'
        return description

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

    def __getattribute__(self, key):
        if not key.startswith('__') and not key.endswith('__'):
            try:
                genus = super(Person, self).__getattribute__('genus')
                value = getattr(genus, 'overload_'+key)
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
        return store.mood_translation[self.mood]

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

    # needs should be a list of tuples[(need, shift)]
    def motivation(self):
        golds = []
        greens = []
        cian = []
        reds = []
        value = 0
        
        if self.life_level == 1:
            greens.append(1)
        elif self.life_level == 0:
            cian.append(1)
        else:
            reds.append(1)

        if self.stimul == 1:
            greens.append(1)
        elif self.stimul == 0:
            cian.append(1)
        else:
            reds.append(1)

        if self.selfesteem == 1:
            greens.append(1)
        elif self.selfesteem == 0:
            cian.append(1)
        elif self.selfesteem == -1:
            reds.append(1)

        if self.master is not None:
            if self.discipline == 4:
                golds.append(1)
            elif self.discipline == 3:
                greens.append(1)
            elif self.discipline == 1:
                cian.append(1)
            else:
                reds.append(1)
        else:
            greens.append(1)

        if self.overseer_stance() is not None:
            if self.overseer_stance().value == 2:
                golds.append(1)
            elif self.overseer_stance().value == 1:
                greens.append(1)
            elif self.overseer_stance().value == -1:
                reds.append(1)

        if len(cian) < 0 and len(reds) < 0:
            if len(golds) > 0 and len(greens) > 0:
                return 5
        else:
            for i in golds:
                value += 1
            for i in greens:
                value += 1
            for i in reds:
                value -= 1
        value += self.count_modifiers('motivation')
        return max(-1, min(5, value))

    @property
    def mood(self):
        golds = []
        greens = []
        cian = []
        reds = []
        value = 0
        
        if self.life_level == 1:
            greens.append(1)
        elif self.life_level == 0:
            cian.append(1)
        else:
            reds.append(1)

        if self.selfesteem == 1:
            greens.append(1)
        elif self.selfesteem == 0:
            cian.append(1)
        elif self.selfesteem == -1:
            reds.append(1)

        if self.joy == 1:
            greens.append(1)

        if self.success == 1:
            greens.append(1)

        if self.purporse == 1:
            greens.append(1)

        if len(cian) < 0 and len(reds) < 0:
            if len(golds) > 0 and len(greens) > 0:
                return 5
        else:
            for i in golds:
                value += 1
            for i in greens:
                value += 1
            for i in reds:
                value -= 1
        value += self.count_modifiers('mood')
        return max(-1, min(5, value))



    # adds features to person, if mutually exclusive removes old feature
    def add_feature(self, id_, time=None):
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

    def visible_features(self,):
        return [i for i in self.features if i.id != self.age and i.id != self.gender]

    def full_name(self):
        return self.firstname + ' "' + self.nickname + '" ' + self.surname

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

    def overseer_relations(self):
        if self.overseer is not None:
            return self.relations(self.overseer)

    def overseer_stance(self):
        if self.overseer is not None:
            return self.stance(self.overseer)



    def rest(self):
        self._favor.tick_time()
        self.favor_income()
        if not self.calculatable:
            return
        self.calc_life_level()

        if self.player_controlled:
            if self.mood < 0:
                self.anxiety += 1
        
        else:
            if self.motivation() < 0:
                self.anxiety += 1

        if self.energy < 0:
            self.add_buff('exhausted')
        
        self.reduce_esteem()
        self.food_system.fatness_change()
        self.remove_money(self.decade_bill)
        self.calc_focus()
        self.set_energy()
        self.reset_needs()
        
        self.ap = 1
        self._stimul = 0
        self.success = 0
        self.purporse = 0
        self.joy = 0
        self.productivity_raised = False

    def tick_time(self):
        if not self.calculatable:
            return
        self.conditions = []
        self.tick_buffs_time()
        self.tick_features()
    def tick_schedule(self):
        if not self.calculatable:
            return
        self.use_job()
        self.use_services()
        self.use_accomodation()
        
        self.use_overtime()

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

    def forget_person(self, person):
        to_remove = []
        for i in self._relations:
            if person in i.persons:
                to_remove.append(i)
        for i in to_remove:
            self._relations.remove(i)
            person._relations.remove(i)
        
        for i in self._stance:
            if person in i.persons:
                to_remove.append(i)
        for i in to_remove:
            if i in self._stance:
                self._stance.remove(i)
            if i in person._stance:
                person._stance.remove(i)
        
        for i in to_remove:
            i.persons = []

    def know_faction(self, faction):
        if faction in self.known_factions():
            return True
        return False

    def known_factions(self, type=None):
        if type is None:
            return self._known_factions
        else:
            return [i for i in self._known_factions if i.type == type]

    def _set_relations(self, person):
        relations = Relations(self, person)
        person._relations.append(relations)
        self._relations.append(relations)
        return relations

    def aknowledge_faction(self, faction):
        if not self.know_faction(faction):
            self._known_factions.append(faction)

    def relations(self, person):
        if person == self:
            raise Exception("relations: target and caller is same person")
        if isinstance(person, Faction):
            self.aknowledge_faction(person)
            return self.relations(person.owner)
        elif isinstance(person, Person):
            for i in person.factions:
                self.aknowledge_faction(i)
        else:
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
            self.aknowledge_faction(person)
            return self.stance(person.owner)
        elif isinstance(person, Person):
            for i in person.factions:
                self.aknowledge_faction(i)
        else:
            raise Exception("relations called with not valid arg: %s" % person)
        
        if not self.know_person(person):
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

    def use_token(self):
        self.tokens.remove(token)
        self.player_relations().stability += 1
        self.relations_tendency[token] += 1
        self.token = 'power'

    def set_token(self, token, free=False):
        sekf.token = token      
        renpy.call_in_new_context('lbl_notify', self, token)

    def get_token_image(self):
        return {'power': 'images/tarot/arcana_lust.jpg',
            'conquest': 'images/tarot/arcana_charriot.jpg',
            'convention': 'images/tarot/arcana_justice.jpg',
            'contribution': 'images/tarot/arcana_lovers.jpg'}[self.token]

    def player_relations(self):
        return self.relations(self.game_ref.player)

    def player_stance(self):
        return self.stance(self.game_ref.player)

    def moral_action(self, *args, **kwargs):
        # checks moral like person.check_moral, but instantly affect selfesteem
        for arg in args:
            if isinstance(arg, int):
                self.selfesteem += arg
                return
        result = self.check_moral(*args, **kwargs)
        self.selfesteem_buffer.append(result)
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
        action_tones['activity'] = act.get(activity)
        action_tones['morality'] = moral.get(morality)
        action_tones['orderliness'] = order.get(orderliness)
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
        if len(self.selfesteem_buffer) < 1:
            self._selfesteem = None
            return
        if all([i >= 0 for i in self.selfesteem_buffer]):
            self._selfesteem = 1
            
        else:
            value = 0
            for i in self.selfesteem_buffer:
                value += i
                if value > 0:
                    self._selfesteem = 0
                else:
                    self._selfesteem = -1
        self.selfesteem_buffer = []

            

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

    #favor methods
    def gain_favor(self, value):
        if self.player_controlled:
            return
        value = self.favor + value
        if value < 0:
            self.favor = 0
            return
        hard_max = 5
        soft_max = 3+self.player_stance().value
        favor = min(hard_max, min(soft_max, value))
        self._favor.income(favor)

    @property
    def favor(self):
        return self._favor.value

    def spend_favor(self, value):
        self._favor.spend(-value)

    def add_favor_consumption(self, name, value, slot, time=1, description=""):
        self._favor.add_consumption(self, name, value, slot, time, description)

    def remove_favor_consumption(self, slot):
        self._favor.remove_consumption(self, slot)

    def get_favor_consumption(self):
        return self._favor.consumption_level()

    def calculate_favor(self, value):
        return self._favor.calculate_consumption(value)

    def favor_income(self):
        if self.player_controlled:
            return
        relations = self.player_relations()
        value = 0
        stance = self.player_stance().value
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
    # end of favor methods
    
    def can_tick(self):
        return self._favor.can_tick() and self.has_money(self.decade_bill)

    @property
    def decade_bill(self):
        return sum([i['cost'] for i in self.get_services()])

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

    def die(self, destroy=False):
        self.remove_relations()
        if destroy:
            self.destroy()
        if self.player_controlled:
            renpy.call('lbl_gameover')
        self.add_feature('dead')
    
    def destroy(self):
        self.remove_relations()
        self._remove_features()
        self._remove_needs()
        self._remove_foodsystem()
        self.remove_genus()
        self.remove_skills()
        self.remove_schedule()
        persons_list.remove(self)

    def remove_genus(self):
        self.genus.remove()

    def remove_schedule(self):
        self.schedule.actions = []
        self.schedule.owner = None
        self.schedule = None

    def _remove_needs(self):
        for i in self._needs:
            i.owner = None
        self._needs = []       

    def _remove_foodsystem(self):
        self.food_system.owner = None

    def _remove_features(self):
        to_remove = []
        for i in self.features:
            to_remove.append(i)
        for i in to_remove:
            i.remove()

    def remove_skills(self):
        for i in self.skills:
            i.owner = None
        self.skills = []


    def remove_relations(self):
        characters = [i for i in self.known_characters]
        for i in characters:
            self.forget_person(i)
        

    def is_dead(self):
        if self.feature('dead') is not None:
            return True
        return False

    #rating methods
    def allure(self):
        value = 0
        value += self.count_modifiers('alure')
        if self.skill('spirit') > value:
            value += 1
        if self.vitality > value:
            value += 1
        
        return max(0, min(value, 5))

    def hardiness(self):
        value = self.physique
        value += self.count_modifiers('hardiness')
        if self.skill('physique') > value:
            value += 1
        if self.vitality > value:
            value += 1
        elif self.vitality < value:
            value -= 1
        
        return max(0, min(value, 5))

    def succulence(self):
        value = 3 + self.count_modifiers('succulence')
        if self.vitality > value:
            value += 1
        elif self.vitality < value:
            value -= 1

        return max(0, min(value, 5))

    def exotic(self):
        value = self.count_modifiers('exotic')
        return max(0, min(value, 5))

    def style(self):
        value = self.agility
        value += self.count_modifiers('style')
        if self.skill('agility') > value:
            value += 1
        return max(0, min(value, 5))

    def purity(self):
        value = self.count_modifiers('purity')
        return max(0, min(value, 5))

    def menace(self):
        value = self.physique
        value += self.skill('physique')-3
        weapons = self.weapon_slots()
        if (weapons['harness'] is None and
            weapons['belt1'] is None and
            weapons['belt2'] is None):
                value -= 1
        for i in weapons.values():
            if i is not None:
                if i.size == 'twohand':
                    value += 1
                    break
        if self.armor is None:
            value -= 1
        elif self.armor.armor_rate == 'heavy_armor':
            value += 1
        value += self.count_modifiers('menace')
        return max(0, min(value, 5))

    def job_productivity(self):
        if self.job_skill is not None:
            value = self.skill(self.job_skill) - self.job_difficulty
        else:
            return 0
        if value < 0:
            value = 0
        value += self._job_productivity
        
        if not self.player_controlled:
            return min(value, self.motivation())
        return value

    def focus(self):
        return abs(self.skill(self.job_skill) - self.job_difficulty)+self._job_productivity

    def increase_productivity(self):
        self.job_buffer = []
        self._job_productivity += 1
        self.productivity_raised = True

    def use_job(self):
        if self.use_job_productivity:
            if self.player_controlled:
                renpy.call_in_new_context('lbl_jobcheck', person=self, attribute=self.job_skill)
            else:
                renpy.call_in_new_context('lbl_jobcheck_npc', person=self, attribute=self.job_skill)
        try:
            event = self._job['event']
        except KeyError:
            pass
        else:
            if event is not None:
                call_event(event, self)
        self.job_buffer = []
        self.productivity_raised = False

    def world(self):
        return self.game_ref.current_world

    def set_job(self, job, skill=None, single=False, target=None, difficulty=1):

        data = self.available_jobs()[job]
        world = self.world().name
        if self._job_productivity > 0:
            old_job = self._job.items()
            old_job_dict = {}
            for key, value in old_job:
                old_job_dict[key] = value
            self.job_buffer = [old_job_dict, self._job_productivity, self.productivity_raised]
            self._job_productivity = 0

        if target is not None:
            special_values = {'target': target}
        else:
            special_values = None
    
        self._job = {}
        self._job[world] = {'id': job}
        for key, value in data.items():
            self._job[world][key] = value
        
        if len(self.job_buffer) > 0:
            for key, value in self.job_buffer[0].items():
                if job == value['id'] and world == key:
                    self._job_productivity = self.job_buffer[1]
                    self.productivity_raised = self.job_buffer[2]
                    self.job_buffer = []
        try:
            skill = data['skill']
        except KeyError:
            skill = None
        try:
            difficulty = data['difficulty']
        except KeyError:
            difficulty = 0
        if skill is None:
            self.use_job_productivity = False
        else:
            self.use_job_productivity = True
        self.job_skill = skill
        self.job_difficulty = difficulty

    def set_accomodation(self, name):
        self._accomodation = collections.defaultdict(dict)
        data = self.available_accomodations()[name]
        world = self.world().name
        self._accomodation[world] = {'id': name}
        for key, value in data.items():
            self._accomodation[world][key] = value


    def use_accomodation(self):
        accomodation = self._accomodation[self.world().name]
        print accomodation
        try:
            event = accomodation['event']
        except KeyError:
            return
        else:
            if event is not None:
                call_event(event, self)

    def set_overtime(self, name):
        self._overtime = collections.defaultdict(dict)
        data = self.available_overtimes()[name]
        world = self.world().name
        self._overtime[world] = {'id': name}
        for key, value in data.items():
            self._overtime[world][key] = value

    @property
    def overtime(self):
        return self._overtime[self.world().name]['name']

    def overtime_description(self):
        return self._overtime[self.world().name]['description']

    def use_overtime(self):
        overtime = self._overtime[self.world().name]
        try:
            event = overtime['event']
        except KeyError:
            pass
        else:
            if event is not None:
                call_event(event, self)


    @property
    def accomodation(self):
        return self._accomodation[self.world().name]['name']

    def accomodation_description(self):
        return self._accomodation[self.world().name]['description']

    def available_jobs(self):
        return self.game_ref.jobs()

    def available_services(self):
        return self.game_ref.services()

    def available_accomodations(self):
        return self.game_ref.accomodations()

    def available_overtimes(self):
        return self.game_ref.overtimes()

    def add_service(self, name):
        data = self.available_services()[name]
        self.services[self.world().name][name] = data


    def has_service(self, name):
        try:
            services = self.services[self.world().name]
        except KeyError:
            return False
        else:
            return name in services.keys()

    def remove_service(self, name):
        services = self.services[self.world().name]
        try:
            del services[name]
        except KeyError:
            pass

    def get_services(self):
        try:
            services = self.services[self.world().name]
        except KeyError:
            return {}
        else:
            return services.values()

    def use_services(self):
        for i in self.get_services():
            try:
                event = i['event']
            except KeyError:
                pass
            else:
                if event is not None:
                    call_event(event, self)
        

    def joy(self, need, value):
        need = getattr(self, need)
        value -= need.spoil_level()
        if value > 0:
            self.joy = 1
        self.spoil(need)

    def set_energy(self):
        value = 0
        value += self.count_modifiers('energy')
        self._energy = max(0, min(5, value))

    def drain_energy(self, value=1):
        self._energy -= value
        if self._energy < -1:
            self._energy = -1

    def gain_energy(self, value=1):
        self._energy += value
        if self._energy > 5:
            self._energy = 5

    def has_energy(self):
        return self._energy > -1