##############################################################################
# Communication with NPCs
#

label lbl_first_impression:
    visavis "You have only one chance for a first expression!"
    menu:
        'Intimidate (ardent, spirit)':
            $ player.moral_action('ardent', visavis) 
            $ dif = visavis.spirit
            $ result = core.skillcheck(player, 'spirit', dif)
            if result:
                $ visavis.set_token('conquest')
                'Conquest'
            else:
                $ visavis.set_token('antagonism')
                'Antagonism'
        'Get to know (lawful, wisdom)':
            $ player.moral_action('lawful', visavis) 
            $ dif = visavis.mind
            $ result = core.skillcheck(player, 'mind', dif)
            if result:
                $ visavis.set_token('convention')
                'Convention'
            else:
                $ visavis.set_token('antagonism')
                'Antagonism'
        'Flatter (good, finesse)':
            $ player.moral_action('good', visavis) 
            $ dif = visavis.finesse
            $ result = core.skillcheck(player, 'agility', dif)
            if result:
                $ visavis.set_token('contribution')
                'Contribution'
            else:
                $ visavis.set_token('antagonism')
                'Antagonism'
        'Sudden joke (chotic, random)':
            $ player.moral_action('chaotic', visavis) 
        'Mock (evil)':
            $ player.moral_action('evil', visavis) 
            $ visavis.set_token('antagonism')
            $ player.joy('authority', 1)
        'Reticence (timid)':
            $ player.moral_action('timid', visavis)
            'No changes' 
                
    hide over
    return

label lbl_communicate(target):
    $ visavis = target
    if not player.relations(visavis).first_impression:
        $ player.relations(visavis).first_impression = True
        $ player.drain_energy()
        jump lbl_first_impression

    target "I'm here"
    menu:
        'Gratify':
            call lbl_gratify              
        'Cooperate':
            call lbl_cooperate
        'Dominate':
            call lbl_dominate
        'Nevermind':
            pass
    
    call lbl_edge_manage
    return

label lbl_dominate:
    menu:
        'Intimidate (spirit)':
            pass
                        
        'Back':
            jump lbl_communicate

    $ player.drain_energy()
    return

label lbl_cooperate:
    menu:
        'Get to know (wisdom)':
            pass
                        
        'Back':
            jump lbl_communicate
    
    $ player.drain_energy()
    return
    
label lbl_gratify:
    menu:
        'Flatter (finesse)':
            python:
                player.moral_action('good', visavis) 
                core.gain_ctoken(visavis, player, 'contribution', 'agility')
                        
        'Back':
            jump lbl_communicate
    
    $ player.drain_energy()
    return
