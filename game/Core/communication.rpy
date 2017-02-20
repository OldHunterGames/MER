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
        'Be my garantor' if not garantor and visavis.stance(player).value > 0:
            visavis 'Ok. I will be your garantor.'
            $ garantor = visavis
                        
        'Hung out':
            call lbl_hungout              
        'Present':
            call lbl_present
        'Sex':
            $ SimpleSex((player, willing), (visavis, willing))
        'Take quest' if target.has_quest():
            call lbl_quests(target)
        'Nevermind':
            pass
    
    call lbl_edge_manage
    return

label lbl_conquest(target):
    python:
        visavis = target
        player.drain_energy()
        chance_to_rise = False
        if visavis.relations(player).harmony()[0] > visavis.stance(player).value + 1:
            chance_to_rise = True  
        visavis.use_token()
    menu:
        'Influence' if chance_to_rise:
            $ visavis.stance(player).value += 1
        'Dominance' if visavis.stance(player).value == 2:
            $ player.joy('authority', 5)
        'Hatred' if visavis.relations(player).congruence > -1:
            $ visavis.relations(player).change('congruence', '+')
        'Fervor' if visavis.relations(player).fervor < 1:
            $ visavis.relations(player).change('fervor', '+')       
        'Connection' if visavis.relations(player).distance > -1:
            $ visavis.relations(player).change('distance', '-')       
    return

label lbl_convention(target):
    python:
        visavis = target
        visavis.use_token()
        player.drain_energy()
        chance_to_rise = False
        if visavis.relations(player).harmony()[0] > visavis.stance(player).value + 1:
            chance_to_rise = True 
    menu:
        'Influence' if chance_to_rise:
            $ visavis.stance(player).value += 1
        'Control' if visavis.stance(player).value == 2:
            $ player.joy('ambition', 5)
        'Politesse' if visavis.relations(player).distance < 1:
            $ visavis.relations(player).change('distance', '+')    
        'Temperance' if visavis.relations(player).fervor > -1:
            $ visavis.relations(player).change('fervor', '-')       
        'Admiration' if visavis.relations(player).congruence < 1:
            $ visavis.relations(player).change('congruence', '-')
    return

label lbl_contribution(target):
    python:
        visavis = target
        visavis.use_token()
        player.drain_energy()
        chance_to_rise = False
        if visavis.relations(player).harmony()[0] > visavis.stance(player).value + 1:
            chance_to_rise = True 
    menu:        
        'Influence' if chance_to_rise:
            $ visavis.stance(player).value += 1
        'Fondness' if visavis.stance(player).value == 2:
            $ player.joy('communication', 5)
        'Admiration' if visavis.relations(player).congruence < 1:
            $ visavis.relations(player).change('congruence', '-')
        'Passion' if visavis.relations(player).fervor < 1:
            $ visavis.relations(player).change('fervor', '+')       
        'Connection' if visavis.relations(player).distance > -1:
            $ visavis.relations(player).change('distance', '-')       
    return

label lbl_antagonism(target):
    python:
        visavis = target
        visavis.use_token()
        player.drain_energy()
        visavis.stance(player).value -= 1
    visavis 'I hate you'
            
label lbl_first_impression:
    visavis "You have only one chance for a first expression!"
    menu:
        'Intimidate (ardent, spirit)':
            $ player.moral_action(target=visavis, activity='ardent') 
            $ dif = visavis.spirit
            $ result = core.skillcheck(player, 'spirit', dif)
            if result > 0:
                $ visavis.set_token('conquest')
            elif result < 0:
                $ visavis.set_token('antagonism')
        'Get to know (lawful, wisdom)':
            $ player.moral_action(target=visavis, orderliness='lawful') 
            $ dif = visavis.mind
            $ result = core.skillcheck(player, 'mind', dif)
            '[result]'
            if result > 0:
                $ visavis.set_token('convention')
            elif result < 0:
                $ visavis.set_token('antagonism')
        'Flatter (good, finesse)':
            $ player.moral_action(target=visavis, moral='good') 
            $ dif = visavis.agility
            $ result = core.skillcheck(player, 'agility', dif)
            if result > 0:
                $ visavis.set_token('contribution')
            elif result < 0:
                $ visavis.set_token('antagonism')
        'Sudden joke (chotic, random)':
            $ player.moral_action(target=visavis, orderliness='chaotic') 
            $ rnd = choice(['conquest', 'convention', 'contribution', 'antagonism', 'plus', 'minus']) 
            if rnd == 'plus':
                $ visavis.stance(player).value += 1
                'stance up'
            elif rnd == 'minus':
                $ visavis.stance(player).value -= 1
                'stance down'
            else:
                $ visavis.set_token(rnd)                
        'Mock (evil)':
            $ player.moral_action(target=visavis, moral='evil') 
            $ visavis.set_token('antagonism')
            $ player.satisfy_need('authority', 2)
        'Reticence (timid)':
            $ player.moral_action(target=visavis, activity='timid')
            'No changes' 
                
    hide card
    return
    
