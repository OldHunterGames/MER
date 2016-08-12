init python:
    edge_locations = {
        'outpost': __('House {0} outpost'),
        'grim_battlefield': __('grim battlefield'),
        'crimson_pit': __('crimson pit'),
        'junk_yard': __('junk yard'),
        'ruined_factory': __('ruined factory'),
        'dying_grove': __('dying grove'),
        'hazy_marsh': __('hazy marsh'),
        'echoing hills': __('echoing hills'),
        'outworld_ruines': __('outworld ruines'),
        'raider_encampment': __('raiders encampment'),
        'charity_mission': __('House {0} charity mission'),
        'shifting_mist': __('Shifting mist')
        }
    
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
        
        }

    house_names = {'kamira': __('Kamira'),
                 'serpis': __('Serpis'), 
                 'corvus': __('Corvus'),
                 'taurus':  __('Taurus')}


label lbl_edge_shifting_mist(location=None):
    return

label lbl_edge_grim_battlefield(location):

    return

label lbl_edge_outpost(location):
    call screen sc_universal_trade
    return
