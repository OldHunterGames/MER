init -10 python:

    
    edge_lifestyle_values = {'0': {'treshold': 0, 'name': __("Miserable poverty")}, 
    '1': {'treshold': 10, 'name': __("Poverty")}, 
    '2': {'treshold': 20, 'name': __("Modest lifestyle")}, 
    '3': {'treshold': 40, 'name': __("Decent lifestyle")}, 
    '4': {'treshold': 70, 'name': __("Luxury")}, 
    '5': {'treshold': 100, 'name': __("Filty rich")}, }
    
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
        'servant': __('You become a servant at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'clerk': __('You become a clerk at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'host': __('You become a host at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'builder': __('You become a builder at the Major House of Eternal Rome. Game of career developement ecpected...'),   
        'mistmarine': __('You become a mistmarine at the Major House of Eternal Rome. Game of epic warfare and violence in Outer Worlds is ecpected...'),   
    }

    edge_jobs_data = {
    'idle': {'name': __('Idle'), 'description': 'Just rest and relax.', 'skill': None, 'difficulty': 0, 'world': 'edge', 'image': 'images/miscards/rest.png', },
    'manual': {'name': __('Manual labor'), 'description': __('Simple manual labor in slums for a fixed salary 10 bars/decade.'), 'skill': 'physique', 'difficulty': 0, 'world': 'edge'},
    'houseservice': {'name': __('House service'), 'description': __('Provide household services in the slumsfor a fixed salary 10 bars/decade.'), 'skill': 'agility', 'difficulty': 0, 'world': 'edge'},
    'range': {'name': __('Range the Edge'), 'description': 'Patrool the Edge of Mists. Encounters with wanderers, marauders and monsters expected.', 'skill': None, 'difficulty': 0, 'world': 'edge'},   
    'beg': {'name': __('Beggar'), 'description': 'Humbly beg for a food.', 'skill': None, 'difficulty': 0, 'world': 'edge'},
    'bukake': {'name': __('Bukake slut'), 'description': 'Suck your dinner out of the slum-scum cocks.', 'skill': None, 'difficulty': 0, 'hidden' : True, 'world': 'edge'},      
    
    'construction': {'name': __('Construction worker'), 'description': __('Might challenge. Slums need new shelters, more you can build more bars you get.'), 'skill': 'physique', 'difficulty': 1, 'world': 'edge'},
    'entertain': {'name': __('Entertain patrons'), 'description': __('Finesse challenge. Entertain the slum-dwellers as a street artist.'), 'skill': 'agility', 'difficulty': 1, 'world': 'edge'},
    'disassembly': {'name': __('Disassemble wrecks'), 'description': __('Wisdom challenge. Disassemble old machinery in a wrecks and ruins brought by a Mistide.'), 'skill': 'mind', 'difficulty': 1, 'world': 'edge'},

    'treasurehunt': {'name': __('Treasure hunt'), 'description': __('Descriptext'), 'skill': 'mind', 'difficulty': 2, 'hidden' : True, 'world': 'edge'},
    }   
    
    edge_services_data = {
        'bukake': {"name": __("Bukake sluts"), 'description': __("Feed bukake sluts with your cum."), 'cost': 0, 'hidden' : True, 'world': 'edge'},
        'whores': {"name": __("Whores"), 'description': __("Use prostitutes services"), 'cost': 5, 'world': 'edge'},
        'booze': {"name": __("Booze"), 'description': __("The nutrition bars brew called a Mystshine."), 'cost': 5, 'world': 'edge'},        
        'maid': {"name": __("Attendant"), 'description': __("Get someone to serve you."), 'cost': 5, 'world': 'edge'},       
    }

    edge_accomodations_data = {
        'makeshift': {"name": __("Homeless"), 'description': __("Sleeps on the ground. No cost."), 'cost': 0, 'world': 'edge'},
        'mat': {"name": __("Rag mat"), 'description': __("Thin rag mat in a barracks. 5 bars/decade"), 'cost': 5, 'world': 'edge'},
        'cot': {"name": __("Humble cot"), 'description': __("Cot and blanket in a common room. 10 bars/decade"), 'cost': 10, 'world': 'edge'},
        'appartment': {"name": __("Appartments"), 'description': __("Rent a flatlet. 25 bars/decade"), 'cost': 25, 'world': 'edge'},                        
    }

    edge_feeds_data = {
        'forage': {"name": __("Forage"), 'description': __("Eat any food you can get at the slums. IF you can get it."), 'cost': 0, 'quality': 0, 'amount': 0, 'world': 'edge'},
        'dry_low': {"name": __("5 bars"), 'description': __("Eat 5 nutrition bars/decade."), 'cost': 5, 'world': 'edge'},
        'dry': {"name": __("10 bars"), 'description': __("Eat 10 nutrition bars/decade."), 'cost': 10, 'world': 'edge'},
        'dry_high': {"name": __("15 bars"), 'description': __("Eat 15 nutrition bars/decade."), 'cost': 15, 'world': 'edge'},
        'cooked': {"name": __("Cooked food"), 'description': __("Eat cooked food in a pub. Don't ask wich meat it is. 20 bars/decade"), 'cost': 20, 'world': 'edge'},
        'cooked_high': {"name": __("Grilled girl"), 'description': __("Eat grilled human flesh.  30 bars/decade"), 'cost': 30, 'world': 'edge'},
        'canibalism': {"name": __('"Long pig"'), 'description': __("Death for one is a life for another. This corpse will not root in vine."), 'cost': 0, 'hidden': True, 'world': 'edge'},                                                
    }

    edge_overtimes_data = {
        'rest': {"name": __("Nap"), 'description': __("Overtime nap is free."), 'cost': 0, 'world': 'edge'},  
        'booze': {"name": __("Pub"), 'description': __("Hung in a pub and drink some crappy booze. 5 bars/decade. Wellness +3"), 'cost': 5, 'world': 'edge'},  
        'whores': {"name": __("Whore service"), 'description': __("Get a pro-hooker for a sexual relief. 5 bars/decade. Eros +3."), 'cost': 5, 'world': 'edge'},          
        'maid': {"name": __("Maid service"), 'description': __("Hire a subservient maid to do a chores for you. 10 bars/decade. Authority +2, comfort +2."), 'cost': 5, 'world': 'edge'},          
    }

    edge_nameset = {
    'generic': {'leader': __('Leader of'), 'champion': __('Champion of'), 'agent': __('Agent from'), 'ambassador': __('Ambassador of'), 'advisor': __('Advisor of'), 'member': __('Member of')}, 
    # 'cosanostra': {'leader': __('Goodfather'), 'champion': __('Cappodecina'), 'agent': __('Sotto cappo'), 'ambassador': __('Lawer'), 'advisor': __('Consigliere'), 'member': __('Soldati')}, 
    'band': {'leader': __('Boss of'), 'champion': __('Enforcer of'), 'agent': __('Pimp from'), 'ambassador': __('Dealer from'), 'advisor': __('Underboss of'), 'member': __('Thug of')}, 
    'western': {'leader': __('Mayor of'), 'champion': __('Sheriff of'), 'agent': __('Bartender from'), 'ambassador': __('Preacher from'), 'advisor': __('Doctor from'), 'member': __('Citisen of')}, 
    'medieval': {'leader': __('Baron of'), 'champion': __('Knight from'), 'agent': __('Jester from'), 'ambassador': __('Merchant from'), 'advisor': __('Bishop of'), 'member': __('Bond from')}, 
    'corporate': {'leader': __('President of'), 'champion': __('Sequrity of'), 'agent': __('Creative officer of'), 'ambassador': __('Vice-president of'), 'advisor': __('Chief engeneer of'), 'member': __('Employee of')}, 
    'tribal': {'leader': __('Chief of'), 'champion': __('Warlord of'), 'agent': __('Fire-keeper of'), 'ambassador': __('Trader from'), 'advisor': __('Shaman of'), 'member': __('Clansman of')}, 
    'military': {'leader': __('Commander of'), 'champion': __('Chief-sergeant of'), 'agent': __('Scout from'), 'ambassador': __('Quartermaster of'), 'advisor': __('Chief of staff from'), 'member': __('Squaddie from')},             
    }
    
    edge_option_cards = {'nevermind': {'name': 'Nevermind', 'description': __('Nevermind'), 'label': 'lbl_edge_comm_nevermind', 'image': 'images/miscards/card.png', }, 
        'makelove': {'name': 'Make love', 'description': __('Make love\n'), 'label': 'lbl_makelove', 'image': 'images/miscards/card.png', }, 
        'flee': {'name': 'Flee', 'description': __('Flee\nTimid action.'), 'label': 'lbl_edge_enc_flee', 'image': 'images/miscards/card.png', }, 
        
        'feed_hungry': {'name': 'Feed the hungry', 'description': __('Good deed. Cost you 5/bars.'), 'label': 'lbl_edge_feed_hungry', 'image': 'images/miscards/card.png', }, 
        'observe': {'name': 'Observe', 'description': __('Maybe you can find a new opportunities'), 'label': 'lbl_edge_observe', 'image': 'images/miscards/card.png', }, 
        'look_troble': {'name': 'Look for trobles', 'description': __('Ardent deed. You will encouner someone... or something'), 'label': 'lbl_edge_look_troble', 'image': 'images/miscards/card.png', }, 
        
        'fi_intimidate': {'name': 'Intimidate', 'description': __('Intimidate\nArdent deed. Opposed willpower check to succed. Get "Charriot" relations arcane.'), 'label': 'lbl_first_impression_intimidate', 'image': 'images/miscards/card.png', }, 
        'fi_getknow': {'name': 'Get to know', 'description': __('Get to know\nLawful deed. Opposed wisdom check to succed. Get "Justuce" relations arcane.'), 'label': 'lbl_first_impression_getknow', 'image': 'images/miscards/card.png', }, 
        'fi_flatter': {'name': 'Flatter', 'description': __('Flatter\nGood deed. Opposed finesse check to succed. Get "Lovers" relations arcane.'), 'label': 'lbl_first_impression_flatter', 'image': 'images/miscards/card.png', }, 
        'fi_joke': {'name': 'Sudden jock', 'description': __('Sudden jock\nChaotic deed. Unpredictible outcome.'), 'label': 'lbl_first_impression_joke', 'image': 'images/miscards/card.png', }, 
        'fi_mock': {'name': 'Mock', 'description': __('Mock/nEvil deed. Gain "Moon" relations arcane and self-affirm your authority.'), 'label': 'lbl_first_impression_mock', 'image': 'images/miscards/card.png', }, 
        'fi_reticence': {'name': 'Reticence', 'description': __('Reticence\nTimid deed. Be patient and quiet. No risk. No reward.'), 'label': 'lbl_first_impression_reticence', 'image': 'images/miscards/card.png', }, 

        'com_obligation': {'name': 'Get favor', 'description': __('Get favor\nThis person is obliged to you, so you may ask for a reward or promote relationship.'), 'label': 'lbl_edge_comm_obligation', 'image': 'images/miscards/card.png', }, 
        'comm_garantor': {'name': 'Be my garantor', 'description': __('Garantor\nYou need a garantor, to become a major House citisen. This person can help you.'), 'label': 'lbl_comm_garantor', 'image': 'images/miscards/card.png', }, 
        'com_hungout': {'name': 'Hung out', 'description': __('Hung out\nSpend some quality time together to promote your relationship.'), 'label': 'lbl_edge_comm_hungout', 'image': 'images/miscards/card.png', }, 
        'com_present': {'name': 'Present', 'description': __('Present\nMake a valuable present as an offering to promote your relationship.'), 'label': 'lbl_edge_comm_call_quest', 'image': 'images/miscards/card.png', },         
        'com_takequest': {'name': 'Quest aviable', 'description': __('Quest\nAsk if you can do sometng to get your relationship to a whole new level.'), 'label': 'lbl_edge_comm_call_quest', 'image': 'images/miscards/card.png', }, 
        'com_quest_completed': {'name': 'Quest completed', 'description': __('Quest\nThis person will owe you now.'), 'label': 'lbl_edge_comm_complete_quest', 'image': 'images/miscards/card.png', }, 
#        'com_agression': {'name': 'Name', 'description': __('descriptext'), 'label': 'lbl_edge_option_', 'image': 'images/miscards/card.png', },         

        'spc_become_slave': {'name': 'Bond to slavery', 'description': __('Bond to slavery\nThe simplest way to get into Eternal Rome is to sell yourself into slavery. Your new master will take you there.'), 'label': 'lbl_edge_slave_auction', 'image': 'images/miscards/card.png', }, 

        'ho_promenade': {'name': 'Promenade', 'description': __('Promenade\nOpposed Spirit check. Gain communication and "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_promenade', 'image': 'images/miscards/card.png', }, 
        'ho_booze': {'name': 'Booze up', 'description': __('Booze up\nCosts 1 bar. Opposed Spirit check. Gain amusement and "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_booze', 'image': 'images/miscards/card.png', }, 
        'ho_dinner': {'name': 'Dinner treat', 'description': __('Dinner treat\nCosts 3 bars. Opposed Spirit check. Gain nutrition and "Lovers" or "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_dinner', 'image': 'images/miscards/card.png', },         
        'ho_discussion': {'name': 'Deep conversation', 'description': __('Deep conversation\nOpposed Wisdom check. Gain authority and "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_discussion', 'image': 'images/miscards/card.png', }, 
        'ho_erudition': {'name': 'Impressive erudition', 'description': __('Imprssive erudition\nOpposed Wisdo, check. Gain "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_erudition', 'image': 'images/miscards/card.png', }, 
        'ho_prank': {'name': 'Impressive prank', 'description': __('Impressive prank\nOpposed Finesse check. Gain "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_prank', 'image': 'images/miscards/card.png', },         
        'ho_might': {'name': 'Impressive might', 'description': __('Impressive might\nOpposed Might check. Gain "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_might', 'image': 'images/miscards/card.png', }, 
        'ho_favor': {'name': 'Carry a favor', 'description': __('Carry a favor\nOpposed Finesse check. Gain "Lovers" or "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_favor', 'image': 'images/miscards/card.png', }, 
        'ho_dance': {'name': 'Dance all night', 'description': __('Dance all night long\nArdent deed. Opposed Might check. Gain activity and "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_dance', 'image': 'images/miscards/card.png', },         

        'errant_talk': {'name': 'Talk', 'description': __('Talk'), 'label': 'lbl_edge_errant_talk', 'image': 'images/miscards/card.png', }, 
        'errant_stalk': {'name': 'Hide & stalk', 'description': __('Hide & Stalk\nTry to stalk the confused wanderer stealthily. Opposed finesse challenge. Get chance to grab or backstab the wanderer.'), 'label': 'lbl_edge_errant_stalk', 'image': 'images/miscards/card.png', }, 
        'errant_engage': {'name': 'Engage', 'description': __('Engage\nArdent deed. Agressive approach. Fight or chase (Might challenge) expected.'), 'label': 'lbl_edge_enc_engage', 'image': 'images/miscards/card.png', },         
        'errant_decieve': {'name': 'Decieve', 'description': __('Decieve\nChaotic and evil deed. Try to lull targets attention and then suddenly attack.'), 'label': 'lbl_edge_enc_decieve', 'image': 'images/miscards/card.png', }, 

        'bond_mistmarine': {'name': 'Mistmarine', 'description': __('Mistmarine\nFight for a House on the Outer Worlds.'), 'label': 'lbl_edge_mistmarine', 'image': 'images/miscards/card.png', }, 
        'bond_clerk': {'name': 'Clerk' 'description': __('Clerk\nOffice work.'), 'label': 'lbl_edge_bond_clerk', 'image': 'images/miscards/card.png', },         
        'bond_builder': {'name': 'Builder', 'description': __('Builder\nConstruction work.'), 'label': 'lbl_edge_bond_builder', 'image': 'images/miscards/card.png', }, 
        'bond_concubine': {'name': 'Concubine', 'description': __('Concubine\nBecome a sex toy for a Major House citisens.'), 'label': 'lbl_edge_sexy_exam', 'image': 'images/miscards/card.png', }, 
        'bond_servant': {'name': 'Servitor', 'description': __('Servitor\nBecome a servant in a Major House.'), 'label': 'lbl_edge_bond_servant', 'image': 'images/miscards/card.png', }, 
        'bond_host': {'name': 'Host', 'description': __('Host\nEntertain customers in drinking establishments of the Majpr House.'), 'label': 'lbl_edge_bond_host', 'image': 'images/miscards/card.png', },         

#        'id': {'name': 'Name', 'description': __('descriptext'), 'label': 'lbl_edge_', 'image': 'images/miscards/card.png', }, 
#        'id': {'name': 'Name', 'description': __('descriptext'), 'label': 'lbl_edge_', 'image': 'images/miscards/card.png', }, 
#        'id': {'name': 'Name', 'description': __('descriptext'), 'label': 'lbl_edge_', 'image': 'images/miscards/card.png', },         
    }
    
    edge_quest_rewards = {
        'reward_garantor': {'name': 'Garantor', 'description': __('Garantor\nThis person will vouch for you for the Major House'), 'label': 'lbl_comm_garantor', 'image': 'images/miscards/card.png', }, 
        'reward_sparks': {'name': 'Sparks', 'description': __('Sparks\nIf you have a clear gem (jewel for example) it will be infused with the Sparks of Creation. This Sparks is a best curency in Eternal Rome but wortless on the Edge of Mists.'), 'label': 'lbl_edge_reward_sparks', 'image': 'images/miscards/card.png', }, 
        'reward_banknotes': {'name': 'Banknotes', 'description': __('Bundle of banknotes\nThis paper money signed by a Major House seal is a common currency at the Eternal Rome.'), 'label': 'lbl_edge_reward_banknotes', 'image': 'images/miscards/card.png', },   
        'reward_bars': {'name': 'Food bars', 'description': __('Nutrition Bars\nBox of 100 nutrition bars. Each bar can feed a human for entire day and do not spoil until the packaging is opened. Used as a common currency at the Edge of Mists.'), 'label': 'lbl_edge_reward_bars', 'image': 'images/miscards/card.png', }, 
        'reward_relations': {'name': 'Relations', 'description': __('Relations\nYou can reinforce your influence, making this person more inclined to cooperate.'), 'label': 'lbl_edge_reward_relations', 'image': 'images/miscards/card.png', },                 
    }
        
    
