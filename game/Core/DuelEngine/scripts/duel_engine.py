# -*- coding: <UTF-8> -*-
from random import *
from duel_data import *
from duel_actions import *
import renpy.store as store
import renpy.exports as renpy

def default_cards():
    return []

def predict_result(npc, player, simulated_fight):
    test_fight = DuelEngine([player], [npc], simulated_fight.situation, True)
    test_fight.points = {'allies': {}, 'enemies': {}}
    for key in simulated_fight.points:
        for k, v in simulated_fight.points[key].items():
            points = BattlePoint(k)
            points.copy_points(v)
            test_fight.points[key][k] = points

    current_value = simulated_fight.summary('allies') - simulated_fight.summary('enemies')
    npc.fight = test_fight
    return_to_hand = []
    saved_drop = [action for action in npc.drop]
    returned = None
    
    for card in npc.hand:
        npc.use_action(card)
        new_value = test_fight.summary('allies') - test_fight.summary('enemies')
        if new_value > current_value:
            return_to_hand.append(npc.drop.pop())
            returned = None
        elif new_value == current_value:
            if simulated_fight.enemies_loose_points > 0:
                returned = card
            elif npc.last_event == 'draw_card' and len(saved_drop) > 1:
                returned = card
            else:
                return_to_hand.append(npc.drop.pop())
                returned = None
        else:
            returned = card
        if returned != None:
            npc.hand.append(returned)
            break
    
    for card in return_to_hand:
        npc.hand.append(card)
    npc.drop = saved_drop
    npc.fight = simulated_fight
    player.fight = simulated_fight
    return returned

class BattlePoint(object):
    def __init__(self, name=None):
        self._value = 0
        self.active = True
        self.doubled = False
        self._color = '#fff'
        self.name = name
    
    @property
    def value(self):
        if self.doubled:
            return self._value*2
        if not self.active:
            return 0
        return self._value
    
    @property
    def true_value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    def copy_points(self, points):
        self._value = points._value
        self.active = points.active
        self.doubled = points.doubled
    @property
    def color(self):
        if self.active:
            return self._color
        return "#000"

    def set_color(self, color):
        self._color = color
    @property
    def description(self):
        str_ = "{color=%s}%s: %s{/color}"%(self.color, self.name, self.value)
        return str_
def init_points(combatant, enemy, situation):
    d = {'onslaught':BattlePoint('onslaught'), 'maneuver': BattlePoint('maneuver'),
         'fortitude': BattlePoint('fortitude'), 'excellence': BattlePoint('excellence')}
    d['onslaught'].set_color('#ff0000')
    d['maneuver'].set_color('#64f742')
    d['fortitude'].set_color('#00007f')
    d['excellence'].set_color('#ffff00')
    for key, value in combatant.default_points.items():
        d[key].value += value
    weapons = combatant.get_weapons()
    enemy_weapons = enemy.get_weapons()
    armor_ignoring = []
    person = combatant.person
    skill = person.skill('combat')
    for weapon in enemy_weapons:
        if weapon.damage_type == 'piercing':
            armor_ignoring.append('light')
        elif weapon.damage_type == 'impact':
            if weapon.size == 'twohanded':
                armor_ignoring.appned('all')
            else:
                armor_ignoring.append('all-half')
        elif weapon.damage_type == 'elemental':
            armor_ignoring.append('heavy')


    for weapon in weapons:
        #size bonuses
        if weapon.size == 'small':
            if situation == 'enclosed':
                d['maneuver'].value += weapon.quality*2
            else:
                d['maneuver'].value += weapon.quality
        elif weapon.size == 'standart':
            if situation != 'enclosed' and any([i for i in enemy_weapons if i.size == 'small']) and enemy.combat_style != 'shieldbearer':
                d['onslaught'].value += weapon.quality*2
        elif weapon.size == 'twohanded' and not any([i for i in enemy_weapons if i.size == 'twohanded']):
            d['onslaught'].value += weapon.quality*3
        #damage_type bonuses
        if weapon.damage_type == 'slashing' and enemy.armor_rate == 'unarmored' and enemy.creature_type == 'natural':
            d['excellence'].value += weapon.quality*2
        elif weapon.damage_type == 'piercing':
            d['excellence'].value += weapon.quality
        elif weapon.damage_type == 'elemental' and enemy.armor_rate == 'heavy':
            d['onslaught'].value += weapon.quality*2
        elif weapon.damage_type == 'silvered' and enemy.creature_type == 'supernatural':
            d['excellence'].value += weapon.quality*2
    #armor bonuses
    if combatant.armor_rate == 'light' and not any([i for i in armor_ignoring if i =='light' or i == 'all']):
        bonus = person.physique + person.agility + combatant.protection_quality + skill.level
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['fortitude'].value += bonus
    elif combatant.armor_rate == 'unarmored' and not any([i for i in armor_ignoring if i == 'unarmored' or i == 'all']):
        bonus = person.agility + skill.level
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['maneuver'].value += bonus
    elif combatant.armor_rate == 'heavy' and not any([i for i in armor_ignoring if i =='heavy' or i == 'all']):
        bonus = (person.physique + combatant.protection_quality + skill.level)*2
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['fortitude'].value += bonus

    return d