label lbl_hungout:
    menu:
        'Promenade (spirit, communication)' if 'promenade' not in visavis.communications_done:
            $ dif = 3 + visavis.relations(player).stability - visavis.need_level('communication')
            $ result = core.skillcheck(player, 'spirit', dif)
            if result > 0:
                $ player.satisfy_need('communication', 2)
                $ visavis.set_token('contribution')
                $ visavis.communications_done.append('promenade')                
            elif result = 0:
                player 'Waste of a time. Next time, maybe.'
            else:
                $ visavis.set_token('antagonism')     
                $ visavis.communications_done.append('promenade')                          
        'Booze (spirit, 1 bar)' if 'booze' not in visavis.communications_done and player.money > 0:
            $ player.remove_money -= 1
            $ dif = 3 + visavis.relations(player).stability - visavis.need_level('amusement')
            $ result = core.skillcheck(player, 'spirit', dif)
            if result > 0:
                $ visavis.communications_done.append('booze')  
                $ player.satisfy_need('amusement', 2)
                $ visavis.set_token('contribution')
            elif result = 0:
                $ player.satisfy_need('amusement', 2)
                'No progress in relationship. At least you get some amusement.' 
            else:
                $ visavis.communications_done.append('booze')  
                $ visavis.set_token('antagonism')                                
        'Dinner treat (spirit, 3 bars)' if 'dinner' not in visavis.communications_done:
            $ player.remove_money(3)
            $ dif = 3 + visavis.relations(player).stability - visavis.need_level('nutrition')
            $ result = core.skillcheck(player, 'spirit', dif)
            if result > 0:
                $ visavis.communications_done.append('dinner') 
                $ player.satisfy_need('nutrition', 4) 
                menu:
                    visavis 'Yum! What shoul we talk about?'
                    'Discuss serious matters':
                        $ visavis.set_token('convention')
                    "Let's just relax":
                        $ visavis.set_token('contribution')    
            elif result = 0:
                $ player.satisfy_need('nutrition', 4) 
                'No progress in relationship. The food is good newertheless.' 
            else:
                $ visavis.communications_done.append('dinner')  
                $ visavis.set_token('antagonism')                
        'Discuccion (wisdom, authority)' if 'discussion' not in visavis.communications_done:
            $ dif = 3 + visavis.relations(player).stability - visavis.need_level('authority')
            $ result = core.skillcheck(player, 'mind', dif)
            if result > 0:
                $ visavis.communications_done.append('discussion') 
                $ visavis.set_token('convention')
                $ player.satisfy_need('authority', 2) 
            elif result = 0:
                player 'Waste of a time. Next time, maybe.'
            else:
                $ visavis.communications_done.append('discussion') 
                $ visavis.set_token('antagonism')   
        'Impressive erudition (wisdom)' if 'impress' not in visavis.communications_done:
            $ visavis.communications_done.append('impress')
            $ dif = 2 + visavis.relations(player).stability
            $ result = core.skillcheck(player, 'mind', dif)
            if result > 0:
                $ visavis.set_token('convention')
            elif result = 0:
                visavis 'Not impressed.'
            else:
                $ visavis.set_token('antagonism')                                        
        'Carry favor (finesse)' if 'favor' not in visavis.communications_done:
            $ dif = 3 + visavis.relations(player).stability - visavis.need_level('authority')
            $ result = core.skillcheck(player, 'agility', dif)
            if result > 0:
                $ visavis.communications_done.append('favor') 
                menu:
                    visavis 'Oh, you so nice. Can I do something for you?'
                    'As a matter of fact, yes':
                        $ visavis.set_token('convention')
                    "The plasure is all mine":
                        $ visavis.set_token('contribution')    
            elif result = 0:
                visavis 'Yah-yah... wathever.' 
            else:
                $ visavis.communications_done.append('favor') 
                $ visavis.set_token('antagonism')                
        'Impressive prank (finesse)' if 'impress' not in visavis.communications_done:
            $ visavis.communications_done.append('impress')
            $ dif = 2 + visavis.relations(player).stability
            $ result = core.skillcheck(player, 'agility', dif)
            if result > 0:
                $ visavis.set_token('contribution')
            elif result = 0:
                visavis 'Not impressed.'
            else:
                $ visavis.set_token('antagonism')      
        'Dance (might, ardent)' if 'dance' not in visavis.communications_done:
            $ player.moral_action(activity='ardent') 
            $ dif = 3 + visavis.relations(player).stability - visavis.need_level('activity')
            $ result = core.skillcheck(player, 'physique', dif)
            if result > 0:
                $ visavis.communications_done.append('dance') 
                $ visavis.set_token('contribution')
                $ player.satisfy_need('activity', 2) 
            elif result = 0:
                player 'Waste of a time. Next time, maybe.'
            else:
                $ visavis.communications_done.append('dance') 
                $ visavis.set_token('antagonism')  
        'Impressive might (might)' if 'impress' not in visavis.communications_done:
            $ visavis.communications_done.append('impress')
            $ dif = 2 + visavis.relations(player).stability
            $ result = core.skillcheck(player, 'physique', dif)
            if result > 0:
                $ visavis.set_token('convention')
            elif result = 0:
                visavis 'Not impressed.'
            else:
                $ visavis.set_token('antagonism')        
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


label lbl_quests(target):
    python:
        quests = target.quests_to_give
        menu_items = []
        for i in quests:
            menu_items.append((i.name(), i))

        choice = renpy.display_menu(menu_items)
        description = choice.description()

    menu:
        '[description]'
        'Take this quest':
            $ core.quest_tracker.add_quest(choice(player))
        "Don't interrested":
            return
    return
