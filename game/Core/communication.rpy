##############################################################################
# Communication with NPCs
#

label lbl_communicate(target):
    target "I'm here"
    menu:
        'Gratify':
            call lbl_gratify(target)              
        'Cooperate':
            call lbl_cooperate(target)
        'Dominate':
            call lbl_dominate(target)
        'Nevermind':
            pass
    
    return

label lbl_dominate(target):
    menu:
        'Insult (charisma)':
            pass
                        
        'Back':
            call lbl_communicate(target)
    
    $ player.ap -= 1
    return