class DuelEngine(object):

    def __init__(self, allies_list, enemies_list, situation=None, simulation=False):
        self.allies = allies_list
        self.enemies = enemies_list
        self.simulation = simulation
        for i in self.allies:
            i.set_fight(self)
            i.set_side('allies')
        for i in self.enemies:
            i.set_fight(self)
            i.set_side('enemies')
        self.current_ally = None
        self.current_enemy = None
        self.use_stack = {'allies': [], 'enemies': []}

        self.points = {}
        self.round = 0
        
        self.situation = situation
        self.type = 'solo' if len(self.allies) == 1 and len(self.allies) == len(self.enemies) else 'mass'
        self.allies_loose_points = 0
        self.enemies_loose_points = 0
        self.pass_ = False
        self.show_summary = False
        self.ended = False
        self.enemy_passed = True
        

    def _get_combatant(self, side):
        try:
            combatant = getattr(self, side).pop()
        except IndexError:
            return self._end_fight(side)
        if side == 'allies':
            combatant.set_side('allies')
            renpy.call_screen('sc_prefight_equip', combatant.person)
        else:
            combatant.set_side('enemies')
        if not self.simulation:
            combatant.set_hand()
        self.use_stack = {'allies': [], 'enemies': []}
        return combatant
        

    def _end_fight(self, loosed_side):
        self.loser = loosed_side
        self.ended = True
        renpy.call_in_new_context('lbl_duel_battle_end', self)

    def round_end(self, loosed_side=None):
        if loosed_side == None:
            loosed_side = self.compare_points()
        self.current_ally.escalation = 0
        self.current_enemy.escalation = 0
        side = 'ally' if loosed_side == 'allies' else 'enemy'
        loser_str = 'current_%s'%(side)
        loser = getattr(self, loser_str)
        self.current_ally.send_event('end_round')
        self.current_enemy.send_event('end_round')
        if self.type == 'solo':
            attr = '%s_loose_points'%(loosed_side)
            value = getattr(self, attr) + 1
            setattr(self, attr, value)
            loser.send_event('loose')

            if value > 1:
                self._end_fight(loosed_side)
               
            else:
                self.start_new_round()
        elif self.type == 'mass':
            combatant = self._get_combatant(loosed_side)
            setattr(self, loser_str, combatant)
            self.start_new_round()

    def compare_points(self):
        d = {'allies': self.summary('allies'), 'enemies': self.summary('enemies')}
        loser = 'enemies' if d['allies'] > d['enemies'] else 'allies'
        return loser
    @property
    def current_loser(self):
        return self.compare_points()
    def summary(self, side):
        value = sum(i.value for i in self.points[side].values())
        return value
    def start_new_round(self):
        self.pass_ = False
        self.round += 1
        self.enemy_passed = False
        if self.round > 1:
            self.points = {'allies': init_points(self.current_ally, self.current_enemy, self.situation),
                            'enemies': init_points(self.current_enemy, self.current_ally, self.situation)}
            
            
        self.current_ally.send_event('round_started')
        self.current_enemy.send_event('round_started')
        self.enemy_run()

    def start(self):
        self.current_ally = self._get_combatant('allies')
        self.current_enemy = self._get_combatant('enemies')
        self.points = {'allies': init_points(self.current_ally, self.current_enemy, self.situation),
                        'enemies': init_points(self.current_enemy, self.current_ally, self.situation)}
        self.start_new_round()
        renpy.call_in_new_context('duel_battle_init', self)
        
        

    def view_points(self, side):
        return [(key, i.value) for key, i in self.points[side].items()]

    @property
    def passed(self):
        if self.pass_ or self.current_ally.hand_is_empty() or self.ended:
            return True
        return False
    def make_pass(self):
        self.pass_ = True

    def enemy_run(self):
        enemy = self.current_enemy
        if self.passed and self.current_loser == 'allies':
            return
        if self.enemy_passed:
            return
        try:
            action = predict_result(enemy, self.current_ally, self)
            if action != None:
                enemy.use_action(action)
            else:
                self.enemy_passed = True
        except IndexError:
                return 
        if self.passed:
            if self.compare_points() != 'allies':
                return self.enemy_run()
            else:
                return 

    def update_stack(self, side, card):
        self.use_stack[side].append(card)

    def set_show_summary(self, bool_):
        self.show_summary = bool_

