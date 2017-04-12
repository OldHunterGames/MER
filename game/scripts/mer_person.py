# -*- coding: UTF-8 -*-
from random import *
import collections

import renpy.store as store
import renpy.exports as renpy

from features import Feature, Phobia
from skills import Skilled
from anatomy import Anatomy
from psymodel import PsyModel
from schedule import Schedule
from relations import Relations
from genus import available_genuses, Genus

from modifiers import ModifiersStorage, Modifiable
from factions import Faction
from buffs import Buff
from background import Background
from inventory import Inventory, InventoryWielder
from mer_resources import BarterSystem
import mer_utilities as utilities
from mer_command import *


def get_avatars(path):
    all_ = renpy.list_files()
    avas = [str_ for str_ in all_ if str_.startswith(path)]
    return avas


def gen_random_person(genus=None, age=None, gender=None, world=None,
                      culture=None, family=None, education=None,
                      occupation=None, initial_tonus=0, initial_fatness=0):
    if genus is not None:
        if genus not in available_genuses():
            raise Exception(
                "gen_person with genus '%s' which not exists" % (genus))
    else:
        genus = choice(available_genuses())
    genus = Genus(genus)
    if gender is None:
        gender = genus.get_gender()
    if age is None:
        age = genus.get_age()
    p = Person(age, gender, genus, initial_fatness, initial_tonus)
    background = Background(age, world, culture, family, education, occupation)
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
    gen_body_parts(p)
    gen_features(p)
    return p


def gen_body_parts(person):
    gender = person.gender
    genus = person.genus.name
    if gender == 'male' or gender == 'sexless':
        sizes = {
            'micro_penis': 1,
            'small_penis': 1,
            'normal_penis': 2,
            'large_penis': 3,
            'huge_penis': 3
        }
        part = person.add_body_part('penis')
        if genus == 'lupine' or genus == 'werewolf':
            size = utilities.weighted_random(
                sizes)
        else:
            size = choice(sizes.keys())

        part.add_feature(genus + '_penis')
        part.add_feature(size)

    else:
        sizes = {
            'micro_vagina': 1,
            'small_vagina': 1,
            'normal_vagina': 1,
            'large_vagina': 1,
            'huge_vagina': 1
        }
        part = person.add_body_part('vagina')
        size = utilities.weighted_random(sizes)
        part.add_feature(size)
        part.add_feature(choice(['wet_vagina', 'dry_vagina']))

        sizes = {'junior':
                 {
                     'micro_boobs': 10,
                     'small_boobs': 10,
                     'normal_boobs': 0,
                     'large_boobs': 0,
                     'huge_boobs': 0
                 },
                 'others':
                 {
                     'micro_boobs': 1,
                     'small_boobs': 1,
                     'normal_boobs': 1,
                     'large_boobs': 1,
                     'huge_boobs': 1
                 }

                 }
        part = person.add_body_part('boobs')
        try:
            size = utilities.weighted_random(sizes[gender])
        except KeyError:
            size = utilities.weighted_random(sizes['others'])
        part.add_feature(size)
    part = person.add_body_part('ass')
    part.add_feature(choice(get_body_part_features('ass_size')))
    person.add_body_part('body')
    person.add_body_part('mouth')
    part = person.add_body_part('manipulator')
    part.add_feature('human_hand')
    part = person.add_body_part('foot')
    part.add_feature('human_foot')


def get_body_part_features(slot):
    data = store.anatomy_features
    return [key for key, value in data.items() if value['slot'] == slot]


def get_features_by_slot(slot, dict):
    return [key for key, value in dict.items() if value.get('slot') == slot]


def gen_features(person):
    for i in ['voice', 'skin', 'hair', 'look', 'constitution']:
        features = get_features_by_slot(i, store.person_features)
        person.add_feature(choice(features))


persons_list = []


