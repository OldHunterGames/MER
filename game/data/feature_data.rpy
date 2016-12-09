init python:
    person_features = {
        # base
        'junior': {'name': __('junior'), 'slot': 'age', 'modifiers': {'physique': -1, 'spirit': -1, 'mind': -1, 'sensitivity': +1}, 'visible': True},
        'adolescent': {'name': __('adolescent'), 'slot': 'age', 'modifiers': {}, 'visible': True},
        'mature': {'name': __('mature'), 'slot': 'age', 'modifiers': {'spirit': +1}, 'visible': True},
        'elder': {'name': __('elder'), 'slot': 'age', 'modifiers': {'agility': -1, 'mind': +1}, 'visible': True},

        'sexless': {'name': __('sexless'), 'slot': 'gender', 'modifiers': {}, 'visible': True},
        'male': {'name': __('male'), 'slot': 'gender', 'modifiers': {'physique': +1, 'sensitivity': -1}, 'visible': True},
        'female': {'name': __('female'), 'slot': 'gender', 'modifiers': {'physique': -1, 'sensitivity': +1}, 'visible': True},
        'shemale': {'name': __('shemale'), 'slot': 'gender', 'modifiers': {}, 'visible': True},

        'brawny': {'name': __('brawny'), 'slot': 'constitution', 'modifiers': {'agility': -1, 'physique': +1}, 'visible': True},
        'large': {'name': __('large'), 'slot': 'constitution', 'modifiers': {'physique': +1}, 'visible': True},
        'athletic': {'name': __('athletic'), 'slot': 'constitution', 'modifiers': {'agility': +1, 'physique': +1}, 'visible': True},
        'small': {'name': __('small'), 'slot': 'constitution', 'modifiers': {'physique': -1}, 'visible': True},
        'lean': {'name': __('lean'), 'slot': 'constitution', 'modifiers': {'agility': +1, 'physique': -1}, 'visible': True},
        'crooked': {'name': __('crooked'), 'slot': 'constitution', 'modifiers': {'agility': -1, 'physique': -1}, 'visible': True},
        'clumsy': {'name': __('clumsy'), 'slot': 'constitution', 'modifiers': {'agility': -1}, 'visible': True},

        'brave': {'name': __('brave'), 'slot': 'spirit_feat', 'modifiers': {'spirit': +1}, 'visible': True},
        'shy': {'name': __('shy'), 'slot': 'spirit_feat', 'modifiers': {'spirit': -1}, 'visible': True},
        'smart': {'name': __('smart'), 'slot': 'mind_feat', 'modifiers': {'mind': +1}, 'visible': True},
        'dumb': {'name': __('dumb'), 'slot': 'mind_feat', 'modifiers': {'mind': -1}, 'visible': True},
        'sensitive': {'name': __('sensitive'), 'slot': 'sensitivity_feat', 'modifiers': {'sensitivity': +1}, 'visible': True},
        'cool': {'name': __('cool'), 'slot': 'sensitivity_feat', 'modifiers': {'sensitivity': -1}, 'visible': True},
        
        # look
        'innocent_appearence': {'name': __('innocent appearence'), 'slot': 'look', 'visible': True},        
        'bold_appearence': {'name': __('bold appearence'), 'slot': 'look', 'visible': True},    
        'foxy_appearence': {'name': __('foxy appearence'), 'slot': 'look', 'visible': True},    
        'gentle_appearence': {'name': __('gentle appearence'), 'slot': 'look', 'visible': True},        
        'calm_appearence': {'name': __('calm appearence'), 'slot': 'look', 'visible': True},    
        'exotic_appearence': {'name': __('exotic appearence'), 'slot': 'look', 'visible': True},                    
        'straight_appearence': {'name': __('straight appearence'), 'slot': 'look', 'visible': True},        
        'sleasy_appearence': {'name': __('sleasy appearence'), 'slot': 'look', 'visible': True},    
        'wild_appearence': {'name': __('wild appearence'), 'slot': 'look', 'visible': True},    

        # anatomy
        'flat_chest': {'name': __('flat chest'), 'slot': 'breast_size', 'modifiers': {'appearance_boobs': 0}, 'visible': True},
        'small_breast': {'name': __('small breast'), 'slot': 'breast_size','modifiers': {'appearance_boobs': 1},  'visible': True},
        'normal_breast': {'name': __('normal breast'), 'slot': 'breast_size','modifiers': {'appearance_boobs': 2},  'visible': True},
        'large_boobs': {'name': __('large breast'), 'slot': 'breast_size','modifiers': {'appearance_boobs': 3},  'visible': True},
        'huge_tits': {'name': __('huge tits'), 'slot': 'breast_size','modifiers': {'appearance_boobs': 4},  'visible': True},
        'enormous_udders': {'name': __('enormous udders'), 'slot': 'breast_size','modifiers': {'appearance_boobs': 5},  'visible': True},

        'small_penis': {'name': __('small_penis'), 'slot': 'penis_size', 'visible': True},
        'normal_penis': {'name': __('normal_penis'), 'slot': 'penis_size', 'visible': True},
        'large_penis': {'name': __('large_penis'), 'slot': 'penis_size', 'visible': True},

        'human_penis': {'name': __('human_penis'), 'slot': 'penis_type', 'visible': True},
        'canine_penis': {'name': __('canine_penis'), 'slot': 'penis_type', 'visible': True},

        # needs
        'greedy': {'name': __('greedy'), 'slot': 'prosperity_feat', 'modifiers': {'prosperity': +1}, 'visible': True},
        'generous': {'name': __('generous'), 'slot': 'prosperity_feat', 'modifiers': {'prosperity': -1}, 'visible': True},
        'gourmet': {'name': __('gourmet'), 'slot': 'nutrition_feat', 'modifiers': {'nutrition': +1}, 'visible': True},
        'moderate_eater': {'name': __('moderate_eater'), 'slot': 'nutrition_feat', 'modifiers': {'nutrition': -1}, 'visible': True},
        'low_pain_threshold': {'name': __('low_pain_threshold'), 'slot': 'wellness_feat', 'modifiers': {'wellness': +1}, 'visible': True},
        'high_pain_threshold': {'name': __('high_pain_threshold'), 'slot': 'wellness_feat', 'modifiers': {'wellness': -1}, 'visible': True},
        'sybarite': {'name': __('sybarite'), 'slot': 'comfort_feat', 'modifiers': {'comfort': +1}, 'visible': True},
        'ascetic': {'name': __('ascetic'), 'slot': 'comfort_feat', 'modifiers': {'comfort': -1}, 'visible': True},
        'energetic': {'name': __('energetic'), 'slot': 'activity_feat', 'modifiers': {'activity': +1}, 'visible': True},
        'lazy': {'name': __('lazy'), 'slot': 'activity_feat', 'modifiers': {'activity': -1}, 'visible': True},
        'extrovert': {'name': __('extrovert'), 'slot': 'communication_feat', 'modifiers': {'communication': +1}, 'visible': True},
        'introvert': {'name': __('introvert'), 'slot': 'communication_feat', 'modifiers': {'communication': -1}, 'visible': True},
        'curious': {'name': __('curious'), 'slot': 'amusement_feat', 'modifiers': {'amusement': +1}, 'visible': True},
        'dull': {'name': __('dull'), 'slot': 'amusement_feat', 'modifiers': {'amusement': -1}, 'visible': True},
        'dominant': {'name': __('dominant'), 'slot': 'authority_feat', 'modifiers': {'authority': +1}, 'visible': True},
        'submissive': {'name': __('submissive'), 'slot': 'authority_feat', 'modifiers': {'authority': -1}, 'visible': True},
        'ambitious': {'name': __('ambitious'), 'slot': 'ambition_feat', 'modifiers': {'ambition': +1}, 'visible': True},
        'modest': {'name': __('modest'), 'slot': 'ambition_feat', 'modifiers': {'ambition': -1}, 'visible': True},
        'lewd': {'name': __('lewd'), 'slot': 'eros_feat', 'modifiers': {'eros': +1}, 'visible': True},
        'frigid': {'name': __('frigid'), 'slot': 'eros_feat', 'modifiers': {'eros': -1}, 'visible': True},

        # nutrition
        'slim': {'name': __('slim'), 'slot': 'shape', 'modifiers': {'nutrition': 1}, 'visible': True, 'value': 1},
        'emaciated': {'name': __('emaciated'), 'slot': 'shape', 'modifiers': {'nutrition': 2, 'vitality': -1}, 'visible': True, 'value': 2},
        'chubby': {'name': __('chubby'), 'slot': 'shape', 'modifiers': {'nutrition': -1}, 'visible': True, 'value': -1},
        'obese': {'name': __('obese'), 'slot': 'shape', 'modifiers': {'nutrition': -1, 'vitality': -1}, 'visible': True, 'value': -1},
        'starving': {'name': __('starving'), 'slot': None, 'modifiers': {'physique': -1}, 'visible': True},
        'dyspnoea': {'name': __('dyspnoea'), 'visible': True},
        'diabetes': {'name': __('diabetes'), 'modifiers': {'vitality': -1}, 'visible': False},

        # fitness
        'tender': {'name': __('brawny'), 'slot': 'fitness', 'modifiers': {'vitality': -1, 'physique': -1}, 'visible': True},
        'fit': {'name': __('brawny'), 'slot': 'fitness', 'modifiers': {'agility': +1, 'vitality': +1}, 'visible': True},
        'beefy': {'name': __('brawny'), 'slot': 'fitness', 'modifiers': {'physique': +1, 'agility': -1}, 'visible': True},
        'muscular': {'name': __('brawny'), 'slot': 'fitness', 'modifiers': {'vitality': +1, 'physique': +1}, 'visible': True},

        'dead': {'name': __('dead'), 'visible': True},
    }

    item_features = {
        'offhand': {'name': __('offhand weapon'), 'slot': 'wpn_size', 'visible': True},
        'versatile': {'name': __('weapon'), 'slot': 'wpn_size', 'visible': True},
        'twohand': {'name': __('twohanded weapon'), 'slot': 'wpn_size', 'visible': True},     
        'shield': {'name': __('shield'), 'slot': 'wpn_size', 'visible': True},        
        
        'subdual': {'name': __('subdual'), 'slot': 'wpn_dmg', 'visible': True},        
        'slashing': {'name': __('slashing'), 'slot': 'wpn_dmg', 'visible': True},  
        'piercing': {'name': __('piercing'), 'slot': 'wpn_dmg', 'visible': True},  
        'impact': {'name': __('impact'), 'slot': 'wpn_dmg', 'visible': True},  
        'elemental': {'name': __('elemental'), 'slot': 'wpn_dmg', 'visible': True},  
        'silvered': {'name': __('silvered'), 'slot': 'wpn_dmg', 'visible': True},       

        'light_armor': {'name': __('light armor'), 'slot': 'armor_rate', 'visible': True},
        'heavy_armor': {'name': __('heavy armor'), 'slot': 'armor_rate', 'visible': True},  

        }
