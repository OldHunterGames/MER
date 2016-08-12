# -*- coding: <UTF-8> -*-
from random import *
from duel_data import *
from duel_actions import *
import renpy.store as store
import renpy.exports as renpy

class BattlePoint(object):
    def __init__(self):
        self._value = 0
        self.active = True
        self.doubled = False
    @property
    def value(self):
        if self.doubled:
            return self._value*2
        if not self.active:
            return 0
        return self._value
    @value.setter
    def value(self, value):
        self._value = value
def init_points(combatant, enemy, situation):
    d = {'onslaught':BattlePoint(), 'maneuver': BattlePoint(), 'fortitude': BattlePoint(), 'excellence': BattlePoint()}
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
        if weapon.damage_type == 'slashing' and enemy.protection_type == 'unarmored' and enemy.creature_type == 'natural':
            d['excellence'].value += weapon.quality*2
        elif weapon.damage_type == 'piercing':
            d['excellence'].value += weapon.quality
        elif weapon.damage_type == 'elemental' and enemy.protection_type == 'heavy':
            d['onslaught'].value += weapon.quality*2
        elif weapon.damage_type == 'silvered' and enemy.creature_type == 'supernatural':
            d['excellence'].value += weapon.quality*2
    #armor bonuses
    if combatant.protection_type == 'light' and not any([i for i in armor_ignoring if i =='light' or i == 'all']):
        bonus = person.physique + person.agility + combatant.protection_quality + skill.level
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['fortitude'].value += bonus
    elif combatant.protection_type == 'unarmored' and not any([i for i in armor_ignoring if i == 'unarmored' or i == 'all']):
        bonus = person.agility + skill.level
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['maneuver'].value += bonus
    elif combatant.protection_type == 'heavy' and not any([i for i in armor_ignoring if i =='heavy' or i == 'all']):
        bonus = (person.physique + combatant.protection_quality + skill.level)*2
        if 'all-half' in armor_ignoring:
            bonus /= 2
        d['fortitude'].value += bonus

    return d

class DuelEngine(object):

    def __init__(self, allies_list, enemies_list, situation=None):
        self.allies = allies_list
        self.enemies = enemies_list
        for i in self.allies:
            i.set_fight(self)
            i.set_side('allies')
        for i in self.enemies:
            i.set_fight(self)
            i.set_side('enemies')
        self.current_ally = self._get_combatant('allies')
        self.current_enemy = self._get_combatant('enemies')

        self.points = {'allies': init_points(self.current_ally, self.current_enemy, situation),
                        'enemies': init_points(self.current_enemy, self.current_ally, situation)}
        self.round = 0
        
        self.situation = situation
        self.type = 'solo' if len(self.allies) == 0 and len(self.allies) == len(self.enemies) else 'mass'
        self.allies_loose_points = 0
        self.enemies_loose_points = 0
        self.pass_ = False
        self.show_summary = False
        self.ended = False

    def _get_combatant(self, side):
        try:
            combatant = getattr(self, side).pop()
            if side == 'allies':
                combatant.set_side('allies')
            else:
                combatant.set_side('enemies')
            combatant.set_hand()
            return combatant
        except IndexError:
            return self._end_fight(side)

    def _end_fight(self, loosed_side):
        self.loser = loosed_side
        self.ended = True
        renpy.call_in_new_context('lbl_duel_battle_end', self)

    def round_end(self, loosed_side=None):
        if loosed_side == None:
            loosed_side = self.compare_points()
        self.current_ally.escalation = 0
        self.current_enemy.escalation = 0
        self.show_summary = True
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
        self.show_summary = False
        self.pass_ = False
        self.round += 1
        if self.round > 1:
            self.points = {'allies': init_points(self.current_ally, self.current_enemy, self.situation),
                            'enemies': init_points(self.current_enemy, self.current_ally, self.situation)}
            
        self.current_ally.send_event('round_started')
        self.current_enemy.send_event('round_started')

    def start(self):
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
        try:
            action = enemy.hand[-1]
            enemy.use_action(action)
        except IndexError:
                return 
        if self.passed:
            if self.compare_points() != 'allies':
                return self.enemy_run()
            else:
                return 


class DuelCombatant(object):
    """
    This class makes a characters participating in Fast Fight.
    """
    def __init__(self, person):
        self.person = person
        self.name = person.name
        self.side = None
        self.fight = None
        self.deck = None
        self.hand = []
        self.drop = []
        if self.armor != None:
            self.protection_type = self.armor.protection_type
        else:
            self.protection_type = 'unarmored'
        if self.armor != None:
            self.protection_quality = self.armor.quality
        else:
            self.protection_quality = 0
        self.creature_type = None #TODO: get creature type from person.genus
        self.name = person.name
        self.avatar = person.avatar_path
        self.escalation = 0
        self.combat_style = self.get_combat_style()
        self.deck = None
        self.loosed = False
        self.default_points = {'onslaught': 0, 'maneuver': 0, 'fortitude': 0, 'excellence': 0}
    
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
            self.deck.fight_started()
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
            card = self.deck.get_card()
            if card != None:
                self.hand.append(self.deck.get_card())
            else:
                return

    def draw_from_drop(self, card):
        if card in self.drop:
            self.hand.append(card)
            self.drop.remove(card)
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

            

class Deck(object):
    def __init__(self, cards_list=None):
        self.cards_list = [make_card(card) for card in cards_list] if cards_list != None else []
        self.current = None
        self.style = None

    def set_style(self, style):
        self.style = style
    
    def add_card(self, card_id):
        self.card_list.append(make_card(card_id))
    
    def _count_cards(self, card_id):
        value = 0
        for card in self.cards_list:
            if card.id == card_id:
                value += 1
        return value
    
    def can_be_added(self, card):
        if self._count_cards(card.id) > 2 and not card.unique:
            return False
        elif self._count_cards(card.id) > 0 and card.unique:
            return False
        return True

    def fight_started(self):
        self.current = [card for card in self.cards_list]
        shuffle(self.current)

    def get_hand(self):
        hand = []
        for i in range(10):
            try:
                hand.append(self.current.pop())
            except IndexError:
                return hand
        return hand

    def get_card(self):
        try:
            card = self.current.pop()
            return card
        except IndexError:
            return 

    def remove_card(self, card_id):
        for card in self.cards_list:
            if card.id == card_id:
                self.cards_list.remove(card)
                return


class DuelAction(object):
    """
    This is a class for "action cards" to form a decks and use in FaFiEn.
    """
    bool_values = ['use_weapon', 'mighty', 'unique']
    must_have_values = ['name', 'rarity']
    def __init__(self, id_):
        self.id = id_
        self.data = store.actions_lib[id_]

    def __getattr__(self, key):
        try:
            value = self.__dict__['data'][key]
            return value
        except KeyError:
            if key in DuelAction.bool_values:
                return False
            elif key == 'power':
                return 0
            elif key in DuelAction.must_have_values:
                raise Exception('DuelAction with id %s do not have value %s'%(self.id, key))
            return None
    
    def use(self, user):
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
        str_ = "%s(%s"%(self.name, self.slot)
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