def gen_sex_traits(person):
    # TODO: sex traits generation rules instead of random
    person.sexual_suite = choice(store.sexual_type.values())
    person.sexual_orientation = choice(store.sexual_orientation.values())


class SlaveStorage(object):

    def __init__(self):
        self._max_slaves = 1
        self._slaves = []

    def slaves(self):
        return [i for i in self._slaves]

    def add_slave(self, slave, master):
        if self.has_space():
            self._slaves.append(slave)
            self._slave_relations(slave, master)
            return True
        else:
            self._slaves.pop()
            self._slaves.append(slave)
            return True
        return False

    def remove_slave(self, slave):
        self._slaves.remove(slave)
        slave.set_master(None)

    def set_max_slaves(self, value):
        self._max_slaves = value

    def has_space(self):
        return len(self._slaves) < self._max_slaves

    def _slave_relations(self, slave, master):
        # master.relations(slave).change_type('slave')
        slave.set_master(master)


class DescriptionMaker(object):
    """Class for complex person description generation"""
    # TODO: Refactor this as abstract and allocate realizations by game lang?

    def __init__(self, person):
        self.person = person

    def description(self):
        person = self.person
        background = self.person.background
        weapon_txt = self.make_weapon_text()
        alignment_desc = [str.capitalize(i)
                          for i in person.alignment.description()]
        get_feature = person.feature_by_slot
        profession = person.feature_by_slot('profession')
        possesive = self.get_possesive()
        pronoun = self.get_pronoun1()
        pronoun2 = self.get_pronoun2()
        slots = ['hair', 'voice', 'constitution', 'shape',
                 'look', 'skin', 'profession', 'gender', 'age']

        string = '{person.firstname} "{person.nickname}" is a {person.age} {person.genus.name} {person.gender}, '

        if not self.person.player_controlled:
            string += self.relations_text()

        string += '{cap_pronoun} behaves as a {alignment[0]}, {alignment[1]} and '\
            '{alignment[2]} person and {possesive} sexuality is a {sex_suite} {sex_orientation}. '
        string += '{{person.firstname}} originated from {background.world.name}, {background.world.description}. '\
            '{{person.firstname}} {background.family.description}, ' \
            '{background.education.description}'.format(
                background=person.background)
        if profession is not None:
            string += 'and became a {profession} eventually. \n'.format(
                profession=profession.name)
        else:
            string += '.\n'
        if person.obligation:
            text = store.obligations_dict.get(
                    person.player_relations().attitude_tendency(),
                    'obligation description here').format(
                        person=person)
            string += utilities.encolor_text(text, 'green', protected=True)
        string += '{person.firstname} has a {constitution} and {shape} figure. '\
            '{cap_possesive} appearance is {look}. '\
            '{cap_possesive} voice is {voice}. '\
            '{person.name} has a {hair} and {skin}. '
        string += '\n'
        start = True
        for i in person.features:
            if i.slot not in slots:
                if not start:
                    string += ' '
                else:
                    start = False
                string += i.description
        string = string.format(
            person=person, pronoun=pronoun,
            alignment=alignment_desc, possesive=possesive,
            cap_possesive=str.capitalize(possesive),
            cap_pronoun=str.capitalize(pronoun),
            hair=get_feature('hair').name, voice=get_feature('voice').name,
            constitution=get_feature('constitution').name,
            shape=get_feature('shape').name,
            look=get_feature('look').name,
            skin=get_feature('skin').description,
            sex_suite=person.sexual_suite['name'],
            sex_orientation=person.sexual_orientation['name'],
            pronoun2=pronoun2, cap_pronoun2=str.capitalize(self.get_pronoun2())
        )
        return string

    def get_pronoun1(self):
        if self.person.gender == 'male' or self.person.gender == 'sexless':
            return 'he'
        else:
            return 'she'

    def get_pronoun2(self):
        if self.person.gender == 'male' or self.person.gender == 'sexless':
            return 'him'
        else:
            return 'her'

    def get_possesive(self):
        return {'he': 'his', 'she': 'her'}[self.get_pronoun1()]

    def make_weapon_text(self):
        weapons = self.person.weapons()
        if len(weapons) > 1:
            weapon_txt = '{person.name} armed with {person.main_hand.name} and {person.other_hand.name}'.format(
                person=self.person)
        elif len(weapons) == 1:
            weapon_txt = '{person.name} armed with {weapons[0].name}'.format(
                weapons=weapons, person=self.person)
        else:
            weapon_txt = ''
        if self.person.armor is not None:
            weapon_txt += '. {cap_pronoun} wears a {person.armor.name}'
        return weapon_txt

    def relations_text(self, colorize=True, protected=True):
        if not self.person.know_player():
            return ''
        relations = self.person.player_relations()
        stance_type = relations.colored_stance(protected)

        return '{stance_type} ({relations[0]}, {relations[1]}, {relations[2]}) towards you. '.format(
            stance_type=stance_type, relations=relations.description(colorize, protected))


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

    def vitality_info(self):
        d = {'physique': self.physique, 'shape': self.count_modifiers('shape'),
             'fitness': self.count_modifiers('fitness'),
             'therapy': self.count_modifiers('therapy')}
        list_ = self.modifiers_separate('vitality')
        list_ = [(value.name, value.value) for value in list_]
        return d, list_

    @property
    def vitality(self):
        list_ = [self.physique, self.count_modifiers('shape'),
                 self.count_modifiers('fitness'),
                 self.count_modifiers('therapy')]
        vitality_mods = self.modifiers_separate('vitality')
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
            raise Exception("No combatant with id: %s" % combatant_id)
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
    """
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
    """


