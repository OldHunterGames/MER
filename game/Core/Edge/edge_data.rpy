init python:
    edge_yeld = [0, 1, 3, 6, 10, 15]
    
    edge_locations = {
        'outpost': __('House {0} outpost'),
        'grim_battlefield': __('grim battlefield ({0})'),
        'crimson_pit': __('crimson pit ({0})'),
        'junk_yard': __('junk yard ({0})'),
        'ruined_factory': __('ruined factory ({0})'),
        'dying_grove': __('dying grove'),
        'hazy_marshes': __('hazy marshes'),
        'echoing_hills': __('echoing hills'),
        'squatted_slums': __('squatted slums ({0})'),
        #'charity_mission': __('House {0} charity mission'),
        'shifting_mist': __('Shifting mist')
        }

    edge_encounters = ['stranger',
    ]
    
    edge_denotation = {
        'idle': __('idle'),
        'explore': __('explore'),
        'nap': __('rest'),
        'foundcamp': __('found camp'),
        'scout': __('scout'),
        'scmunition': __('scavenge munition'),
        'dbexctraction': __('extract fuel'),
        'scjunc': __('scavenge junk'),
        'disassemble': __('disassemble machinery'),
        'lookforstash': __('look for hidden stash'),
        'foodwork': __('work for food'),
        }

    gang_prefix_names = [__('Black'),
        __('Red'),
        __('White'),
        __('Crimson'),
        __('Bloody'),
        __('Golden'),
        __('Silver'),
        __('Purple'),
        __('Hungry'),
        __('Howling'),
        __('Vicious'),
        __('Daring'),
        __('Dire'),
        __('Jagged'),
        __('Venomous'),
        __('Gaudy'),
        __('Mighty'),
        __('Night'),
        __('Wild'),
        __('Chaos'),
        __('Mad'),
        __('Frenzied'),
        __('Rabid'),
        __('Shadow'),
        __('Decadent'),
        __('Ravenous'),
        __('Horny'),
        __('Desperate'),
        __('Wicked'),
        __('Thunder'),
        __('Gutsy'),
        __('Angry'),
        __('Grey'),
        ]

    gang_suffix_names = [__('Wolves'),
        __('Vipers'),
        __('Knives'),
        __('Swords'),
        __('Fists'),
        __('Gauntlets'),
        __('Rangers'),
        __('Brothers'),
        __('Martyrs'),
        __('Lurkers'),
        __('Rats'),
        __('Cocks'),
        __('Stalkers'),
        __('Falcones'),
        __('Eagles'),
        __('Hounds'),
        __('Bears'),
        __('Drifters'),
        __('Lions'),
        __('Boars'),
        __('Dodgers'),
        __('Stallions'),
        __('Punks'),
        __('Cult'),
        __('Defilers'),
        __('Marauders'),
        __('Ravagers'),
        __('Devils'),
        __('Spiders'),
        __('Hornets'),
        __('Spears'),
        __('Harlequins'),
        __('Kings'),
        __('Vultures'),
        __('Ravens'),       
        __('Fangs'),
        __('Amigos'),
        __('Helms'),
        __('Shields'),
        __('Sabres'),
        __('Axes'),
        __('Lancers'),
        __('Fiends'),
        __('Bulls'),
        ]

    fates_list = {
        'concubine': __('You become a concubine at the Major House of Eternal Rome. Game full of sexy encounters ecpected...'),   
        'stripper': __('You become a stripper at the Major House of Eternal Rome. Game full of sexy encounters ecpected...'),   
        'maid': __('You become a sexy maid at the Major House of Eternal Rome. Game full of hard work and sexy encounters ecpected...'),   
        'secretaty': __('You become a secretary at the Major House of Eternal Rome. Game full of hard work and sexy encounters ecpected...'),   
        'nurse': __('You become a sexy nurse at the Major House of Eternal Rome. Game full of hard work and sexy encounters ecpected...'),   
        'scholar': __('You become a sholar at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'artisan': __('You become an artisan at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'repairperson': __('You become a repairperson at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'integrator': __('You become an electrinics system integrator at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'mistmarine': __('You become a mistmarine at the Major House of Eternal Rome. Game of epic warfare and violence in Outer Worlds is ecpected...'),   
    }

    edge_jobs_data = {
    'idle': {'name': __('Idle'), 'description': 'EROR', 'skill': None, 'difficulty': 0},
    'manual': {'name': __('Manual labor'), 'description': __('doing manual labor in slums'), 'skill': 'physique', 'difficulty': 2},
    'houseservice': {'name': __('Simple work'), 'description': __('providing household services in the slums'), 'skill': 'physique', 'difficulty': 2},
    'range': {'name': __('Range the Edge'), 'description': 'EROR', 'skill': None, 'difficulty': 0},   
    'beg': {'name': __('Beggar'), 'description': 'EROR', 'skill': None, 'difficulty': 0},
    'bukake': {'name': __('Bukake slut'), 'description': 'EROR', 'skill': None, 'difficulty': 0},      
    
    'repair': {'name': __('Repairings'), 'description': __('repairs various stuff for slum-dwellers'), 'skill': None, 'difficulty': 0},
    'entertain': {'name': __('Entertain patrons'), 'description': __('entertains the slum-dwellers'), 'skill': None, 'difficulty': 0},
    'alchemy': {'name': __('Brew booze'), 'description': __('brew booze for a slum-dwellers'), 'skill': None, 'difficulty': 0},
    'disassembly': {'name': __('Disassemble wrecks'), 'description': __('disassembles old machinery'), 'skill': None, 'difficulty': 0},

    'treasurehunt': {'name': __('Treasure hunt'), 'description': __('Descriptext'), 'skill': 'mind', 'difficulty': 2},
    }   
    
    edge_services_data = {
        'personal_slut': {"name": __("Personal slut"), 'description': "Your own slut", 'cost': 5, 'event': 'slut'}
    }


