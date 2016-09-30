init python:
    sys.path.append(renpy.loader.transfn("Core/DuelEngine/scripts"))
    import random as rand

    from duel_engine import DuelAction

    def make_inactive(battlepoints_list):
        for point in battlepoints_list:
            point.active = False
    
    def make_active(battlepoints_list):
        for point in battlepoints_list:
            point.active = True
    
    def clinch_special(card):
        user = card.current_fighter
        battle_points = [value['maneuver'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    
    def clinch_remove(card):
        user = card.current_fighter
        battle_points = [value['maneuver'] for value in user.fight.points.values()]
        make_active(battle_points)
    
    def hit_n_run_special(card):
        user = card.current_fighter
        battle_points = [value['onslaught'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    
    def hit_n_run_remove(card):
        user = card.current_fighter
        battle_points = [value['onslaught'] for value in user.fight.points.values()]
        make_active(battle_points)
    
    def rage_special(card):
        user = card.current_fighter
        battle_points = [value['fortitude'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    
    def rage_remove(card):
        user = card.current_fighter
        battle_points = [value['fortitude'] for value in user.fight.points.values()]
        make_active(battle_points)
    def outsmart_special(card):
        user = card.current_fighter
        for action in user.fight.persistent_actions:
            action.remove()
        user.fight.persistent_actions = []
    def fallback_special(card):
        user = card.current_fighter
        if len(user.drop) < 1:
            return
        value = 0
        point_to_decrease = None
        for point in user.fight.points[user.side].values():
            if point.value > value:
                value = point.value
                point_to_decrease = point
        if point_to_decrease != None:
            point_to_decrease.value -= user.escalation
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('draw_from_drop', user, 'draw_card', user.draw_from_drop)
        else:
            max_ = 0
            card_to_get = None
            for card in user.drop:
                if card.power > max_:
                    card_to_get = card
                    max_ = card.power
            user.draw_from_drop(card_to_get)

    #special mechanincs
    def reckless(card):
        user = card.current_fighter
        fight = user.fight
        side = fight.get_enemy_side(user.side)
        if card.rarity != 'exceptional':
            card.power += 5
            slot = 'excellence'
        else:
            slot = card.slot
        fight.points[side][slot].value += card.power
        card.set_power(0)

    def advantage(card):
        user = card.current_fighter
        user.draw(2)

    def combo(card):
        user = card.current_fighter
        if len(user.drop) < 1:
            return
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('draw_from_drop', user, 'use_card', user.use_from_drop)
        else:
            max_ = 0
            card_to_get = None
            for card in user.drop:
                if card.power > max_:
                    card_to_get = card
                    max_ = card.power
            user.use_from_drop(card_to_get)

    def amplifiction(card):
        user = card.current_fighter
        fight = user.fight
        points = fight.points[user.side][card.slot]
        points.add_multiplier('amplifiction')

    def sequence(card):
        user = card.current_fighter
        hand = user.hand
        for i in hand.get_all_cards():
            if i.id == card.id:
                user.use_action(i)

    def use_slot(card, slot):
        user = card.current_fighter
        points = user.fight.points[user.side][slot]
        points.value += card.power
    
    def slot_chosing(card, names):
        user = card.current_fighter
        active_points = []
        for i in names:
            if user.fight.points[user.side][i].active:
                active_points.append(i)
        try:
            choosed = active_points[0]
            multi = user.fight.points[user.side][choosed].multiplier()
        except IndexError:
            return
        if len(active_points) < 2:
            return choosed 
        for i in active_points:
            points = user.fight.points[user.side][i]
            if points.multiplier > multi:
                choosed = i
        points = user.fight.points[user.side][i]
        points.value += card.power


    def counterstrike(card):
        user = card.current_fighter
        names = ['onslaught', 'fortitude']
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('sc_chose_slot', card, user, names)
        else:
            points = slot_chosing(card, names)
            

    def footwork(card):
        user = card.current_fighter
        names = ['maneuver', 'fortitude']
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('sc_chose_slot', card, user, names)
        else:
            points = slot_chosing(card, names)

    def outflank(card):
        user = card.current_fighter
        names = ['maneuver', 'onslaught']
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('sc_chose_slot', card, user, names)
        else:
            points = slot_chosing(card, names)

    def versatile(card):
        user = card.current_fighter
        names = ['maneuver', 'onslaught', 'fortitude']
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('sc_chose_slot', card, user, names)
        else:
            points = slot_chosing(card, names)

    def pressing(card):
        user = card.current_fighter
        escalation = user.escalation
        points = user.fight.points[user.side]
        points_value = [i.value for k, i in points.items() if k != 'excellence']
        max_slot = max(points_value)
        max_point = points.values()[points_value.index(max_slot)]
        if escalation < max_slot:
            max_point.value -= escalation
        points['excellence'].value += escalation+2

    def tactical(card):
        user = card.current_fighter
        user.draw(2)
        if user.side == 'allies':
            card.blocked = True
            renpy.show_screen('sc_chose_drop', user)
        else:
            for i in range(2):
                try:
                    card = rand.choice(user.hand.cards_list)
                except IndexError:
                    return
                user.drop_card(card)
    #power mods
    def buildup(card):
        user = card.current_fighter
        value = len([i for i in user.drop if i.power > 0])
        return value

    def aggravating(card):
        user = card.current_fighter
        points = fight.points[user.side][card.slot]
        value = 0
        for i in user.drop:
            if i.id == card.id:
                value += i.power
        return value


    special_mechanics = {
        'power_calculators':{},
        'card_draw':[combo, advantage, tactical],

    }


    
    # available keys for actions
    # {id: name, rarity, power=0, use_weapon=False, mighty=False, slot=None, special_effect=None, unique=False, style=None}
    # slot is one of 'onslaught', 'maneuver', 'fortitude', 'excellence'
    # special_effect must be function which take 1 arg, excepted arg is DuelCombatant who used card
    # style is one of 'breter', 'juggernaut', 'shieldbearer', 'restler', 'beast'

    actions_lib = {'clinch': {'name': __('clinch'), 'rarity': 'common', 'power': 0, 'special_effect': clinch_special, 'on_remove': clinch_remove, 'description': 'Persistent effect. The maneuver do not scores for both combatants while clinch is in the game.', },
                    'hit_n_run': {'name': __('hit-n-run'), 'rarity': 'common', 'power': 0, 'special_effect': hit_n_run_special, 'on_remove': hit_n_run_remove, 'description': 'Persistent effect. The onslaught do not scores for both combatants while hit-n-run is in the game.', },
                    'rage': {'name': __('rage'), 'rarity': 'common', 'power': 0, 'special_effect': rage_special, 'on_remove': rage_remove, 'description': 'Persistent effect. The fortitude do not scores for both combatants while rage is in the game.', },
                    'outsmart': {'name': __('outsmart'), 'rarity': 'common', 'power': 0, 'special_effect': outsmart_special, 'description': 'Discards all persistent effects.', },
                    'fallback': {'name': __('fallback'), 'rarity': 'common', 'power': 0, 'special_effect': fallback_special, 'description': 'Deduct your current escalation from your biggest basic point-pool. Get one new card.', },
                    
                    'puny_strike': {'name': __('puny strike'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#ff0000}Weapon attack{/color}', 'special_effect': None},
                    'draggle': {'name': __('draggle'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#ff0000}Weapon feint{/color}',  'special_effect': None},
                    'desperation': {'name': __('desperation'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#ff0000}Weapon defence{/color}',  'special_effect': None},
                    
                    'light_strike': {'name': __('light strike'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#ff00ff}Weapon attack{/color}',  'special_effect': None},
                    'move': {'name': __('move'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#ff00ff}Weapon feint{/color}',  'special_effect': None},
                    'rebound': {'name': __('rebound'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#ff00ff}Weapon defence{/color}',  'special_effect': None},

                    'strike': {'name': __('strike'), 'rarity': 'common', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#00ffff}Weapon attack{/color}',  'special_effect': None},
                    'dash': {'name': __('dash'), 'rarity': 'common', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#00ffff}Weapon feint{/color}',  'special_effect': None},
                    'block': {'name': __('block'), 'rarity': 'common', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#00ffff}Weapon defence{/color}',  'special_effect': None},
                    
                    'hard_strike': {'name': __('hard strike'), 'rarity': 'common', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#0000ff}Weapon attack{/color}',  'special_effect': None},
                    'fast_dash': {'name': __('fast dash'), 'rarity': 'common', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#0000ff}Weapon feint{/color}',  'special_effect': None},
                    'hard_block': {'name': __('hard block'), 'rarity': 'common', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#0000ff}Weapon defence{/color}',  'special_effect': None},
                    
                    'powerful_strike': {'name': __('powerful strike'), 'rarity': 'common', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#008000}Weapon attack{/color}',  'special_effect': None},
                    'lightning_dash': {'name': __('lightning dash'), 'rarity': 'common', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#008000}Weapon feint{/color}',  'special_effect': None},
                    'powerful_block': {'name': __('powerful block'), 'rarity': 'common', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#008000}Weapon defence{/color}',  'special_effect': None},
                    
                    'bite': {'name': __('bite'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#00ffff}Unarmed attack{/color}',  'special_effect': None},
                    'headbutt': {'name': __('headbutt'), 'rarity': 'common', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#0000ff}Unarmed attack{/color}',  'special_effect': None},
                    'kick': {'name': __('kick'), 'rarity': 'common', 'power': 4, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#008000}Unarmed attack{/color}',  'special_effect': None},
                    'vicious_bite': {'name': __('vicious_bite'), 'rarity': 'common', 'power': 5, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': '{color=#D4A017}Unarmed attack{/color}',  'special_effect': None},
                    
                    'recoil': {'name': __('recoil'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#00ffff}Unarmed feint{/color}',  'special_effect': None},
                    'dodge': {'name': __('dodge'), 'rarity': 'common', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot': 'maneuver', 'description': '{color=#0000ff}Unarmed feint{/color}',  'special_effect': None},
                    
                    'deep_breath': {'name': __('deep breath'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#00ffff}Unarmed defence{/color}',  'special_effect': None},
                    'caution': {'name': __('caution'), 'rarity': 'common', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot':  'fortitude', 'description': '{color=#0000ff}Unarmed defence{/color}',  'special_effect': None},
                    
                    'name': {'name': __('name'), 'rarity': 'common', 'power': 0, 'use_weapon': False, 'mighty': False, 'slot': 'onslaught', 'description': 'описалово',  'special_effect': None},
                    'test1': {'name': __('test1'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'slot': 'onslaught', 'description': 'описалово', 'special_effect': None, 'power_mods': [buildup], 'special_mechanics': [pressing, amplifiction]}

                    
}

screen draw_from_drop(user, text, func):
    modal True
    vbox:
        align(0.6, 0.7)
        text '%s:'%text
        for c in user.draw_list():
            textbutton c.name:
                action Function(func, c), Function(user.fight.send_event, user), Hide('draw_from_drop')

screen sc_chose_slot(card, user, names):
    modal True
    vbox:
        align(0.6, 0.7)
        for name in names:
            textbutton name:
                action Function(use_slot, card, name), Function(user.fight.send_event, user), Hide('sc_chose_slot')
init python:
    sc_chose_drop_dropped = []
    def make_empty(list_):
        copy = [i for i in list_]
        for i in copy:
            try:
                list_.remove(i)
            except ValueError:
                pass
screen sc_chose_drop(user):
    modal True
    vbox:
        align(0.6, 0.7)
        text 'drop card'
        for i in user.hand:
            textbutton i.name:
                action [Function(user.drop_card, i), AddToSet(sc_chose_drop_dropped, i),
                    If(len(sc_chose_drop_dropped) > 0, true=Hide('sc_chose_drop')),
                    If(len(sc_chose_drop_dropped) > 0, true=Function(user.fight.send_event, user)),
                    If(len(sc_chose_drop_dropped) > 0, true=Function(make_empty, sc_chose_drop_dropped))]