class FoodSystem(object):

    _features = {
        2: 'obese',
        1: {0: 'chubby', 1: 'beefy', -1: 'flabby'},
        0: {0: 'undistinguished', 1: 'muscular', -1: 'skinyfar'},
        -1: {0: 'slim', 1: 'wiry', -1: 'frail'},
        -2: 'emaciated'
    }

    def __init__(self, owner, fatness=0, tonus=0):
        self.owner = owner
        self.satiety = 0
        self._fatness = fatness
        self._fitness = 0
        self._tonus = tonus
        self.quality = 0
        self.quality_changed = False
        self.amount = 0
        self._set_shape()

    @property
    def fitness(self):
        if abs(self._fatness) == 2:
            return 0
        if self._tonus > 7 - self.owner.physique:
            return 1
        elif self._tonus < -2 - self.owner.physique:
            return -1
        else:
            return 0

    @property
    def tonus(self):
        return self._tonus

    @tonus.setter
    def tonus(self, value):
        self._tonus = max(-10, min(10, value))
        self._set_shape()

    @property
    def fatness(self):
        return self._fatness

    def increase_fatness(self):
        if self._fatness == 2:
            self._increase_shape()
            return
        self._fatness += 1
        self._set_shape()

    def decrease_fatness(self):
        if self._fatness == -2:
            self._decrease_shape()
            return
        if self.owner.has_feature('dyspnoea'):
            self.owner.remove_feature('dyspnoea')
        else:
            self._fatness -= 1
            self._set_shape()

    def _set_shape(self):
        data = self._features[self._fatness]
        if not isinstance(data, str):
            data = data[self._fitness]
        self.owner.add_feature(data)

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
        text = '%s' % (utilities.encolor_text(quality, colorize_quality))
        if colorize_amount != 2:
            amount = utilities.encolor_text(amount, colorize_amount + 1)
            text += '(%s)' % (amount)
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
        text = '%s' % (utilities.encolor_text(quality, quality_encolor))
        if self.amount != 2:
            amount = utilities.encolor_text(amount, self.amount)
            text += '(%s)' % (amount)
        if self.amount < 1:
            return utilities.encolor_text(amount, 0)
        else:
            return text

    def _increase_shape(self):
        if not self.owner.has_feature('dyspnoea'):
            self.owner.add_feature('dyspnoea')
        else:
            random_num = randint(1, 10)
            satiety = min(self.satiety, self.owner.physique)
            if random_num <= satiety:
                self.owner.add_feature('diabetes')

    def _decrease_shape(self):
        if self.amount < 1:
            self.owner.die()

    def is_good_feed(self):
        return (not self.owner.has_feature('diabetes') or
                not self.owner.has_feature('obese'))

    def is_bad_feed(self):
        return (self.owner.has_feature('slim') or
                self.owner.has_feature('emaciated'))

    def fatness_change(self):
        if self.owner.has_condition('workout'):
            self.satiety -= 1
        if self.amount == 3:
            amount_value = 1
        elif self.amount == 1:
            amount_value = -1
        else:
            amount_value = 0
        if self.amount < 1:
            total = 0
        elif self.quality < 0:
            total = 0
        else:
            total = max(-1, min(5, self.quality + amount_value))
        if total > 0:
            self.owner.satisfy_need('nutrition', total)
        elif total < 0:
            self.owner.tense_need('nutrition', 'hunger')
        if self.amount == 3:
            self.satiety += self.amount - 2
        elif self.amount == 1:
            if self.fatness != -2:
                self.satiety -= 1
        elif self.amount == 0:
            if self.satiety > 0:
                self.satiety = -1
            else:
                self.satiety += self.satiety - 1
        satiety = self.satiety

        if self.satiety > self.owner.physique:
            self.satiety = 0
            self.increase_fatness()

        elif self.satiety < -(6 - self.owner.physique):
            self.satiety = 0
            self.decrease_fatness()

        if satiety > 0 and self.is_good_feed():
            self.owner.add_buff('overfeed')
        elif satiety < 0 or self.is_bad_feed():
            self.owner.add_buff('underfeed')
        self.set_starvation()


