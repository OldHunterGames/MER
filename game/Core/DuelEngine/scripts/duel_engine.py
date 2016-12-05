# -*- coding: <UTF-8> -*-
from random import *

from duel_data import *
from duel_actions import *
import renpy.store as store
import renpy.exports as renpy
import mer_utilities as utilities

def default_cards():
    return [key for key, value in store.actions_lib.items() if value['rarity'] == 'base']

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
    try:
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
    except IndexError:
        pass
    for card in return_to_hand:
        npc.hand.append(card)
    npc.drop = saved_drop
    npc.set_fight(simulated_fight)
    player.set_fight(simulated_fight)
    return returned

class BattlePoint(object):
    def __init__(self, name=None):
        self._value = 0
        self.active = True
        self.multipliers = []
        self._color = '#fff'
        self.name = name
    
    def multiplier(self):
        return len(self.multipliers)
    
    def add_multiplier(self, name):
        self.remove_multiplier(name)
        self.multipliers.append(name)

    def remove_multiplier(self, name):
        try:
            self.multipliers.remove(name)
        except ValueError:
            pass

    @property
    def value(self):
        if not self.active:
            return 0
        return self._value*(len(self.multipliers)+1)
    
    @property
    def true_value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    def copy_points(self, points):
        self._value = points._value
        self.active = points.active
        self.multipliers = points.multipliers
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
        for i in self.multipliers:
            str_ += '!'
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
    skill_level = combatant.skill_level
    for weapon in enemy_weapons:
        if weapon.damage_type == 'piercing':
            armor_ignoring.append('light')
        elif weapon.damage_type == 'impact':
            if weapon.size == 'twohand':
                armor_ignoring.appned('all')
            else:
                armor_ignoring.append('all-half')
        elif weapon.damage_type == 'elemental':
            armor_ignoring.append('heavy')
    #style bonuses
    ally_style = combatant.get_combat_style()
    enemy_style = enemy.get_combat_style()
    if ally_style == enemy_style and ally_style == 'resler':
        if combatant.physique > enemy.physique:
            d['excellence'].value += combatant.physique * (combatant.physique-enemy.physique)
    elif ally_style == 'rookie':
        for weapon in weapons:
            d['onslaught'].value += weapon.quality
    elif ally_style == 'beast':
        if enemy_style == 'beast':
            if combatant.physique > enemy.physique:
                d['excellence'].value += combatant.physique * (combatant.physique-enemy.physique)
        elif enemy_style == 'resler':
            d['excellence'].value += combatant.physique * min(1, (combatant.physique-enemy.physique))

    for weapon in weapons:
        #size bonuses
        if weapon.size == 'offhand':
            if situation == 'enclosed':
                d['maneuver'].value += weapon.quality*2
            else:
                d['maneuver'].value += weapon.quality
        elif weapon.size == 'versatile':
            if situation != 'enclosed' and any([i for i in enemy_weapons if i.size == 'offhand']) and enemy.combat_style != 'shieldbearer':
                d['onslaught'].value += weapon.quality*2
        elif weapon.size == 'twohand' and not any([i for i in enemy_weapons if i.size == 'twohand']):
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
    if combatant.armor_rate == 'light_armor' and not any([i for i in armor_ignoring if i =='light' or i == 'all']):
        bonus = combatant.physique + combatant.agility + combatant.protection_quality + skill_level
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['fortitude'].value += bonus
    elif combatant.armor_rate == 'unarmored' and not any([i for i in armor_ignoring if i == 'unarmored' or i == 'all']):
        bonus = combatant.agility + skill_level
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['maneuver'].value += bonus
    elif combatant.armor_rate == 'heavy_armor' and not any([i for i in armor_ignoring if i =='heavy' or i == 'all']):
        bonus = (combatant.physique + combatant.protection_quality + skill_level)*2
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
        self.persistent_actions = []
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
        self.player_turn = False
        

    def _get_combatant(self, side):
        try:
            combatant = getattr(self, side).pop()
        except IndexError:
            return self._end_fight(side)
        if side == 'allies':
            combatant.set_side('allies')
            renpy.call_screen('sc_prefight_equip', combatant, self)
        else:
            combatant.set_side('enemies')
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
        for action in self.persistent_actions:
            action.remove()
        self.persistent_actions = []
            
        self.current_ally.send_event('round_started')
        self.current_enemy.send_event('round_started')
        self.enemy_run()

    def start(self):
        self.current_ally = self._get_combatant('allies')
        self.current_enemy = self._get_combatant('enemies')
        self.current_ally.send_event('fight_started')
        self.current_enemy.send_event('fight_started')
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
        if enemy.hand_is_empty():
            return
        if self.passed and self.current_loser == 'allies':
            return
        if self.enemy_passed:
            self.send_event(enemy)
            return
        action = predict_result(enemy, self.current_ally, self)
        if action is not None:
            enemy.use_action(action)
        elif self.passed and self.compare_points() != 'allies' and self.enemies_loose_points > 0:
            for i in enemy.hand:
                enemy.use_action(i)
                break
            return self.enemy_run()
        else:
            self.enemy_passed = True
            self.send_event(enemy)
            return
        if self.passed:
            if self.compare_points() != 'allies':
                return self.enemy_run()
            else:
                return
        return 

    def update_stack(self, side, card):
        self.use_stack[side].append(card)

    def set_show_summary(self, bool_):
        self.show_summary = bool_

    def get_enemy_side(self, side):
        if side == 'allies':
            return 'enemies'
        else:
            return 'allies'

    def send_event(self, fighter):
        if fighter.side == 'allies':
            self.player_turn = False
            self.enemy_run()
        elif fighter.side == 'enemies':
            self.player_turn = True