class DuelCombatant(object):
    """
    This class makes a characters participating in Fast Fight.
    """
    def __init__(self, person):
        self.person = person
        cards_list = default_cards()
        if not person.default_cards:
            person.add_default_cards(cards_list)
        if not isinstance(person.deck, Deck):
            person.deck = Deck()
            for card in cards_list:
                person.deck.add_card(card)
        elif not person.deck.is_completed():
            person.deck = Deck()
            for card in cards_list:
                person.deck.add_card(card)
        self.name = person.name
        self.side = None
        self.fight = None
        self.deck = person.deck
        self.hand = []
        self.drop = []
        if self.armor != None:
            self.armor_rate = self.armor.armor_rate
        else:
            self.armor_rate = 'unarmored'
        if self.armor != None:
            self.protection_quality = self.armor.quality
        else:
            self.protection_quality = 0
        self.creature_type = None #TODO: get creature type from person.genus
        self.name = person.name
        self.avatar = person.avatar_path
        self.escalation = 0
        self.combat_style = self.get_combat_style()
        self.loosed = False
        self.default_points = {'onslaught': 0, 'maneuver': 0, 'fortitude': 0, 'excellence': 0}
        self.last_event = None

    @property
    def last_played_card(self):
        try:
            last = self.drop[-1]
            return last
        except IndexError:
            return 
    
    @property
    def main_weapon(self):
        return self.person.main_hand
    
    @property
    def other_weapon(self):
        return self.person.other_hand
    
    @property
    def armor(self):
        return self.person.armor
    
    def hand_is_empty(self):
        if len(self.hand) < 1:
            return True
        return False
    def set_deck(self, deck):
        self.deck = deck
    def set_hand(self):
        if self.deck != None:
            self.hand = self.deck.get_hand()
        else:
            raise Exception("set_hand called, but this combatant has no choosen deck yet")
    def shuffle_actions(self):
        self.reserve.extend(self.discard)
        self.discard = []
        shuffle(self.reserve)

    def draw(self, number=1):
        # Drawing no more than we have at all
        while number > 0:
            number -= 1
            if self.hand.can_draw():
                self.hand.add_card()
                self.send_event('draw_card')
            else:
                return

    def draw_from_drop(self, card):
        if card in self.drop:
            self.hand.append(card)
            self.drop.remove(card)
            self.send_event('draw_card')
    def get_combat_style(self):
        if self.person.has_shield():
            return 'shieldbearer'
        if self.person.main_hand != None and self.person.other_hand != None:
            return 'juggernaut'
        if self.person.main_hand != None or self.person.other_hand != None:
            return 'breter'
        return 'restler'

    def get_weapons(self):
        l = []
        if self.main_weapon != None:
            if self.main_weapon.type == 'weapon':
                l.append(self.main_weapon)
        if self.other_weapon != None and self.other_weapon != self.main_weapon:
            if self.other_weapon.type == 'weapon':
                l.append(self.other_weapon)
        return l
    
    def set_side(self, side):
        self.side = side
    
    def set_fight(self, fight):
        self.fight = fight
    
    def use_action(self, duel_action):
        if self.escalation < duel_action.power:
            self.escalation = duel_action.power
        points = duel_action.use(self)
        if duel_action.slot != None:
            self.fight.points[self.side][duel_action.slot].value += points
        self.fight.update_stack(self.side, duel_action)
        if duel_action.power > 0:
            self.drop.append(duel_action)
        self.hand.remove(duel_action)

    def send_event(self, event):
        if event == 'end_round':
            if self.combat_style == 'breter':
                self.draw()
            elif self.combat_style == 'juggernaut':
                points = self.fight.points[self.side]['onslaught']
                value = points.value
                self.default_points['onslaught'] += min(value, self.escalation)
            elif self.combat_style == 'shieldbearer':
                pass
        if event == 'loose':
            if self.combat_style == 'beast':
                self.default_points['excellence'] += self.escalation
        if event == 'roud_started':
            self.default_points = {'onslaught': 0, 'maneuver': 0, 'fortitude': 0, 'excellence': 0}
        self.last_event = event
            

