init python:
    actions_lib = {'clinch': {'name': __('clinch'), 'rarity': 'base', 'power': 0, 'special_mechanics': [clinch_special], 'on_remove': clinch_remove, 'description': __('Persistent effect. The maneuver do not scores for both combatants while clinch is in the game.'), },
                    'hit_n_run': {'name': __('hit-n-run'), 'rarity': 'base', 'power': 0, 'special_mechanics': [hit_n_run_special], 'on_remove': hit_n_run_remove, 'description': __('Persistent effect. The onslaught do not scores for both combatants while hit-n-run is in the game.'), },
                    'rage': {'name': __('rage'), 'rarity': 'base', 'power': 0, 'special_mechanics': [rage_special], 'on_remove': rage_remove, 'description': __('Persistent effect. The fortitude do not scores for both combatants while rage is in the game.'), },
                    'outsmart': {'name': __('outsmart'), 'rarity': 'base', 'power': 0, 'special_mechanics': [outsmart_special], 'description': __('Discards all persistent effects.'), },
                    'fallback': {'name': __('fallback'), 'rarity': 'base', 'power': 0, 'special_mechanics': [fallback_special], 'description': __('Deduct your current escalation from your biggest basic point-pool. Get one new card.'), },
                    'initiative': {'name': __('initiative'), 'rarity': 'base', 'power': 0, 'special_mechanics': [initiative_special], 'on_remove': initiative_remove, 'description': __('')},
                    'fatigue': {'name': __('fatigue'), 'rarity': 'base', 'power': 0, 'special_mechanics': [fatigue_special], 'description': __('')},

                    'desperate_strike': {'name': __('puny strike'), 'rarity': 'base', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#ff0000}Weapon attack{/color}')},
                    'desperate_move': {'name': __('draggle'), 'rarity': 'base', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#ff0000}Weapon feint{/color}')},
                    'desperate_block': {'name': __('desperation'), 'rarity': 'base', 'power': 0, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#ff0000}Weapon defence{/color}')},
                    
                    'simple_strike': {'name': __('light strike'), 'rarity': 'base', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#ff00ff}Weapon attack{/color}')},
                    'simple_move': {'name': __('move'), 'rarity': 'base', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#ff00ff}Weapon feint{/color}')},
                    'simple_block': {'name': __('rebound'), 'rarity': 'base', 'power': 1, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#ff00ff}Weapon defence{/color}')},

                    'strike': {'name': __('strike'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#00ffff}Weapon attack{/color}')},
                    'move': {'name': __('dash'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#00ffff}Weapon feint{/color}')},
                    'block': {'name': __('block'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#00ffff}Weapon defence{/color}')},
                    
                    'tricky_strike': {'name': __('hard strike'), 'rarity': 'base', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#0000ff}Weapon attack{/color}')},
                    'tricky_move': {'name': __('fast dash'), 'rarity': 'base', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#0000ff}Weapon feint{/color}')},
                    'tricky_block': {'name': __('hard block'), 'rarity': 'base', 'power': 3, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#0000ff}Weapon defence{/color}')},
                    
                    'great_strike': {'name': __('powerful strike'), 'rarity': 'base', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#008000}Weapon attack{/color}')},
                    'great_move': {'name': __('lightning dash'), 'rarity': 'base', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#008000}Weapon feint{/color}')},
                    'great_block': {'name': __('powerful block'), 'rarity': 'base', 'power': 4, 'use_weapon': True, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#008000}Weapon defence{/color}')},
                    
                    'bite': {'name': __('bite'), 'rarity': 'base', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#00ffff}Unarmed attack{/color}')},
                    'headbutt': {'name': __('headbutt'), 'rarity': 'base', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#0000ff}Unarmed attack{/color}')},
                    'kick': {'name': __('kick'), 'rarity': 'base', 'power': 4, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#008000}Unarmed attack{/color}')},
                    'vicious_bite': {'name': __('vicious_bite'), 'rarity': 'base', 'power': 5, 'use_weapon': False, 'mighty': False, 'slot':  'onslaught', 'description': __('{color=#D4A017}Unarmed attack{/color}')},
                    
                    'recoil': {'name': __('recoil'), 'rarity': 'base', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#00ffff}Unarmed feint{/color}')},
                    'dodge': {'name': __('dodge'), 'rarity': 'base', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot': 'maneuver', 'description': __('{color=#0000ff}Unarmed feint{/color}')},
                    
                    'deep_breath': {'name': __('deep breath'), 'rarity': 'base', 'power': 2, 'use_weapon': False, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#00ffff}Unarmed defence{/color}')},
                    'caution': {'name': __('caution'), 'rarity': 'base', 'power': 3, 'use_weapon': False, 'mighty': False, 'slot':  'fortitude', 'description': __('{color=#0000ff}Unarmed defence{/color}')},

                    'follow_up': {'name': __('follow up'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'slot': 'maneuver', 'description': __('{color=#00ffff}Weapon feint{/color} \nCombo - choose one card with power 1 or more from your used cards pile and play it immediately.'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [combo]},
                    'flurry': {'name': __('flurry'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'slot': 'maneuver', 'description': __('{color=#00ffff}Weapon feint{/color} \nSequence - play all flurry card from your hand and deck at once.'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [sequence]},

                    'battering_strike': {'name': __('battering strike'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'slot': 'onslaught', 'description': __('{color=#ff00ff}Weapon attack{/color} \nAggravating - adds power of each battering strike in your used cards pile.'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [aggravating]},
                    'rampage': {'name': __('rampage'), 'rarity': 'base', 'power': 2, 'use_weapon': True, 'slot': 'onslaught', 'description': __('{color=#00ffff}Weapon attack{/color} \nAmplificate onslaught - double your onslaught victory points.'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [amplifiction]},

                    'second_thought': {'name': __('second thought'), 'rarity': 'base', 'power': 3, 'use_weapon': True, 'slot': 'fortitude', 'description': __('{color=#00ffff}Weapon defence{/color} \nTactical - draw two cards then discard two cards of your choice.'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [tactical]} ,                   
                    'stability': {'name': __('stability'), 'rarity': 'base', 'power': 4, 'use_weapon': False, 'slot': 'fortitude', 'description': __('{color=#D4A017}Unarmed defence{/color} \nPressing - diminish your top basic victory points pool by your escalation, then add escalation + 2 points to your excellence pool.'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [pressing]},                   

                    'savage_force': {'name': __('savage force'), 'rarity': 'base', 'power': 3, 'use_weapon': True, 'slot': 'onslaught', 'description': __('{color=#0000ff}Weapon action{/color} \nVersatile - chose common victory points slot to add this cards power'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [versatile]},                    
                    'frenzy': {'name': __('frenzy'), 'rarity': 'base', 'power': 1, 'use_weapon': True, 'slot': 'onslaught', 'description': __('{color=#ff00ff}Weapon attack{/color} \nBuildup - add number of power cards in your used cards pile to this cards power.'), 'combat_style': None, 'tag': None, 'power_mods': [buildup], 'special_mechanics': None},                    


                    
                    'test': {'name': __('test'), 'rarity': 'base', 'power': 2, 'use_weapon': False, 'slot': 'onslaught', 'description': __('описалово'), 'combat_style': None, 'tag': None, 'power_mods': None, 'special_mechanics': [combo, sequence, amplifiction, advantage]},                    
}
