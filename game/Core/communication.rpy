##############################################################################
# Communication with NPCs
#

label lbl_communicate(target):
    $ visavis = target
    if not player.relations(visavis).first_impression:
        $ player.relations(visavis).first_impression = True
        $ player.drain_energy()
        jump lbl_first_impression

    target "I'm here"
    menu:
        'Hung out':
            call lbl_hungout              
        'Present':
            call lbl_present
        'Nevermind':
            pass
    
    call lbl_edge_manage
    return

label lbl_conquest(target):
    python:
        visavis = target
        player.drain_energy()
        chance_to_rise = False
        if person.relations(person).harmony > visavis.stance(player).value + 1
            chance_to_rise = True  
    
    'Influence' if  chance_to_rise:
        $ visavis.stance(player).value += 1
    'Dominance' if visavis.stance(player).value = 2:
        $ player.joy('authority', 5)
    'Hatred' if visavis.relations(player).congruence > -1:
        $ visavis.relations(player).change('congruence', '-')
    'Fervor' if visavis.relations(player).fervor < 1:
        $ visavis.relations(player).change('fervor', '+')       
    'Connection' if visavis.relations(player).distance > -1:
        $ visavis.relations(player).change('distance', '-')       
    return

label lbl_convention(target):
    python:
        visavis = target
        player.drain_energy()
        chance_to_rise = False
        if person.relations(person).harmony > visavis.stance(player).value + 1
            chance_to_rise = True 
            
    'Influence' if chance_to_rise:
        $ visavis.stance(player).value += 1
    'Control' if visavis.stance(player).value = 2:
        $ player.joy('ambition', 5)
    'Politesse' if visavis.relations(player).distance < 1:
        $ visavis.relations(player).change('distance', '+')    
    'Temperance' if visavis.relations(player).fervor > -1:
        $ visavis.relations(player).change('fervor', '-')       
    'Admiration' if visavis.relations(player).congruence < 1:
        $ visavis.relations(player).change('congruence', '+')
    return

label lbl_contribution(target):
    python:
        visavis = target
        player.drain_energy()
        chance_to_rise = False
        if person.relations(person).harmony > visavis.stance(player).value + 1
            chance_to_rise = True 
            
    'Influence' if chance_to_rise:
        $ visavis.stance(player).value += 1
    'Fondness' if visavis.stance(player).value = 2:
        $ player.joy('communication', 5)
    'Admiration' if visavis.relations(player).congruence < 1:
        $ visavis.relations(player).change('congruence', '+')
    'Passion' if visavis.relations(player).fervor < 1:
        $ visavis.relations(player).change('fervor', '+')       
    'Connection' if visavis.relations(player).distance > -1:
        $ visavis.relations(player).change('distance', '-')       
    return

label lbl_antagonism(target):
    python:
        visavis = target
        player.drain_energy()
        visavis.stance(player).value -= 1
    visavis 'I hate you'
            
label lbl_first_impression:
    visavis "You have only one chance for a first expression!"
    menu:
        'Intimidate (ardent, spirit)':
            $ player.moral_action('ardent', visavis) 
            $ dif = visavis.spirit
            $ result = core.skillcheck(player, 'spirit', dif)
            if result:
                $ visavis.set_token('conquest')
            else:
                $ visavis.set_token('antagonism')
        'Get to know (lawful, wisdom)':
            $ player.moral_action('lawful', visavis) 
            $ dif = visavis.mind
            $ result = core.skillcheck(player, 'mind', dif)
            if result:
                $ visavis.set_token('convention')
            else:
                $ visavis.set_token('antagonism')
        'Flatter (good, finesse)':
            $ player.moral_action('good', visavis) 
            $ dif = visavis.finesse
            $ result = core.skillcheck(player, 'agility', dif)
            if result:
                $ visavis.set_token('contribution')
            else:
                $ visavis.set_token('antagonism')
        'Sudden joke (chotic, random)':
            $ player.moral_action('chaotic', visavis) 
            $ rnd = choice(['conquest', 'convention', 'contribution', 'antagonism', 'plus', 'minus']) 
            if rnd == 'plus':
                $ visavis.stance(player).value += 1
                'stance up'
            elif rnd = 'minus':
                $ visavis.stance(player).value -= 1
                'stance down'
            else:
                $ visavis.set_token(rnd)                
            'Result = [rnd]'
        'Mock (evil)':
            $ player.moral_action('evil', visavis) 
            $ visavis.set_token('antagonism')
            $ player.joy('authority', 2)
        'Reticence (timid)':
            $ player.moral_action('timid', visavis)
            'No changes' 
                
    hide card
    return
    
label lbl_hungout:
    menu:
        'Promenade (spirit)' if 'promenade' not in visavis.communications_done:
            pass
        'Booze (spirit, 1 bar)' if 'booze' not in visavis.communications_done:
            pass   
        'Dinner treat (spirit, 3 bars)' if 'dinner' not in visavis.communications_done:
            pass     
        'Discuccion (wisdom)' if 'discussion' not in visavis.communications_done:
            pass             
        'Impressive erudition (wisdom)' if 'impress' not in visavis.communications_done:
            pass                                     
        'Carry favor (finesse)' if 'favor' not in visavis.communications_done:
            pass
        'Impressive prank (finesse)' if 'impress' not in visavis.communications_done:
            pass    
        'Dance (might)' if 'dance' not in visavis.communications_done:
            pass   
        'Impressive might (might)' if 'impress' not in visavis.communications_done:
            pass                
        'Back':
            jump lbl_communicate

    $ player.drain_energy()
    return

label lbl_present:
    menu:
        'Get to know (wisdom)':
            pass
                        
        'Back':
            jump lbl_communicate
    
    $ player.drain_energy()
    return    
    return    
