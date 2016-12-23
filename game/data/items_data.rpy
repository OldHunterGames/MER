init python:
    # sizes ['offhand', 'versatile', 'shield', 'twohand']
    weapon_data = {
        'shield':{'name': __('shield'), 'size': 'shield', 'damage_type': 'subdual', 'quality': 3},    
        'knife':{'name': __('knife'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 2},
        'dagger':{'name': __('dagger'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 3},
        'sdw':{'name': __('sdw'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 3},
        'crowbar': {'name': __('crowbar'),'size': 'versatile', 'damage_type': 'impact', 'quality': 2},
        'maul': {'name': __('maul'),'size': 'versatile', 'damage_type': 'impact', 'quality': 3},
        'club': {'name': __('club'),'size': 'versatile', 'damage_type': 'subdual', 'quality': 3},
        'quarterstaff': {'name': __('quarterstaff'),'size': 'twohand', 'damage_type': 'subdual', 'quality': 3},
        'letal_weapon': {'name': __('letal weapon'),'size': 'versatile', 'damage_type': 'impact', 'quality': 3},
        'long_weapon': {'name': __('long weapon'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 3},
        'sword': {'name': __('sword'),'size': 'versatile', 'damage_type': 'slashing', 'quality': 3},
        'hand_axe':{'name': __('hand axe'),'size': 'versatile', 'damage_type': 'slashing', 'quality': 2},
        'hunting_weapon': {'name': __('hunting weapon'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 2},
        'pickaxe': {'name': __('pickaxe'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 2},
        'strudy_axe':{'name': __('strudy axe'),'size': 'twohand', 'damage_type': 'slashing', 'quality': 2},
        'rusty_axe':{'name': __('rusty axe'),'size': 'twohand', 'damage_type': 'slashing', 'quality': 1},
        'rusty_knife':{'name': __('rusty knife'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 1},
        'knuckles':{'name': __('knuckles'), 'size': 'offhand', 'damage_type': 'subdual', 'quality': 1},            
        'lancet':{'name': __('lancet'), 'size': 'offhand', 'damage_type': 'slashing', 'quality': 1}
        }

    
    armor_data = {
        'hard_armor': {'name': __('hard armor'), 'armor_rate': 'heavy_armor', 'quality': 3},
        'soft_armor': {'name': __('soft armor'), 'armor_rate': 'light_armor', 'quality': 3},            
        'leather_coat': {'name': __('soft armor'), 'armor_rate': 'light_armor', 'quality': 2},  
        'bad_plate': {'name': __('bad plate'), 'armor_rate': 'heavy_armor', 'quality': 1},
            }


    treasure_data = {
        'diamond':{
            'name': __("diamond"),
            'description': __('diamond'),
            'price': 5,
            'mutable_name': False,
            'mutable_description': False
        }
    }