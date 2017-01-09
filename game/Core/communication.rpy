##############################################################################
# Communication with NPCs
#

label lbl_first_impression:
    visavis "You have only one chance for a first expression!"
    
    jump lbl_edge_manage
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

label lbl_gratify(target):
    menu:
        'Compliment (charisma)':
            python:
                morality = ['good', target]
                difficulty = core.token_difficulty(target, 'contribution', 'communication')
                skillcheck = core.skillcheck(player, 'charisma', ['power'], ['communication'], morality, difficulty, beneficiar=player)
                skillcheck = skillcheck.result
                result = core.gain_ctoken(skillcheck, target, 'contribution', tense=None, satisfy=['communication'])
                ## person, skill, morality=None, difficulty=0, tense=None, satisfy=None, beneficiar=None
            
            if result:
                'Bingo'
            else:
                'No chance'
                        
        'Back':
            call lbl_communicate(target)
    
    $ player.ap -= 1
    return