class Person(Skilled, InventoryWielder, Attributed, PsyModel):
    game_ref = None

    @utilities.Observable
    def __init__(self, age=None, gender=None, genus='human', fatness=0, tonus=0):
        super(Person, self).__init__()
        self.kink = 'default'
        self.anatomy = Anatomy()

        self.player_controlled = False
        self.init_inventorywielder()
        self.init_skilled()
        self.init_attributed()
        self.init_psymodel()
        self._event_type = 'person'
        self._firstname = u"Anonimous"
        self.surname = u""
        self.nickname = u""

        # gets Feature() objects and their child's. Add new Feature only with
        # self.add_feature()
        self.features = []
        self.tokens = []             # Special resources to activate various events
        self.relations_tendency = {'convention': 0,
                                   'conquest': 0, 'contribution': 0}
        # obedience, dependecy and respect stats
        self.avatar_path = ''

        self._master = None          # If this person is a slave, the master will be set
        self.supervisor = None
        self.overseer = None
        self.slaves = SlaveStorage()
        self.subordinates = []
        self.ap = 1
        self.schedule = Schedule()
        # init starting features

        self.availabe_actions = []  # used if we are playing slave-part

        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.sparks = 0
        self.factors = []
        self.restrictions = []
        self.bad_markers = []
        self.good_markers = []
        self.discipline = 0

        self.university = {'name': 'study', 'effort': 'bad', 'auto': False}
        self.fatigue = 0
        self.appetite = 0
        self.calorie_storage = 0
        self.money = 0
        self._determination = 0
        self._anxiety = 0
        self.rewards = []
        self.merit = 0  # player only var for storing work result
        self.sex_standart = 0

        # Other persons known and relations with them, value[1] = [needed
        # points, current points]
        self._relations = []
        self.conditions = []
        if isinstance(genus, Genus):
            self.genus = genus
        else:
            self.genus = Genus(genus)
        self.genus.apply(self)
        self.add_feature(age)
        self.add_feature(gender)
        self.set_avatar()
        self._buffs = []
        self._main_hand = None
        self._other_hand = None
        self.resources_storage = None
        self.deck = None
        self._calculatable = False
        self.faction = None
        self.background = None
        self.food_system = FoodSystem(self, fatness, tonus)
        self._known_factions = []
        self._favor = BarterSystem()
        self.card_storage = None
        self.decks = []

        self._taboos = []
        self._fetishes = []
        self.revealed_taboos = []
        self.revealed_fetishes = []
        self.communications_done = []

        self._renpy_character = store.Character(self.firstname)

        self.pocket_money = 0
        self._job = None
        self.job_buffer = None
        self.productivity_raised = False
        self.life_buffer = {}
        self._accommodation = None
        self._overtime = None
        self._feed = None

        self.services = collections.defaultdict(dict)

        self.allowed = {
            'job': [],
            'service': [],
            'accommodation': [],
            'overtime': [],
            'feed': []
        }
        self._default_schedule = {'job': 'idle',
                                  'accommodation': 'makeshift',
                                  'overtime': 'rest',
                                  'feed': 'forage'}
        self.token = 'power'
        self._spoil_number = 1
        self.success = 0
        self.purporse = 0

        self._energy = 0
        self.set_energy()
        self._current_job = None
        self.quests_to_give = []
        self._phrases = dict()
        self.obligation = False
        self.rewards = CardsMaker()
        self._interactions = CardsMaker()
        self._active_quest = None

    def get_interactions(self):
        self._interactions.set_context(owner=self)
        return self._interactions.run()

    def add_interaction(self, key, value):
        self._interactions.add_entry(key, value)

    def remove_interaction(self, key):
        self._interactions.remove_entry(key)

    # def add_reward(self, reward):
    #     self.rewards.append(reward)

    # def remove_reward(self, reward):
    #     try:
    #         self.rewards.remove(reward)
    #     except ValueError:
    #         pass

    @property
    def master(self):
        return self._master

    def set_active_quest(self, quest):
        self._active_quest = quest

    @property
    def active_quest(self):
        return self._active_quest

    def quest_completed(self, player):
        if self._active_quest is None:
            return False
        else:
            return self._active_quest.completed(player)

    def get_phrase(self, id_, default_value="No phrase"):
        phrase = self._phrases.get(
            id_, store.basic_dialogues.get(
                id_, default_value))
        return phrase

    def set_nickname(self, string):
        self.nickname = string

    def set_phrases(self, dict_):
        self._phrases = dict_

    def has_available_quests(self, player):
        if self._active_quest is not None:
            return False
        return any(self.available_quests())

    def available_quests(self):
        return [i for i in self.quests_to_give if not i.active]

    def clear_quests(self):
        self.quests_to_give = []

    def get_body_part(self, name):
        return self.anatomy.get_part(name)

    def add_body_part(self, name):
        return self.anatomy.add_part(name)

    def has_body_part(self, name):
        if name is None:
            return True
        return self.get_body_part(name) is not None

    def add_quest(self, quest):
        quest.employer = self
        self.quests_to_give.append(quest)

    def remove_quest(self, quest):
        self.quests_to_give.remove(quest)

    def set_pocket_money(self, level):
        self.pocket_money = level

    @property
    def tonus(self):
        return self.food_system.tonus

    @tonus.setter
    def tonus(self, value):
        self.food_system.tonus = value

    @property
    def energy(self):
        return self._energy

    def emotional_stability(self):
        return 3 + self.count_modifiers('emotional_stability')

    def armor_heavier_than(self, person):
        return self.count_modifiers('armor_weight') > person.count_modifiers('armor_weight')

    def check_your_privilege(self, victim):
        privilege = self.menace() - victim.menace()
        if privilege > 2:
            return True

        return False

    def owned_faction(self):
        if self.faction is not None:
            if self.faction.owner == self:
                return self.faction
        return None

    def count_modifiers(self, attribute):
        value = super(Person, self).count_modifiers(attribute)
        value += self.inventory.count_modifiers(attribute)
        for i in self.features:
            value += i.count_modifiers(attribute)
        return value

    def modifiers_separate(self, attribute):
        list_ = super(Person, self).modifiers_separate(attribute)
        list_.extend(self.inventory.get_modifier_separate(attribute))
        return list_

    def ration_status(self):
        return self.food_system.ration_status()

    def get_combat_style(self):
        # TODO: add beast combat style
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
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, name):
        self._firstname = name
        self._renpy_character.name = name

    def __call__(self, what, interact=True):
        self.game_ref.sayer = self
        self._renpy_character(what, interact=interact)

    def say_phrase(self, phrase_id, default_value='No phrase'):
        phrase = self.get_phrase(phrase_id, default_value)
        self(phrase)

    def predict(self, what):
        self._renpy_character.predict(what)

    def apply_background(self, background):
        self.background = background
        background.apply(self)

    def set_faction(self, faction):
        if self.faction is not None:
            self.faction.remove_member(self)
        self.faction = faction

    def has_faction(self):
        return self.faction is not None

    def remove_faction(self, faction):
        if self.faction is not None:
            self.faction.remove_member(self)
        self.faction = None

    def eat(self, amount, quality):
        self.food_system.set_food(amount, quality)

    def food_info(self):
        return self.food_system.food_info()

    @property
    def calculatable(self):
        return self.player_controlled
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

    def random_features(self):
        # constitution
        const = choice(('athletic', 'brawny', 'large',
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
        self.genus.apply(self)

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

    def job_name(self):
        if self._job.name is None:
            return 'idle'
        else:
            return self._job.name

    def job_description(self):
        return self.job.full_description()

    def __getattribute__(self, key):
        if not key.startswith('__') and not key.endswith('__'):
            try:
                genus = super(Person, self).__getattribute__('genus')
                value = getattr(genus, 'overload_' + key)
                return value
            except AttributeError:
                pass
        return super(Person, self).__getattribute__(key)

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

    # show methods returns strings, to simplify displaying various stats to
    # player
    def show_taboos(self):
        s = ""
        for taboo in self.taboos:
            if taboo.value != 0:
                s += "{taboo.name}({taboo.value}), ".format(taboo=taboo)
        return s

    def show_features(self):
        s = ""
        for feature in self.features:
            if feature.visible:
                s += "{feature.name}, ".format(feature=feature)
        return s

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

    @property
    def name(self):
        s = self.firstname + ' %s'%self.nickname + ' %s'%self.surname
        return s

    def tick_features(self):
        for feature in self.features:
            feature.tick_time()

    # adds features to person, if mutually exclusive removes old feature
    def add_feature(self, id_, time=None):
        if self.has_feature(id_):
            return
        try:
            feature = Feature(id_)
        except KeyError:
            pass
        else:
            if feature.slot is not None:
                self.remove_feature_by_slot(feature.slot)
            self.features.append(feature)

    def add_phobia(self, id_):
        Phobia(self, id_)

    def feature_by_slot(self, slot):  # finds feature which hold needed slot
        for f in self.features:
            if f.slot == slot:
                return f
        return None

    def feature(self, id_):  # finds feature with needed name if exist
        for f in self.features:
            if f.id == id_:
                return f
        return None

    def has_feature(self, id_):
        return self.feature(id_) is not None

    def remove_feature(self, feature):
        if isinstance(feature, str):
            for i in self.features:
                if i.id == feature:
                    self.features.remove(i)
        else:
            try:
                self.features.remove(feature)
            except ValueError:
                return

    def remove_feature_by_slot(self, slot):
        for f in self.features:
            if f.slot == slot:
                self.features.remove(f)
                return

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

    def overseer_relations(self):
        if self.overseer is not None:
            return self.relations(self.overseer)

    def rest(self):
        self._favor.tick_time()
        self.favor_income()

        if not self.calculatable:
            return

        #if self.energy < 0:
        #    self.add_buff('exhausted')
        self.food_system.fatness_change()
        self.remove_money(self.decade_bill())
        self.set_energy()

        if self.pocket_money > 0:
            self.satisfy_need('prosperity', self.pocket_money)

        self.ap = 1
        self._stimul = 0
        self.success = 0
        self.purporse = 0
        self.productivity_raised = False
        for key, value in self.tokens_relations.items():
            skill = self.skill(key)
            if skill > 0:
                self.add_chance(skill, value, attributed=key)

    def tick_time(self):
        if not self.calculatable:
            return
        self.conditions = []
        self.tick_buffs_time()
        self.tick_features()
        self.reset_psych()

    def tick_schedule(self):
        self.bad_markers = []
        self.good_markers = []
        self.decay_corpses()
        if not self.calculatable:
            return
        self.schedule.use(self)

    def know_person(self, person):
        if person in self.known_characters:
            return True
        return False

    def know_player(self):
        if self.player_controlled:
            return False
        for i in self._relations:
            if i.is_player_relations():
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

    def discover_faction(self, faction):
        if not self.know_faction(faction):
            self._known_factions.append(faction)

    def relations(self, person):
        if person == self:
            raise Exception("relations: target and caller is same person")
        if isinstance(person, Faction):
            self.discover_faction(person)
            if self.know_person(person.owner):
                return self.relations(person.owner)
            else:
                return
        elif isinstance(person, Person):
            if person.faction is not None:
                self.discover_faction(person.faction)
        else:
            raise Exception("relations called with not valid arg: %s" % person)
        if not self.know_person(person):
            relations = self._set_relations(person)
            return relations
        for rel in self._relations:
            if self in rel.persons and person in rel.persons:
                return rel

    def use_token(self):
        if self.token == 'power':
            return
        if self.token != 'antagonism':
            self.player_relations().stability += 1
            self.relations_tendency[self.token] += 1
        self.token = 'power'

    def set_token(self, token, free=False):
        if self.token == 'antagonism':
            if token == 'antagonism':
                self.player_relations.stance -= 1
            else:
                self.token = 'power'
                return
        self.token = token
        renpy.call_in_new_context('lbl_notify', self, token)

    def get_token_image(self):
        return {'power': 'images/tarot/arcana_lust.jpg',
                'conquest': 'images/tarot/arcana_charriot.jpg',
                'convention': 'images/tarot/arcana_justice.jpg',
                'contribution': 'images/tarot/arcana_lovers.jpg',
                'antagonism': 'images/tarot/arcana_moon.jpg'}[self.token]

    def player_relations(self):
        return self.relations(self.game_ref.player)

    def enslave(self, target):
        success = self.slaves.add_slave(target, self)
        if success:
            self.relations(target)

    def remove_slave(self, slave=None):
        slave = self.slaves.slaves()[0]
        self.slaves.remove_slave(slave)
        return slave

    def get_slaves(self):
        return self.slaves.slaves()

    def has_slaves(self):
        return len(self.get_slaves()) > 0

    def set_master(self, master):
        self._master = master

    def set_supervisor(self, supervisor):
        self.supervisor = supervisor

    def desirable_relations(self):
        d = {'lawful': ('formal', 'loyality'), 'chaotic': ('intimate', 'scum-slave'),
             'timid': ('delicate', 'worship'), 'ardent': ('intense', 'disciple'),
             'good': ('supporter', 'dedication'), 'evil': ('contradictor', 'henchman')}
        list_ = [self.alignment.morality_str(), self.alignment.orderliness_str(),
                 self.alignment.activity_str()]
        return [d.get(x) for x in list_]

    def willing_available(self):
        return []

    # favor methods
    def gain_favor(self, value):
        if self.player_controlled:
            return
        if self.game_ref.player not in self.known_characters:
            return
        value = self.favor + value
        if value < 0:
            self.favor = 0
            return
        hard_max = 5
        soft_max = 3 + self.player_stance().value
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
        pass
    # end of favor methods

    def can_tick(self):
        if not self.calculatable:
            return True
        return self._favor.can_tick() and self.has_money(self.decade_bill())

    def decade_bill(self):
        value = self.schedule.get_cost()
        return value

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

    @utilities.Observable
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
        self._remove_foodsystem()
        self.remove_genus()
        persons_list.remove(self)

    def remove_genus(self):
        self.genus.remove()

    def _remove_foodsystem(self):
        self.food_system.owner = None

    def _remove_features(self):
        self.features = []

    def remove_relations(self):
        characters = [i for i in self.known_characters]
        for i in characters:
            self.forget_person(i)

    def is_dead(self):
        if self.feature('dead') is not None:
            return True
        return False

    # rating methods
    def allure(self):
        value = self.agility
        value += self.count_modifiers('allure')
        return max(0, min(value, 5))

    def hardiness(self):
        value = self.physique
        value += self.count_modifiers('hardiness')
        return max(0, min(value, 5))

    def succulence(self):
        value = 3 + self.count_modifiers('succulence')
        return max(0, min(value, 5))

    def exotic(self):
        value = self.count_modifiers('exotic')
        return max(0, min(value, 5))

    def style(self):
        value = self.agility
        value += self.count_modifiers('style')
        return max(0, min(value, 5))

    def purity(self):
        value = self.count_modifiers('purity')
        return max(0, min(value, 5))

    def menace(self):
        value = self.physique
        value += self.skill('physique') - 3
        weapons = self.weapon_slots().values()
        if (self.get_slot('harness') is None and
                self.get_slot('belt1')is None and
                self.get_slot('belt2') is None):
            value -= 1
        for i in weapons:
            weapon = i.get_item()
            if weapon is not None:
                if weapon.size == 'twohand':
                    value += 1
                    break
        if self.armor is None:
            value -= 1
        elif self.armor.armor_rate == 'heavy_armor':
            value += 1
        value += self.count_modifiers('menace')
        return max(0, min(value, 5))

    def get_price(self):
        # pricing formula for untrained slaves
        pricing = store.slave_pricing
        modifiers = store.slave_price_modifiers
        basic = max([self.allure(), self.hardiness(), self.succulence()])
        modifier = max([self.purity(), self.exotic()])
        price = pricing[basic]
        price *= modifiers[modifier]
        return int(price)
    # end of rating methods

    def focus(self):
        return self.schedule.job.focus

    def job_skill(self):
        return self.schedule.job.skill

    @property
    def job(self):
        return self.schedule.job

    @property
    def accommodation(self):
        return self.schedule.accommodation

    @property
    def ration(self):
        return self.schedule.ration

    @property
    def job_difficulty(self):
        if self.schedule.job.difficulty is not None:
            return self.schedule.job.difficulty
        else:
            return 0

    def increase_productivity(self):
        if self.productivity_raised:
            return
        self.schedule.remove_buffer()
        self.schedule.job.focus += 1
        self.productivity_raised = True

    def reset_productivity(self):
        self.schedule.job.focus = 0

    def job_productivity(self):
        return self.schedule.job.focus

    def world(self):
        # not sure we need core reference here
        return self.game_ref.current_world

    # energy methods
    def set_energy(self):
        # value = self.count_modifiers('energy')
        value = self.energy
        self._energy = max(0, min(5, value))

    def drain_energy(self, value=1):
        self._energy -= value
        if self._energy < 0:
            self._energy = 0

    def gain_energy(self, value=1):
        self._energy += value
        if self._energy > 5:
            self._energy = 5

    def has_energy(self):
        return self._energy > 0
