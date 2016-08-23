# Edge of Mists locations

label lbl_edge_missed_location:
    'In progress'    
    return

label lbl_edge_shifting_mist(location=None):
    'Battle'
    python:
        ally1 = DuelCombatant(player)
        enemy1 = DuelCombatant(gen_random_person('human'))
        basic_deck = Deck(['clinch', 'hit_n_run', 'rage', 'outsmart', 'fallback', 'bite', 'headbutt', 'recoil', 'dodge', 'deep_breath', 'caution', 'bite', 'bite', 'light_strike', 'strike', 'powerful_strike', 'move', 'dash', 'fast_dash', 'rebound', 'block', 'hard_block'])
        ally1.set_deck(basic_deck)
        enemy1.set_deck(basic_deck)
        
        fight = DuelEngine([ally1],[enemy1], None)
        fight.start()
    return

label lbl_edge_grim_battlefield(location):
    menu:
        'The tides of Mist brought here an old battlefield full of dead bodies and battered armaments. Territory is under control of [location.owner.name]. You can see a few scavergers here and there, they looking for usible munitions.'
        'Find out about [location.owner.name]':
            'Information'
        'Work for food':
            menu:
                'The [location.owner.name] offer to give you some food (3 provisions units) if you scavenge armaments for them for a decade.'
                'Agree':
                    $ special_values = {'skill': 'survival', 'beneficiar': location.owner,}
                    $ target.schedule.add_action('job_foodwork', 1, special_values=special_values)  
                    jump lbl_edge_manage
                'Decline':
                    $ pass
        'Pay a tool for scavenge':
            menu:
                'You must pay 400 banknotes to [location.owner.name] in order to scavenge their territory for usible munitions for a decade. All you can find and carry out is yours.'
                'Agree (400 banknotes)' if core.resources.money >= 400:
                    $ core.resources.money -= 400
                    $ description = ' scavenging munition on the gim battlefield. Yelds '
                    $ special_values = {'description': description, 'resource': core.resources.munition, 'resource_name': 'munition', 'skill': 'survival', 'difficulty' : 1, 'moral': None, 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
                    $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
                    jump lbl_edge_manage
                'Decline':
                    $ pass
        'Ask to join the [location.owner.name] gang' if not core.has_any_faction(player):
            'Not yet implemented'
        'Get out':
            return 

    call lbl_edge_grim_battlefield(location) 
    return

label lbl_edge_dying_grove(location):
    $ special_values = {'place': 'grove', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu             
    return

label lbl_edge_hazy_marsh(location):
    $ special_values = {'place': 'marsh', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu        
    return
    
label lbl_edge_echoing_hills(location):
    $ special_values = {'place': 'hills', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu        
    return
    
label lbl_edge_outpost(location):
    call screen sc_universal_trade
    return