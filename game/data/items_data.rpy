init python:
    # sizes ['offhand', 'versatile', 'shield', 'twohand']
    weapon_data = {
        'shield':{'name': __('shield'), 'size': 'shield', 'damage_type': 'subdual', 'quality': 3, 'price': 2},    
        'knife':{'name': __('knife'), 'size': 'offhand', 'damage_type': 'piercing', 'mutable_name': False, 'quality': 2, 'price': 1},
        'dagger':{'name': __('dagger'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 3, 'price': 2},
        'sdw':{'name': __('SDW'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 3, 'price': 2},
        'crowbar': {'name': __('crowbar'),'size': 'versatile', 'damage_type': 'impact', 'quality': 2, 'price': 1},
        'maul': {'name': __('maul'),'size': 'versatile', 'damage_type': 'impact', 'quality': 3, 'price': 2},
        'club': {'name': __('club'),'size': 'versatile', 'damage_type': 'subdual', 'quality': 3, 'price': 2},
        'quarterstaff': {'name': __('quarterstaff'),'size': 'twohand', 'damage_type': 'subdual', 'quality': 3, 'price': 2},
        'letal_weapon': {'name': __('letal weapon'),'size': 'versatile', 'damage_type': 'impact', 'quality': 3, 'price': 2},
        'long_weapon': {'name': __('long weapon'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 3, 'price': 2},
        'sword': {'name': __('sword'),'size': 'versatile', 'damage_type': 'slashing', 'quality': 3, 'price': 2},
        'hand_axe':{'name': __('hand axe'),'size': 'versatile', 'damage_type': 'slashing', 'quality': 2, 'price': 1},
        'hunting_weapon': {'name': __('hunting weapon'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 2, 'price': 1},
        'pickaxe': {'name': __('pickaxe'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 2, 'price': 1},
        'strudy_axe':{'name': __('strudy axe'),'size': 'twohand', 'damage_type': 'slashing', 'quality': 2, 'price': 1},
        'rusty_axe':{'name': __('rusty axe'),'size': 'twohand', 'damage_type': 'slashing', 'quality': 1, 'price': 0},
        'rusty_knife':{'name': __('rusty knife'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 1, 'price': 0},
        'knuckles':{'name': __('knuckles'), 'size': 'offhand', 'damage_type': 'subdual', 'quality': 1, 'price': 0},            
        'lancet':{'name': __('lancet'), 'size': 'offhand', 'damage_type': 'slashing', 'quality': 1, 'price': 0},
        'bare_hands': {'name': __('bare hands'), 'size': 'offhand', 'damage_type': 'subdual', 'quality': 1, 'price': -1}
        }

    
    armor_data = {
        'hard_armor': {'name': __('hard armor'), 'armor_rate': 'heavy_armor', 'quality': 3, 'price': 2},
        'soft_armor': {'name': __('soft armor'), 'armor_rate': 'light_armor', 'quality': 3, 'price': 2},            
        'leather_coat': {'name': __('soft armor'), 'armor_rate': 'light_armor', 'quality': 2, 'price': 1},  
        'bad_plate': {'name': __('bad plate'), 'armor_rate': 'heavy_armor', 'quality': 1},
        'nude': {'name': __('nude'), 'armor_rate': 'light_armor', 'quality': 1, 'price': -1}
            }


    treasure_data = {
        'gem':{
            'name': __("clear gem"),
            'description': __('Clear crystal, suited to store the Sparks.'),
            'price': 1,
            'mutable_name': False,
            'mutable_description': False
        },
        'sparkgem':{
            'name': __("clear gem"),
            'description': __('Shiny gem, filled with Sparks.'),
            'price': 1,
            'mutable_name': False,
            'mutable_description': False
        },
        'navigem':{
            'name': __("clear gem"),
            'description': __('This shiny gem contains a vision of Outer World.'),
            'price': 1,
            'mutable_name': False,
            'mutable_description': False
        },
        'notes':{
            'name': __("bundle of notes"),
            'description': __("It's a papper money emmited by a Noble House of Eternal Rome."),
            'price': 4,
            'mutable_name': False,
            'mutable_description': False
        },        
    }
