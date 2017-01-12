init python:
    
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
    'idle': {'name': __('Idle'), 'description': 'Just rest and relax.', 'skill': None, 'difficulty': 0},
    'manual': {'name': __('Manual labor'), 'description': __('Simple manual labor in slums for a fixed salary 10 bars/decade.'), 'skill': 'physique', 'difficulty': 1},
    'houseservice': {'name': __('House service'), 'description': __('Provide household services in the slumsfor a fixed salary 10 bars/decade.'), 'skill': 'agility', 'difficulty': 1},
    'range': {'name': __('Range the Edge'), 'description': 'Patrool the Edge of Mists. Encounters with wanderers, marauders and monsters expected.', 'skill': None, 'difficulty': 0},   
    'beg': {'name': __('Beggar'), 'description': 'Humbly beg for a food.', 'skill': None, 'difficulty': 0},
    'bukake': {'name': __('Bukake slut'), 'description': 'Suck your dinner out of the slum-scum cocks.', 'skill': None, 'difficulty': 0, 'hidden' : True},      
    
    'construction': {'name': __('Construction'), 'description': __('Might challenge. Slums need new shelters, more you can build more bars you get.'), 'skill': 'physique', 'difficulty': 2},
    'entertain': {'name': __('Entertain patrons'), 'description': __('Finesse challenge. Entertain the slum-dwellers as a street artist.'), 'skill': 'agility', 'difficulty': 2},
    'disassembly': {'name': __('Disassemble wrecks'), 'description': __('Wisdom challenge. Disassemble old machinery in a wrecks and ruins brought by a Mistide.'), 'skill': 'mind', 'difficulty': 2},

    'treasurehunt': {'name': __('Treasure hunt'), 'description': __('Descriptext'), 'skill': 'mind', 'difficulty': 2, 'hidden' : True},
    }   
    
    edge_services_data = {
        'bukake': {"name": __("Bukake sluts"), 'description': __("Feed bukake sluts with your cum."), 'cost': 0, 'hidden' : True},
        'whores': {"name": __("Whores"), 'description': __("Use prostitutes services"), 'cost': 5},
        'booze': {"name": __("Booze"), 'description': __("The nutrition bars brew called a Mystshine."), 'cost': 5},        
        'maid': {"name": __("Attendant"), 'description': __("Get someone to serve you."), 'cost': 5},       
    }

    edge_accomodations_data = {
        'makeshift': {"name": __("Homeless"), 'description': __("Sleeps on the ground. No cost."), 'cost': 0},
        'mat': {"name": __("Barracks (5)"), 'description': __("Thin rag mat in a barracks. 5 bars/decade"), 'cost': 5},
        'cot': {"name": __("Humble cot (10)"), 'description': __("Cot and blanket in a common room. 10 bars/decade"), 'cost': 10},
        'appartment': {"name": __("Appartments (25)"), 'description': __("Rent a flatlet. 25 bars/decade"), 'cost': 25},                        
    }

    edge_feeds_data = {
        'forage': {"name": __("Starving"), 'description': __("Starve. No cost."), 'cost': 0, 'quality': 0, 'amount': 0},
        'dry_low': {"name": __("5 bars"), 'description': __("Eat 5 nutrition bars."), 'cost': 5},
        'dry': {"name": __("10 bars"), 'description': __("Eat 10 nutrition bars."), 'cost': 10},
        'dry_high': {"name": __("15 bars"), 'description': __("Eat 15 nutrition bars."), 'cost': 15},
        'cooked': {"name": __("Cooked food (20)"), 'description': __("Eat cooked food in a pub. Don't ask wich meat it is. 20 bars/decade"), 'cost': 20},
        'cooked_high': {"name": __("Grilled girl (30)"), 'description': __("Eat grilled human flesh.  30 bars/decade"), 'cost': 30},
        'canibalism': {"name": __('"Long pig"'), 'description': __("Deth for one is a life for another. This corpse will not root in vine."), 'cost': 0, 'hidden': True},                                                
    }

    edge_overtimes_data = {
        'rest': {"name": __("Nap"), 'description': __("Overtime nap"), 'cost': 0},  
        'sports': {"name": __("Sports"), 'description': __("Free time is a workout time!"), 'cost': 0},  
        'bar': {"name": __("Pub"), 'description': __("Hung in a pub."), 'cost': 5},  
        'healing': {"name": __("Healing"), 'description': __("Get some medical attention."), 'cost': 5},          
    }

