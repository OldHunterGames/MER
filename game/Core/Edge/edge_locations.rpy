# Edge of Mists locations

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
        'The tides of Mist brought here an old battlefield full of dead bodies and battered armaments. Territory is under control of [location.owner.name]. You can see a few scavergers here and there, they lookin for usible munitions.'
        'Work for food':
            $ pass
        'Pay a tool for scavenge':
            $ pass
        'Ask to join the band':
            $ pass
        'Get out':
            jump lbl_edge_locations_menu   

    return

label lbl_edge_dying_grove(location):
    $ special_values = {'place': 'grove', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu             
    return

label lbl_edge_hazy_marsh(location):
    $ special_values = {'place': 'marsh', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu        
    return
    
label lbl_edge_echoing_hills(location):
    $ special_values = {'place': 'hills', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu        
    return
    
label lbl_edge_outpost(location):
    call screen sc_universal_trade
    return