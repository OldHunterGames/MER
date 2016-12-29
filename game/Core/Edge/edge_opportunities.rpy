## Opportunities

label lbl_edge_opportunities:
    menu:
        'Interesting observation' if edge_exploration:
            $ ap -= 1
            call lbl_edge_observations
        'Not yet':
            pass
    
    call lbl_edge_manage
    return

label lbl_edge_observations:
    python:
        rnd = choice(edge_exploration)
        evn = 'evn_edge_' + rnd
        call_event(evn, player)
    
    return
