## Opportunities

label lbl_edge_opportunities:
   
    python:     
        options = CardsMaker()
        options.add_entry('feed_hungry', edge_option_cards)
        options.add_entry('observe', edge_option_cards)
        options.add_entry('look_troble', edge_option_cards)
        if 'recruiter' not in edge.options:
            options.add_entry('opp_find_recruiter', edge_option_cards)                        
        if 'slaver' not in edge.options:
            options.add_entry('opp_find_slaver', edge_option_cards) 
        options.add_entry('nevermind', edge_option_cards)  
        CardMenu(options.run()).show()
                
    hide card

    call lbl_edge_manage
    return
    
label lbl_edge_find_recruiter(card):
    $ call_event('recruiter', player, True)
    
    return
    
label lbl_edge_find_slaver(card):
    $ call_event('slaver', player, True)
    
    return

label lbl_edge_feed_hungry(card):
    if player.money < 5:
        'You have no spare food.'
        return 
    else:
        $ player.money -= 5
        'You feed the hungry one.'
        $ player.moral_action(target=None, moral='good') 
    return
    
label lbl_edge_look_troble(card):
    $ player.moral_action(target=None, activity='ardent') 
    call edge_job_range(player)
    
    return
        
label lbl_edge_observe(card):
    python:
        'Observing...'
        rnd = choice(edge_exploration)
        evn = 'evn_edge_' + rnd
        call_event(evn, player)
    
    return
