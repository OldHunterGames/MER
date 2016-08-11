init python:
    edge_locations = {
        'grim_battlefield': __('grim battlefield'),
        'crimson_pit': __('crimson pit'),
        'junk_yard': __('junk yard'),
        'ruined_factory': __('ruined factory'),
        'dying_grove': __('dying grove'),
        'hazy_marsh': __('hazy marsh'),
        'echoing hills': __('echoing hills'),
        'outworld_ruines': __('outworld ruines'),
        'raider_encampment': __('raiders encampment'),
        'charity_mission': __('charity mission'),
        }
    
    edge_denotation = {
        'idle': __('idle'),
        'explore': [__('explore'), edge.explore],
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


label lbl_edge_shifting_mist(location):
    $ explore = edge_denotation['explore']
    $ menu_list = [(explore[0], explore[1])]
    $ choice = renpy.display_menu(menu_list)
    $ choice()
    return

label lbl_edge_grim_battlefield(location):
    
    return