class DuelCombatant(object):
    """
    This class makes a characters participating in Fast Fight.
    """

    def __init__(self, person=None):
        self.person = person
        cards = default_cards()
        default_deck = Deck()
        shuffle(cards)
        while not default_deck.is_at_limit():
            if len(cards) > 0:
                default_deck.add_card(cards.pop())
            else:
                break
        try:
            if person.card_storage is None:
                person.card_storage = CardStorage()
        except AttributeError:
            pass
        try:
            if not isinstance(person.deck, Deck):
                person.deck = default_deck
            elif not person.deck.is_completed():
                person.deck = default_deck
            person.decks.append(default_deck)
            self.deck = person.deck
        except AttributeError:
            self.deck = default_deck
        
        try:
            self.name = person.name
        except AttributeError:
            self.name = 'Unknown'
        
        try:
            self.skill = person.skill('combat')
        except AttributeError:
            self.skill = None
        
        try:
            self.skill_level = person.skill('combat').level
        except AttributeError:
            self.skill_level = 0
        
        self.init_stats()
        self.side = None
        self.fight = None
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
        try:
            self.avatar = person.avatar_path
        except AttributeError:
            self.avatar = utilities.default_avatar_path()
        self.escalation = 0
        self.combat_style = self.get_combat_style()
        self.loosed = False
        self.default_points = {'onslaught': 0, 'maneuver': 0, 'fortitude': 0, 'excellence': 0}
        self.last_event = None
    @property
    def decks(self):
        try:
            decks = self.person.decks
        except AttributeError:
            decks = []
        return decks
    def draw_list(self):
        list_ = [i for i in self.drop if i.drawable()]
        return list_
    def init_stats(self):
        for i in ['physique', 'agility']:
            try:
                setattr(self, i, getattr(self.person, i))
            except AttributeError:
                setattr(self, i, 0)
    @property
    def last_played_card(self):
        try:
            last = self.drop[-1]
            return last
        except IndexError:
            return 
    
    @property
    def main_weapon(self):
        try:
            weapon = self.person.main_hand
        except AttributeError:
            weapon = None
        return weapon
    
    @property
    def other_weapon(self):
        try:
            weapon = self.person.other_hand
        except AttributeError:
            weapon = None
        return weapon
    
    @property
    def armor(self):
        try:
            armor = self.person.armor
        except AttributeError:
            armor = None
        return armor

    def has_shield(self):
        return self.person.has_shield()
    
    def hand_is_empty(self):
        if len(self.hand) < 1:
            return True
        return False
    def set_deck(self, deck):
        self.deck = deck
    def set_hand(self):
        if self.deck is not None:
            self.hand = self.deck.get_hand(self)
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
        #TODO: add beast combat style
        style = 'resler'
        if len(self.get_weapons()) > 0:
            if self.skill.expirience:
                if self.main_weapon.type == 'twohand':
                    style = 'juggernaut'
                elif self.has_shield():
                    style = 'shieldbearer'
                else:
                    style = 'breter'
            elif self.skill.training:
                style = 'rookie'
        return style

    def get_weapons(self):
        l = []
        if self.main_weapon is not None:
            if self.main_weapon.type == 'weapon':
                l.append(self.main_weapon)
        if self.other_weapon is not None and self.other_weapon != self.main_weapon:
            if self.other_weapon.type == 'weapon':
                l.append(self.other_weapon)
        return l
    
    def set_side(self, side):
        self.side = side
    
    def set_fight(self, fight):
        self.fight = fight
    
    def use_action(self, duel_action):
        
        points, escalation = duel_action.use()
        if self.escalation < escalation:
            self.escalation = escalation
        if duel_action.slot is not None:
            self.fight.points[self.side][duel_action.slot].value += points
        self.fight.update_stack(self.side, duel_action)
        if duel_action.persistent:
            self.fight.persistent_actions.append(duel_action)
        self.fight.send_event(self)
        if duel_action in self.hand:
            self.drop_card(duel_action)

    def drop_card(self, card):
        self.drop.append(card)
        self.hand.remove(card)

    def use_from_drop(self, duel_action):
        if duel_action not in self.drop:
            return
        points, escalation = duel_action.use()
        if self.escalation < escalation:
            self.escalation = escalation
        if duel_action.slot is not None:
            self.fight.points[self.side][duel_action.slot].value += points
        self.fight.update_stack(self.side, duel_action)
        if duel_action.persistent:
            self.fight.persistent_actions.append(duel_action)

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
        if event == 'fight_started':
            self.set_hand()
        self.last_event = event
    

