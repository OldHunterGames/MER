init python:
    sys.path.append(renpy.loader.transfn("Core/DuelEngine/scripts"))
    import random as rand

    from duel_engine import DuelAction
    def make_inactive(battlepoints_list):
        for point in battlepoints_list:
            point.active = False
    def clinch_special(user):
        battle_points = [value['maneuver'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    def hit_n_run_special(user):
        battle_points = [value['onslaught'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    def rage_special(user):
        battle_points = [value['fortitude'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    def outsmart_special(user):
        for value in user.fight.points.values():
            for i in value:
                value[i].active = True
    def fallback_special(user):
        if len(user.drop) < 2:
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
            card = renpy.show_screen('draw_from_drop', user)
        else:
            card = rand.choice(user.drop)
        user.draw_from_drop(card)
    
    # available keys for actions
    # {id: name, rarity, power=0, use_weapon=False, mighty=False, slot=None, special_effect=None, unique=False, style=None}
    # slot is one of 'onslaught', 'maneuver', 'fortitude', 'excellence'
    # special_effect must be function which take 1 arg, excepted arg is DuelCombatant who used card
    # style is one of 'breter', 'juggernaut', 'shieldbearer', 'restler', 'beast'
<<<<<<< HEAD
    actions_lib = {'clinch': {'name': __('clinch'), 'rarity': 'common', 'power': 0, 'special_effect': clinch_special},
                    'hit_n_run': {'name': __('hit n run'), 'rarity': 'common', 'power': 0, 'special_effect': hit_n_run_special},
                    'rage': {'name': __('rage'), 'rarity': 'common', 'power': 0, 'special_effect': rage_special},
                    'outsmart': {'name': __('outsmart'), 'rarity': 'common', 'power': 0, 'special_effect': outsmart_special},
                    'fallback': {'name': __('fallback'), 'rarity': 'common', 'power': 0, 'special_effect': fallback_special},
                    'puny_strike': {'name': __('puny strike'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'special_effect': None},
                    'draggle': {'name': __('draggle'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'special_effect': None},
                    'desperation': {'name': __('desperation'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'special_effect': None},
                    'light_strike': {'name': __('light strike'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'special_effect': None},
                    'move': {'name': __('move'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'special_effect': None},
                    'rebound': {'name': __('rebound'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'special_effect': None},
=======
    actions_lib = {'clinch': {'name': __('clinch'), 'rarity': 'common', 'power': 0, 'special_effect': clinch_special, 'description': 'описалово', },
                    'hit_n_run': {'name': __('hit n run'), 'rarity': 'common', 'power': 0, 'special_effect': hit_n_run_special 'description': 'описалово', },
                    'rage': {'name': __('rage'), 'rarity': 'common', 'power': 0, 'special_effect': rage_special 'description': 'описалово', },
                    'outsmart': {'name': __('outsmart'), 'rarity': 'common', 'power': 0, 'special_effect': rage_special 'description': 'описалово', },
                    'fallback': {'name': __('fallback'), 'rarity': 'common', 'power': 0, 'special_effect': fallback_special 'description': 'описалово', },
                    'puny_strike': {'name': __('puny strike'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово', 'special_effect': None},
                    'draggle': {'name': __('draggle'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    'desperation': {'name': __('desperation'), 'rarity': 'common', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
                    'light_strike': {'name': __('light strike'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'move': {'name': __('move'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    'rebound': {'name': __('rebound'), 'rarity': 'common', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
>>>>>>> origin/master

                    'strike': {'name': __('strike'), 'rarity': 'common', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'dash': {'name': __('dash'), 'rarity': 'common', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    'block': {'name': __('block'), 'rarity': 'common', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
                    
                    'hard_strike': {'name': __('hard strike'), 'rarity': 'common', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'fast_dash': {'name': __('fast dash'), 'rarity': 'common', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    'hard_block': {'name': __('hard block'), 'rarity': 'common', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
                    
                    'powerful_strike': {'name': __('powerful strike'), 'rarity': 'common', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'lightning_dash': {'name': __('lightning dash'), 'rarity': 'common', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    'powerful_block': {'name': __('powerful block'), 'rarity': 'common', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
                    
                    'bite': {'name': __('bite'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'headbutt': {'name': __('headbutt'), 'rarity': 'common', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'kick': {'name': __('kick'), 'rarity': 'common', 'power': 4, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    'vicious_bite': {'name': __('vicious_bite'), 'rarity': 'common', 'power': 5, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': 'описалово',  'special_effect': None},
                    
                    'recoil': {'name': __('recoil'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    'dodge': {'name': __('dodge'), 'rarity': 'common', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot': 'maneuver', 'description': 'описалово',  'special_effect': None},
                    
                    'deep_breath': {'name': __('deep breath'), 'rarity': 'common', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
                    'caution': {'name': __('caution'), 'rarity': 'common', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot':  'fortitude', 'description': 'описалово',  'special_effect': None},
                    
                    'name': {'name': __('name'), 'rarity': 'common', 'power': 0, 'use_weapon': False, 'mighty': False, 'slot': 'onslaught', 'description': 'описалово',  'special_effect': None},

                    
}

screen draw_from_drop(user):
    vbox:
        align(0.6, 0.7)
        text 'draw_card:'
        for c in user.drop:
            if c != user.drop[-1]:
                textbutton c.name:
                    action Function(user.draw_from_drop, card), Hide('draw_from_drop')