class Deck(object):
    def __init__(self, cards_list=None):
        self.cards_list = [make_card(card) for card in cards_list] if cards_list != None else []
        self.current = None
        self.style = None

    def is_completed(self):
        if len(self.cards_list) == 22:
            return True
        return False

    def set_style(self, style):
        self.style = style
    
    def add_card(self, card_id):
        if isinstance(card_id, DuelAction):
            self.cards_list.append(card_id)
        else:
            self.cards_list.append(make_card(card_id))

    def remove_card(self, card):
        self.cards_list.remove(card)
    
    def count_cards(self, card_id):
        value = 0
        for card in self.cards_list:
            if card.id == card_id:
                value += 1
        return value
    
    def can_be_added(self, card):
        if self.count_cards(card.id) > 2 and not card.unique:
            return False
        elif self.count_cards(card.id) > 0 and card.unique:
            return False
        return True

    def get_hand(self):
        shuffled = [card for card in self.cards_list]
        shuffle(shuffled)
        hand = []
        for i in range(10):
            try:
                hand.append(shuffled.pop())
            except IndexError:
                break
        return Hand(self, hand, shuffled)


class Hand(object):
    def __init__(self, deck, cards_list, cards_left):
        self.deck = deck
        self._cards_left = cards_left
        self.cards_list = cards_list

    def add_card(self, card=None):
        if card != None:
            self.cards_list.append(card)
            return
        self.get_from_deck()

    def append(self, item):
        self.cards_list.append(item)

    def __iter__(self):
        return self.cards_list.__iter__()

    def remove(self, item):
        self.cards_list.remove(item)

    def __len__(self):
        return len(self.cards_list)

    def get_from_deck(self):
        try:
            self.cards_list.append(self._cards_left.pop())
        except IndexError:
            return

    def can_draw(self):
        return len(self._cards_left) > 0


class DuelAction(object):
    """
    This is a class for "action cards" to form a decks and use in FaFiEn.
    """
    bool_values = ['use_weapon', 'mighty', 'unique']
    must_have_values = ['name', 'rarity']
    def __init__(self, id_):
        self.id = id_
        self.data = store.actions_lib

    def __getattr__(self, key):
        try:
            id_ = self.__dict__['id']
            value = self.__dict__['data'][id_][key]
            return value
        except KeyError:
            if key in DuelAction.bool_values:
                return False
            elif key == 'power':
                return 0
            elif key in DuelAction.must_have_values:
                raise Exception('DuelAction with id %s do not have value %s'%(self.id, key))
            elif key == 'style' or key == 'special_effect' or key == 'slot':
                return None
        raise AttributeError(key)

    
    def use(self, user):
        user.send_event('card_used')
        power = self.power
        if self.mighty:
            power += 5
        if self.use_weapon:
            for weapon in user.get_weapons():
                power += weapon.quality
        if self.special_effect != None:
            self.special_effect(user)
        return power
    
    def show(self):
        try:
            str_ = self.description
        except AttributeError:
            pass
        str_ += "\n %s(%s"%(self.name, self.slot)
        if self.slot != None:
            str_ += ': %s)'%(self.power)
        else:
            str_ += ')'

        return str_

def make_card(card_id):
    try:
        card = store.actions_lib[card_id]
    except KeyError:
        raise Exception("unknown card %s"%(card_id))
    card = DuelAction(card_id)
    return card