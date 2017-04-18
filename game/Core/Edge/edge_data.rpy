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
        'citisen': __("You become are full fleged citisen of the Eternal Rome. Great feat indeed! Now you on your own, the possibilities are wast."),
    }

    edge_jobs_data = {
    'idle': {'name': __('Idle'), 'description': 'Idle\nTimid deed. Just rest and take your time for yourself. Gain enregy.', 'skill': None, 'difficulty': 0, 'world': 'edge', 'image': 'miscards', },

    'beg': {'name': __('Beggar'), 'description': 'Beg for food\nTimid deed. No challenge. Get a bare minimum of worst food, just enough to sustain yourself. Your authority, prosperity and wellness will suffer in a process. ', 'skill': None, 'difficulty': 0, 'world': 'edge'},
    'bukake': {'name': __('Bukake slut'), 'description': 'Bukkake-slut\nKind deed. No challenge. Suck your dinner out of the slum-scums balls through their dirty cocks. Unhealthy, tiresome job, humiliation and sexplotation treat. Get unlimited but disgusting food.', 'skill': None, 'difficulty': 0, 'hidden' : True, 'world': 'edge'},      

    'construction': {'name': __('Construction work'), 'description': __('Construction work\nLawful deed.\nEndurance productivity.\nBoring job.\nConstruction in the slums is ongoing. While the Mists overflow and make some territories unsuitable for life, stubborn slum dwellers build up other places with their miserable adobe huts. Hardy worker will not be left without business.'), 'skill': 'physique', 'difficulty': 0, 'world': 'edge'},
    'extraction': {'name': __('Demonblood extraction'), 'description': __('Demonblood extraction.\nLawful deed.\nEndurance productivity.\nUnhealthy job.\nThe tar-like dark crimson "demonblood" is the only source of fuel for slum dwellers as well as for the Eternal Rome itself. This substance is extracted in foul-filled pits and is formed into air-cake pellets which are then sold as solid fuel.'), 'skill': 'physique', 'difficulty': 0, 'world': 'edge'},
    'entertain': {'name': __('Entertain patrons'), 'description': __('Entertain patrons.\nLawful deed.\nGrace productivity.\nHumiliating job\nIn the grim life of Freeman, there are only two reliable entertainments - sex and a crappy moonshine that is served in a single drinking house for the whole district. The second entertainment by local standards is elite, so regulars are usually entertained with songs and dances. Entertainers suffer pinching and caustic comments in the process, but they get good tips.'), 'skill': 'agility', 'difficulty': 0, 'world': 'edge'},
    'houseservice': {'name': __('Household service'), 'description': __('Household services.\nLawful deed.\nWisdom productivity.\nBoring job\nEven in the slums there is a daily routine - washing, cleaning and cooking. Happy are those who can afford to hire someone to do the job. However, the workers do not complain, because they can provide their own food.'), 'skill': 'agility', 'difficulty': 0, 'world': 'edge'},
    'scavenger': {'name': __('Scavenge the Edge'), 'description': __('Scavenger.\nChaotic deed.\nWisdom productivity.\nUnpleasant work\nThe tides of the Mists bring fragments of the Outer Worlds. Fields of battle, strewn with decaying bodies, dead withered forests, abandoned factories with rusted machinery and crashed space ships ... is a paradise of scavengers who are not afraid to get their hands dirty. Here you can find many interesting things to sell them to the junkie from the Outpost.'), 'skill': 'agility', 'difficulty': 0, 'world': 'edge'},

    'hooker': {'name': __('Prostitution'), 'description': __('Whore.\n\nSex or assault encounters.\nUnhealthy, tiresome job, humiliation and sexplotation treat.\nMany women on the Border of the Mists are trying to survive selling their body. This work is very dangerous, so prostitutes do not live too long and there is always a place for "fresh meat" in the sex market.'), 'skill': None, 'difficulty': 0, 'world': 'edge'},
    'range': {'name': __('Range the Edge'), 'description': 'Patrool the Edge of Mists. Encounters with wanderers, marauders and monsters expected.', 'skill': None, 'difficulty': 0, 'world': 'edge'},   
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
    'nap': {"name": __("Nap"), 'description': __("Overtime nap is free."), 'cost': 0, 'world': 'edge'},  
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
    
    edge_option_cards = {'nevermind': {'name': 'Nevermind', 'description': __('Nevermind'), 'label': 'lbl_edge_comm_nevermind', 'image': 'miscards', }, 
        'makelove': {'name': 'Make love', 'description': __('Make love\n'), 'label': 'lbl_makelove', 'image': 'miscards', }, 
        'flee': {'name': 'Flee', 'description': __('Flee\nTimid action. Just get out of here and do not involve.'), 'label': 'lbl_edge_enc_flee', 'image': 'miscards', }, 
        'assault_yeld': {'name': 'Yeld', 'description': __('Yeld\nTimid action. Lose your savings and equipement but save your life... maybe.'), 'label': 'edge_jbevent_yeld', 'image': 'miscards', }, 
        
        'feed_hungry': {'name': 'Feed the hungry', 'description': __('Good deed. Cost you 5/bars.'), 'label': 'lbl_edge_feed_hungry', 'image': 'miscards', }, 
        'observe': {'name': 'Observe', 'description': __('Maybe you can find a new opportunities'), 'label': 'lbl_edge_observe', 'image': 'miscards', }, 
        'look_troble': {'name': 'Look for trobles', 'description': __('Look for troubles\nArdent deed. You will encouner someone... or something'), 'label': 'lbl_edge_look_troble', 'image': 'miscards', }, 
        'opp_find_outpost': {'name': 'Check outpost', 'description': __('Outpost\nThe huge wall seems to stretch endlessly in both directions. But the passage inside is visible only in one place - a massive tower with a gate protruding far ahead from the wall. At the foot of the tower, fenced with steel mesh is a small military outpost, something like a checkpoint. There are quite a lot of people and security guards in heavy armor are on duty.'), 'label': 'lbl_edge_find_outpost', 'image': 'miscards', }, 
        'opp_find_junker': {'name': 'Junk trade', 'description': __('Junker\nThere are rumors that there is someone at the outpost who buys any items from other worlds for nutritional bars. To start such a familiarity would be very interesting.'), 'label': 'lbl_edge_find_junker', 'image': 'miscards', }, 
        'opp_find_recruiter': {'name': 'Meet representative', 'description': __('Meet Major House representative\nIt is your chance to get inside the walls of Eternal Rome.'), 'label': 'lbl_edge_find_recruiter', 'image': 'miscards', }, 
        'opp_find_slaver': {'name': 'Slave trade', 'description': __('Meet the slavedriver\nMany poor souls ending up on a slave market, sold to Eternal Rome citisens. Not a worst fate here on the Edge of Mists. You should meet person in charge of slave trade at the Outpost.'), 'label': 'lbl_edge_find_slaver', 'image': 'miscards', }, 
       

        'fi_intimidate': {'name': 'Intimidate', 'description': __('Intimidate\nArdent deed. Opposed willpower check to succed. Get "Charriot" relations arcane.'), 'label': 'lbl_first_impression_intimidate', 'image': 'miscards', }, 
        'fi_getknow': {'name': 'Get to know', 'description': __('Get to know\nLawful deed. Opposed wisdom check to succed. Get "Justuce" relations arcane.'), 'label': 'lbl_first_impression_getknow', 'image': 'miscards', }, 
        'fi_flatter': {'name': 'Flatter', 'description': __('Flatter\nGood deed. Opposed finesse check to succed. Get "Lovers" relations arcane.'), 'label': 'lbl_first_impression_flatter', 'image': 'miscards', }, 
        'fi_joke': {'name': 'Sudden jock', 'description': __('Sudden jock\nChaotic deed. Unpredictible outcome.'), 'label': 'lbl_first_impression_joke', 'image': 'miscards', }, 
        'fi_mock': {'name': 'Mock', 'description': __('Mock\nEvil deed.\nGain "Moon" relations arcane and self-affirm your authority.'), 'label': 'lbl_first_impression_mock', 'image': 'miscards', }, 
        'fi_reticence': {'name': 'Reticence', 'description': __('Reticence\nTimid deed. Be patient and quiet. No risk. No reward.'), 'label': 'lbl_first_impression_reticence', 'image': 'miscards', }, 

        'com_obligation': {'name': 'Get favor', 'description': __('Get favor\nThis person is obliged to you, so you may ask for a reward or promote relationship.'), 'label': 'lbl_edge_comm_obligation', 'image': 'miscards', }, 
        'comm_garantor': {'name': 'Be my garantor', 'description': __('Garantor\nYou need a garantor, to become a major House citisen. This person can help you.'), 'label': 'lbl_comm_garantor', 'image': 'miscards', }, 
        'com_hungout': {'name': 'Hung out', 'description': __('Hung out\nSpend some quality time together to promote your relationship.'), 'label': 'lbl_edge_comm_hungout', 'image': 'miscards', }, 
        'com_present': {'name': 'Present', 'description': __('Present\nMake a valuable present as an offering to promote your relationship.'), 'label': 'lbl_edge_comm_call_quest', 'image': 'miscards', },         
        'com_takequest': {'name': 'Quest aviable', 'description': __('Quest\nAsk if you can do sometng to get your relationship to a whole new level.'), 'label': 'lbl_edge_comm_call_quest', 'image': 'miscards', }, 
        'com_quest_completed': {'name': 'Quest completed', 'description': __('Quest\nThis person will owe you now.'), 'label': 'lbl_edge_comm_complete_quest', 'image': 'miscards', }, 
#        'com_agression': {'name': 'Name', 'description': __('descriptext'), 'label': 'lbl_edge_option_', 'image': 'miscards', },         

        'spc_enslave': {'name': 'Persuade', 'description': __("Persuade to enslavement\nOpposed spirit challenge\nLife on the border is difficult and dangerous. So much so that it's probably better to be a slave in Eternal Rome than fremen on the Edge of Mists. Convince this person that you can help it to get into good hands."), 'label': 'lbl_edge_enslave', 'image': 'miscards', }, 
        'spc_become_slave': {'name': 'Bond to slavery', 'description': __('Bond to slavery\nThe simplest way to get into Eternal Rome is to sell yourself into slavery. Your new master will take you there.'), 'label': 'lbl_edge_slave_auction', 'image': 'miscards', }, 
        'spc_recruiter_bond': {'name': 'Job options', 'description': __('Work for a Major House\nAsk if you can apply for a job for a Major House.'), 'label': 'lbl_edge_spc_bond_start', 'image': 'miscards', }, 
        'spc_recruiter_citisen': {'name': 'Become a citisen', 'description': __('Major House membersip\nYou must prove yourself worthy.'), 'label': 'lbl_edge_spc_citisen_start', 'image': 'miscards', }, 
        'spc_sellall': {'name': 'Sell junk', 'description': __('Sell junk\nJunker will buy any items for a recycling. In Eternal Rome all materials are preccious.'), 'label': 'lbl_edge_spc_sellall', 'image': 'miscards', }, 

        'ho_promenade': {'name': 'Promenade', 'description': __('Promenade\nOpposed Spirit check. Gain communication and "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_promenade', 'image': 'miscards', }, 
        'ho_booze': {'name': 'Booze up', 'description': __('Booze up\nCosts 1 bar. Opposed Spirit check. Gain amusement and "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_booze', 'image': 'miscards', }, 
        'ho_dinner': {'name': 'Dinner treat', 'description': __('Dinner treat\nCosts 3 bars. Opposed Spirit check. Gain nutrition and "Lovers" or "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_dinner', 'image': 'miscards', },         
        'ho_discussion': {'name': 'Deep conversation', 'description': __('Deep conversation\nOpposed Wisdom check. Gain authority and "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_discussion', 'image': 'miscards', }, 
        'ho_erudition': {'name': 'Impressive erudition', 'description': __('Imprssive erudition\nOpposed Wisdo, check. Gain "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_erudition', 'image': 'miscards', }, 
        'ho_prank': {'name': 'Impressive prank', 'description': __('Impressive prank\nOpposed Finesse check. Gain "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_prank', 'image': 'miscards', },         
        'ho_might': {'name': 'Impressive might', 'description': __('Impressive might\nOpposed Might check. Gain "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_might', 'image': 'miscards', }, 
        'ho_favor': {'name': 'Carry a favor', 'description': __('Carry a favor\nOpposed Finesse check. Gain "Lovers" or "Justice" relationship arcane.'), 'label': 'lbl_edge_ho_favor', 'image': 'miscards', }, 
        'ho_dance': {'name': 'Dance all night', 'description': __('Dance all night long\nArdent deed. Opposed Might check. Gain activity and "Lovers" relationship arcane.'), 'label': 'lbl_edge_ho_dance', 'image': 'miscards', },         

        'bond_mistmarine': {'name': 'Mistmarine', 'description': __('Mistmarine\nFight for a House on the Outer Worlds.'), 'label': 'lbl_edge_mistmarine', 'image': 'miscards', }, 
        'bond_clerk': {'name': 'Clerk', 'description': __('Clerk\nOffice work.'), 'label': 'lbl_edge_bond_clerk', 'image': 'miscards', },         
        'bond_builder': {'name': 'Builder', 'description': __('Builder\nConstruction work.'), 'label': 'lbl_edge_bond_builder', 'image': 'miscards', }, 
        'bond_concubine': {'name': 'Concubine', 'description': __('Concubine\nBecome a sex toy for a Major House citisens.'), 'label': 'lbl_edge_sexy_exam', 'image': 'miscards', }, 
        'bond_servant': {'name': 'Servitor', 'description': __('Servitor\nBecome a servant in a Major House.'), 'label': 'lbl_edge_bond_servitor', 'image': 'miscards', }, 
        'bond_host': {'name': 'Host', 'description': __('Host\nEntertain customers in drinking establishments of the Majpr House.'), 'label': 'lbl_edge_bond_host', 'image': 'miscards', },         

#    'id': {'name': 'Name', 'description': __('Name\n'), 'label': 'lbl_edge_', 'image': 'miscards', }, 
#    'id': {'name': 'Name', 'description': __('Name\n'), 'label': 'lbl_edge_', 'image': 'miscards', }, 
#    'id': {'name': 'Name', 'description': __('Name\n'), 'label': 'lbl_edge_', 'image': 'miscards', },         
#    'id': {'name': 'Name', 'description': __('Name\n'), 'label': 'lbl_edge_', 'image': 'miscards', }, 
#    'id': {'name': 'Name', 'description': __('Name\n'), 'label': 'lbl_edge_', 'image': 'miscards', }, 
#    'id': {'name': 'Name', 'description': __('Name\n'), 'label': 'lbl_edge_', 'image': 'miscards', },         
    }
    
    edge_quest_rewards = {
        'reward_garantor': {'name': 'Garantor', 'description': __('Garantor\nThis person will vouch for you for the Major House'), 'label': 'lbl_comm_garantor', 'image': 'miscards', }, 
        'reward_sparks': {'name': 'Sparks', 'description': __('Sparks\nIf you have a clear gem (jewel for example) it will be infused with the Sparks of Creation. This Sparks is a best curency in Eternal Rome but wortless on the Edge of Mists.'), 'label': 'lbl_edge_reward_sparks', 'image': 'miscards', }, 
        'reward_banknotes': {'name': 'Banknotes', 'description': __('Bundle of banknotes\nThis paper money signed by a Major House seal is a common currency at the Eternal Rome.'), 'label': 'lbl_edge_reward_banknotes', 'image': 'miscards', },   
        'reward_bars': {'name': 'Food bars', 'description': __('Nutrition Bars\nBox of 100 nutrition bars. Each bar can feed a human for entire day and do not spoil until the packaging is opened. Used as a common currency at the Edge of Mists.'), 'label': 'lbl_edge_reward_bars', 'image': 'miscards', }, 
        'reward_relations': {'name': 'Relations', 'description': __('Relations\nYou can reinforce your influence, making this person more inclined to cooperate.'), 'label': 'lbl_edge_reward_relations', 'image': 'miscards', },                 
    }
        
    edge_seduce_jury = {
        'seduce_body': {'name': 'Body demonstration', 'description': __('Body demonstration\nTry to impress hury with your natural body health and vigor.'), 'label': 'lbl_edge_sexy_exam_might', 'image': 'miscards', }, 
        'seduce_grace': {'name': 'Striptease', 'description': __('Striptease\nGraceful strip-dance for a jury.'), 'label': 'lbl_edge_sexy_exam_grace', 'image': 'miscards', }, 
        'seduce_mind': {'name': 'Dirty talk', 'description': __('Dirty talk\nTell the jury about your most intimate and wicked fantasies.'), 'label': 'lbl_edge_sexy_exam_mind', 'image': 'miscards', },         
        'seduce_spirit': {'name': 'Passionate seduction', 'description': __('Passionate seduction\nJust show jury your character and seduce them straightforward.'), 'label': 'lbl_edge_sexy_exam_spirit', 'image': 'miscards', }, 
    }


    edge_raider_options = {
   'raider_engage': {'name': 'Engage', 'description': __('Engage\nArdent deed. Combat challenge.'), 'label': 'lbl_edge_raider_fight', 'image': 'miscards', }, 
   'raider_flee': {'name': 'Flee', 'description': __('Flee\nTimid deed. Stamina challenge (easy). No chance to fight back.'), 'label': 'lbl_edge_raider_flee', 'image': 'miscards', }, 
   'raider_hide': {'name': 'Hide', 'description': __('Hide\nTimid deed. Grace challenge (easy). No chance to fight back.'), 'label': 'lbl_edge_raider_hide', 'image': 'miscards', },         
   'raider_talk': {'name': 'Talk', 'description': __('Talk\nSpirit challenge (mennace based). Chance to fight back if failed.'), 'label': 'lbl_edge_raider_talk', 'image': 'miscards', }, 
   'raider_yeld': {'name': 'Yeld', 'description': __('Yeld\nBecome a slave.'), 'label': 'lbl_edge_raider_yeld', 'image': 'miscards', }, 
    }

    edge_errant_options = {
    'errant_talk': {'name': 'Talk', 'description': __('Talk\nStart a peaceful communication.'), 'label': 'lbl_edge_errant_talk', 'image': 'miscards', }, 
    'errant_stalk': {'name': 'Hide & stalk', 'description': __('Hide & Stalk\n Timid deed. Opposed finesse challenge. Try to stalk the confused wanderer stealthily. Get chance for a sneak attack.'), 'label': 'lbl_edge_errant_stalk', 'image': 'miscards', }, 
    'errant_engage': {'name': 'Engage', 'description': __('Engage\nArdent deed. Agressive approach. Fight (combat challenge) or chase (opposed might challenge) is possible.'), 'label': 'lbl_edge_enc_engage', 'image': 'miscards', },         
    'errant_decieve': {'name': 'Decieve', 'description': __('Decieve\nChaotic deed. Spirit challenge vs target wisdom. Try to lull targets attention and then suddenly attack.'), 'label': 'lbl_edge_enc_decieve', 'image': 'miscards', }, 
    'errant_subdue': {'name': 'Subdue', 'description': __('Subdue\nEvil deed. Hit the errant over the head with a rock. with a rock. Or just grab and pin down if you a strong enough...'), 'label': 'lbl_edge_errant_subdue', 'image': 'miscards', }, 
    'errant_backstab': {'name': 'Backstab', 'description': __('Backstab\nEvil deed. Killing blow.'), 'label': 'lbl_edge_errant_backstab', 'image': 'miscards', }, 
    }

    edge_captive_options = {
    'captive_loot': {'name': 'Loot', 'description': __('Loot\nGet all captive possesions.'), 'label': 'lbl_edge_captive_loot', 'image': 'miscards', }, 
    'captive_sell': {'name': 'Sell', 'description': __('Sell\nSell a captive to a slavedriver. Price is based on atributes.'), 'label': 'lbl_edge_captive_sell', 'image': 'miscards', }, 
    'captive_rape': {'name': 'Rape', 'description': __('Rape\nArdent deed.\nGet some fun.'), 'label': 'lbl_edge_captive_rape', 'image': 'miscards', },         
    'captive_slay': {'name': 'Slay', 'description': __('Slay\nEvil deed.\nIf you need a corpse...'), 'label': 'lbl_edge_captive_slay', 'image': 'miscards', }, 
    'captive_cannibalise': {'name': 'Slay & Eat', 'description': __('Slay & Eat\nEvil deed.\nOn the Border of the Mists nothing grows. Here there are only two sources of food - nutritional bars that you can bargain at the outpost or meat of other inhabitants of the border. Meat is more delicious.'), 'label': 'lbl_edge_captive_cannibalise', 'image': 'miscards', }, 
    'captive_capture': {'name': 'Capture', 'description': __('Capture\nLawful deed.\n'), 'label': 'lbl_edge_captive_capture', 'image': 'miscards', }, 
    'captive_release': {'name': 'Release', 'description': __('Release\nChaotic deed.\n'), 'label': 'lbl_edge_captive_release', 'image': 'miscards', },         
    }

    edge_quest_options = {
    'quest_duel': {'name': 'Duel', 'description': __('Duel\nWin a fight against this character.'), 'label': 'lbl_edge_duel', 'image': 'miscards', }, 
    'quest_please': {'name': 'Sexualy please', 'description': __('Sexualy please\nThis character craves for exceptional pleasure.'), 'label': 'lbl_makelove', 'image': 'miscards', }, 

    }
