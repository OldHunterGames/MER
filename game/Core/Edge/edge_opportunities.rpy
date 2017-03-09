## Opportunities

label lbl_edge_opportunities:
    
    #TODO
    $ CardMenu(MakeOpportunitiesCards().run()).show()
    call lbl_edge_manage
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
