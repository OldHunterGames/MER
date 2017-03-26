init python:
    # sizes ['offhand', 'versatile', 'shield', 'twohand']
    weapon_data = {
        'bare_hands': {'name': __('bare hands'), 'size': 'offhand', 'damage_type': 'subdual', 'quality': 0, 'price': -1}        
        'stone_knife':{'name': __('stone knife'), 'size': 'offhand', 'damage_type': 'piercing', 'mutable_name': False, 'quality': 2, 'price': 1},
        'stone_spear': {'name': __('stone spear'),'size': 'twohand', 'damage_type': 'piercing', 'quality': 2, 'price': 3},
        'heavy_axe': {'name': __('long axe'),'size': 'twohand', 'damage_type': 'slashing', 'quality': 3, 'price': 10},
        'dagger':{'name': __('dagger'), 'size': 'offhand', 'damage_type': 'piercing', 'quality': 4, 'price': 5},
        'smallsword': {'name': __('smallsword'),'size': 'versatile', 'damage_type': 'piercing', 'quality': 3, 'price': 5},
        'sword': {'name': __('sword'),'size': 'versatile', 'damage_type': 'slashing', 'quality': 4, 'price': 10},
        'sabre': {'name': __('sabre'),'size': 'versatile', 'damage_type': 'slashing', 'quality': 4, 'price': 10},
        'shield':{'name': __('shield'), 'size': 'shield', 'damage_type': 'subdual', 'quality': 3, 'price': 10},    
        'knife':{'name': __('knife'), 'size': 'offhand', 'damage_type': 'piercing', 'mutable_name': False, 'quality': 2, 'price': 3},

        'quarterstaff': {'name': __('quarterstaff'),'size': 'twohand', 'damage_type': 'subdual', 'quality': 3, 'price': 2},

        }

    
    armor_data = {
        'nude': {'name': __('nude'), 'armor_rate': 'unarmored', 'quality': 0, 'price': -1}
        'hides': {'name': __('hides'), 'armor_rate': 'light_armor', 'quality': 1, 'price': 3},   
        'loincloth': {'name': __('loincloth'), 'armor_rate': 'unarmored', 'quality': 1, 'price': 1},            
        'rags': {'name': __('rags'), 'armor_rate': 'unarmored', 'quality': 1, 'price': 1},  
        'simple_clothes': {'name': __('simple clothes'), 'armor_rate': 'unarmored', 'quality': 2, 'price': 3},  
        'fine_clothes': {'name': __('fine clothes'), 'armor_rate': 'unarmored', 'quality': 3, 'price': 5},  
        'luxury_clothes': {'name': __('luxury clothes'), 'armor_rate': 'unarmored', 'quality': 4, 'price': 10},          
        'fullplate': {'name': __('fullplate armor'), 'armor_rate': 'heavy_armor', 'quality': 4, 'price': 50},
        'body_armor': {'name': __('polymer armor'), 'armor_rate': 'light_armor', 'quality': 4, 'price': 20},  

        'hard_armor': {'name': __('hard armor'), 'armor_rate': 'heavy_armor', 'quality': 3, 'price': 2},
        'soft_armor': {'name': __('soft armor'), 'armor_rate': 'light_armor', 'quality': 3, 'price': 2},            
        'leather_coat': {'name': __('soft armor'), 'armor_rate': 'light_armor', 'quality': 2, 'price': 1},  
        'bad_plate': {'name': __('bad plate'), 'armor_rate': 'heavy_armor', 'quality': 1},
            }

    assesories_data = {
        'jewel':{
            'name': __("jewel"),
            'description': __('This piece of jewelry contains a clear gem, suited to store the Sparks.'),
            'price': 10,
            'mutable_name': True,
            'mutable_description': False
        },
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