class CardStorage(object):


    def __init__(self):
        self.default_cards = [make_card(i) for i in default_cards()]
        self.other_cards = []

    @property
    def cards(self):
        list_ = []
        list_.extend(self.default_cards)
        list_.extend(self.other_cards)
        return list_

    def add_card(self, card_id):
        self.other_cards.append(make_card(card_id))


class Deck(object):
    cards_limit = {'base': 4, 'common': 4, 'uncommon': 3, 'rare': 2, 'unique': 1}
    def __init__(self, cards_list=None):
        self.name = 'default name'
        self.cards_list = [make_card(card) for card in cards_list] if cards_list is not None else []
        self.combat_style = None
    
    def set_name(self, name):
        self.name = name
    def set_style(self, style):
        self.combat_style = style
    
    def is_at_limit(self):
        return len(self.cards_list) >= 40
    
    def is_completed(self):
        if len(self.cards_list) == 40:
            return True
        return False
    
    def is_usable(self):
        return len(self.cards_list) >= 22
    def description(self):
        txt = self.name
        txt += '\n(%s/40)'%(len(self.cards_list))
        return txt
    
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
        if self.is_completed():
            return False
        else:
            limit = self.cards_limit[card.rarity] < self.count_cards(card.id)
            if card.combat_style is not None:
                style = self.combat_style == card.combat_style
            else:
                style = True
            return limit and style

    def get_hand(self, fighter):
        shuffled = [card for card in self.cards_list]
        shuffle(shuffled)
        hand = []
        for i in range(10):
            try:
                hand.append(shuffled.pop())
            except IndexError:
                break
        return Hand(self, hand, shuffled, fighter)


class Hand(object):
    def __init__(self, deck, cards_list, cards_left, fighter):
        self.deck = deck
        self._cards_left = cards_left
        self.cards_list = cards_list
        for card in cards_list:
            card.current_fighter = fighter
        for card in cards_left:
            card.current_fighter = fighter

    def add_card(self, card=None):
        if card is not None:
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

    def get_all_cards(self):
        list_ = [i for i in self.cards_list]
        list_.extend(self._cards_left)
        return list_


class DuelAction(object):
    """
    This is a class for "action cards" to form a decks and use in FaFiEn.
    """
    bool_values = ['use_weapon', 'unique']
    must_have_values = ['name', 'rarity']
    def __init__(self, id_):
        self.id = id_
        self.data = store.actions_lib
        self.current_fighter = None
        self.default_power = 0
        self.escalation = 0
        self._power = None
        self.evaluate_power = True
    
    @property
    def power_mods(self):
        try:
            mods = self.data[self.id]['power_mods']
            if mods is None:
                mods = []
        except KeyError:
            mods = []
        return mods
    
    @property
    def special_mechanics(self):
        try:
            list_ = self.data[self.id]['special_mechanics']
            if list_ is None:
                list_ = []
        except KeyError:
            list_ = []
        return list_
    @property
    def tag(self):
        try:
            tag = self.data[self.id]['tag']
        except KeyError:
            tag = None
        return tag
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
    
    def drawable(self):
        return (self.rarity != 'exceptional' and self.power > 0 and
            not any([i in store.special_mechanics['card_draw'] for i in self.special_mechanics]))
    
    @property
    def power(self):
        if self.evaluate_power:
            self.evaluate_power = False
        else:
            return 0
        if self._power is not None:
            return self._power
        try:
            power = self.data[self.id]['power']
        except KeyError:
            power = 0
        if self.use_weapon:
            for weapon in self.current_fighter.get_weapons():
                power += weapon.quality
        for i in self.power_mods:
            try:
                power += i(self)
            except TypeError:
                pass
        self.evaluate_power = True
        return power
    
    @power.setter
    def power(self, value):
        self._power = value

    @property
    def persistent(self):
        return hasattr(self, 'on_remove')

    def remove(self):
        if self.persistent:
            self.on_remove(self)

    def use(self):
        self.current_fighter.send_event('card_used')
        eval_list = []
        eval_last = []
        for i in self.special_mechanics:
            if i in store.special_mechanics['eval_early']:
                eval_list.insert(0, i)
            elif i in store.special_mechanics['eval_last']:
                eval_last.append(i)
            else:
                eval_list.append(i)
        eval_list.extend(eval_last)
        for i in eval_list:
            i(self)
        self.escalation = self.power
        if self.rarity == 'exceptional':
            if self.power > 0:
                self.power += 5
            self.escalation = 0
        values = (self.power, self.escalation)
        self.power = None
        self.escalation = 0
        return values
    
    def show(self):
        try:
            str_ = self.description
        except AttributeError:
            pass
        str_ += '\n %s'%(self.name)
        if self.slot is not None:
            str_ += '\n'
            str_ += '(%s: %s)'%(self.slot, self.power)

        return str_
def make_card(card_id):
    try:
        card = store.actions_lib[card_id]
    except KeyError:
        raise Exception("unknown card %s"%(card_id))
    card = DuelAction(card_id)
    return card