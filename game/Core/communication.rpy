##############################################################################
# Communication with NPCs
#

label lbl_communicate(target):
    $ visavis = target
    if not player.relations(visavis).first_impression:
        $ player.relations(visavis).first_impression = True
        $ player.drain_energy()
        jump lbl_first_impression

    $ target.say_phrase('hello')
    python:     
        options = CardsMaker()
        #if not garantor and visavis.relations(player).stance > 0:
        #    options.add_entry('comm_garantor', edge_option_cards['comm_garantor'])
        options.add_entry('com_hungout', edge_option_cards['com_hungout'])
        #options.add_entry('com_present', edge_option_cards['com_present'])
        if target.has_available_quests(player):
            options.add_entry('com_takequest', edge_option_cards['com_takequest'])
        if target.obligation:
            options.add_entry('com_obligation', edge_option_cards['com_obligation'])
        if target == edge_slaver:
            options.add_entry('spc_become_slave', edge_option_cards['spc_become_slave'])    
        if target.quest_completed(player): 
            options.add_entry('com_quest_completed', edge_option_cards['com_quest_completed'])        
        options.add_entry('nevermind', edge_option_cards['nevermind'])  
        CardMenu(options.run()).show()
                
    hide card
    call lbl_edge_manage
    return

label lbl_comm_garantor(card):
    visavis 'Ok. I will be your garantor.'
    $ garantor = visavis    
    
    return

label lbl_edge_comm_call_quest(card):
    call lbl_quests(visavis)
    
    return

label lbl_edge_comm_obligation(card):
    $ CardMenu(visavis.reward.run()).show()
    hide card
    return
    
label lbl_edge_comm_nevermind(card):
    pass
    
    return
    
label lbl_edge_comm_complete_quest(card):

    call lbl_edge_comm_obligation
    
    return

label lbl_edge_comm_present(card):
    menu:
                        
        'Back':
            jump lbl_communicate
    
    $ player.drain_energy()

    return    

    
label lbl_edge_reward_sparks(card):
    python:
        flag = False
        for item in player.items:
            if item.id == 'jewel':
                player.remove_item(item)
                sparkgem = create_item('sparkgem', 'assesory')
                player.add_item(sparkgem)
                flag = True
                break
    if flag:
        'Got sparks'
    else:
        'You need gem'

    return
        
label lbl_edge_reward_banknotes(card):
    '[player.name] got bundle of banknotes.'
    $ notes = create_item('notes', 'treasure')
    $ player.add_item(notes)

    return
    
label lbl_edge_reward_bars(card):
    '[player.name] got 100 bars'
    $ player.money += 100
    
    return

label lbl_edge_reward_relations(card):  
    '[visavis.name] is now more inclined to cooperate.'
    $ player.relations(visavis).stance += 1
    
    return
             
label lbl_quests(card):
    python:
        quests = visavis.available_quests()
        if len(quests) > 0:
            quest = choice(quests)
            description = quest.description()
            core.quest_tracker.add_quest(quest)
        else:
            quest = None
    
    if quest is not None:
        visavis '[description]'
        $ player.drain_energy()
    else:
        visavis 'I have no quests for you'
    
    return
            
label lbl_first_impression:
    visavis "You have only one chance for a first expression!"
    
    python:     
        options = CardsMaker()
        options.add_entry('fi_intimidate', edge_option_cards['fi_intimidate'])
        options.add_entry('fi_getknow', edge_option_cards['fi_getknow'])
        options.add_entry('fi_flatter', edge_option_cards['fi_flatter'])
        options.add_entry('fi_joke', edge_option_cards['fi_joke'])
        options.add_entry('fi_mock', edge_option_cards['fi_mock'])
        options.add_entry('fi_reticence', edge_option_cards['fi_reticence'])        
        CardMenu(options.run()).show()
                
    hide card
    return

label lbl_first_impression_intimidate(card):
    $ player.moral_action(target=visavis, activity='ardent') 
    $ dif = visavis.spirit
    $ result = core.skillcheck(player, 'spirit', dif)
    if result > 0:
        $ visavis.set_token('conquest')
    elif result < 0:
        $ visavis.set_token('antagonism')    
            
    return

label lbl_first_impression_getknow(card):
    $ player.moral_action(target=visavis, orderliness='lawful') 
    $ dif = visavis.mind
    $ result = core.skillcheck(player, 'mind', dif)
    '[result]'
    if result > 0:
        $ visavis.set_token('convention')
    elif result < 0:
        $ visavis.set_token('antagonism')    
    
    return

label lbl_first_impression_flatter(card):
    $ player.moral_action(target=visavis, moral='good') 
    $ dif = visavis.agility
    $ result = core.skillcheck(player, 'agility', dif)
    if result > 0:
        $ visavis.set_token('contribution')
    elif result < 0:
        $ visavis.set_token('antagonism')    
    
    return

label lbl_first_impression_joke(card):
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
    
    return

label lbl_first_impression_mock(card):
    $ player.moral_action(target=visavis, moral='evil') 
    $ visavis.set_token('antagonism')
    $ player.satisfy_need('authority', 2)    
    
    return

label lbl_first_impression_reticence(card):
    $ player.moral_action(target=visavis, activity='timid')    
    
    return        

label lbl_edge_comm_hungout(card):
    
    python:     
        options = CardsMaker()        
        if 'promenade' not in visavis.communications_done:
            options.add_entry('ho_promenade', edge_option_cards['ho_promenade'])
        if 'booze' not in visavis.communications_done and player.money > 0:
            options.add_entry('ho_booze', edge_option_cards['ho_booze'])
        if 'dinner' not in visavis.communications_done and player.money > 2:
            options.add_entry('ho_dinner', edge_option_cards['ho_dinner'])
        if 'discussion' not in visavis.communications_done:
            options.add_entry('ho_discussion', edge_option_cards['ho_discussion'])
        if 'impress' not in visavis.communications_done:
            options.add_entry('ho_erudition', edge_option_cards['ho_erudition'])
            options.add_entry('ho_prank', edge_option_cards['ho_prank'])
            options.add_entry('ho_might', edge_option_cards['ho_might'])
        if 'favor' not in visavis.communications_done:
            options.add_entry('ho_favor', edge_option_cards['ho_favor'])        
        if 'dance' not in visavis.communications_done:
            options.add_entry('ho_dance', edge_option_cards['ho_dance'])
        options.add_entry('makelove', edge_option_cards['makelove'])    
        options.add_entry('nevermind', edge_option_cards['nevermind'])          
        CardMenu(options.run()).show()

    $ player.drain_energy()
    hide card

    return

label lbl_edge_ho_promenade(card):
    $ dif = 2 + visavis.spirit - visavis.need_level('communication')
    $ result = core.skillcheck(player, 'spirit', dif)
    if result > 0:
        $ player.satisfy_need('communication', 2)
        $ visavis.set_token('contribution')
        $ visavis.communications_done.append('promenade')                
    elif result == 0:
        player 'Waste of a time. Next time, maybe.'
    else:
        $ visavis.set_token('antagonism')     
        $ visavis.communications_done.append('promenade')         
    return

label lbl_edge_ho_might(card):
    $ visavis.communications_done.append('impress')
    $ dif = visavis.phisique
    $ result = core.skillcheck(player, 'physique', dif)
    if result > 0:
        $ visavis.set_token('convention')
    elif result == 0:
        visavis 'Not impressed.'
    else:
        $ visavis.set_token('antagonism')   
                    
    return

label lbl_edge_ho_dance(card):
    $ player.moral_action(activity='ardent') 
    $ dif = 2 + visavis.phisique - visavis.need_level('activity')
    $ result = core.skillcheck(player, 'physique', dif)
    if result > 0:
        $ visavis.communications_done.append('dance') 
        $ visavis.set_token('contribution')
        $ player.satisfy_need('activity', 2) 
    elif result == 0:
        player 'Waste of a time. Next time, maybe.'
    else:
        $ visavis.communications_done.append('dance') 
        $ visavis.set_token('antagonism')      
    return

label lbl_edge_ho_prank(card):
    $ visavis.communications_done.append('impress')
    $ dif = visavis.agility
    $ result = core.skillcheck(player, 'agility', dif)
    if result > 0:
        $ visavis.set_token('contribution')
    elif result == 0:
        visavis 'Not impressed.'
    else:
        $ visavis.set_token('antagonism')        
    return

label lbl_edge_ho_favor(card):
    $ dif = 2 + visavis.agility - visavis.need_level('authority')
    $ result = core.skillcheck(player, 'agility', dif)
    if result > 0:
        $ visavis.communications_done.append('favor') 
        menu:
            visavis 'Oh, you so nice. Can I do something for you?'
            'As a matter of fact, yes':
                $ visavis.set_token('convention')
            "The plasure is all mine":
                $ visavis.set_token('contribution')    
    elif result == 0:
        visavis 'Yah-yah... wathever.' 
    else:
        $ visavis.communications_done.append('favor') 
        $ visavis.set_token('antagonism')       
    return

label lbl_edge_ho_erudition(card):
    $ visavis.communications_done.append('impress')
    $ dif = visavis.mind
    $ result = core.skillcheck(player, 'mind', dif)
    if result > 0:
        $ visavis.set_token('convention')
    elif result = 0:
        visavis 'Not impressed.'
    else:
        $ visavis.set_token('antagonism')      
    return

label lbl_edge_ho_discussion(card):
    $ dif = 2 + visavis.mind - visavis.need_level('authority')
    $ result = core.skillcheck(player, 'mind', dif)
    if result > 0:
        $ visavis.communications_done.append('discussion') 
        $ visavis.set_token('convention')
        $ player.satisfy_need('authority', 2) 
    elif result == 0:
        player 'Waste of a time. Next time, maybe.'
    else:
        $ visavis.communications_done.append('discussion') 
        $ visavis.set_token('antagonism')       
    return

label lbl_edge_ho_dinner(card):
    $ player.remove_money(3)
    $ dif = 2 + visavis.spirit - visavis.need_level('nutrition')
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
    elif result == 0:
        $ player.satisfy_need('nutrition', 4) 
        'No progress in relationship. The food is good newertheless.' 
    else:
        $ visavis.communications_done.append('dinner')  
        $ visavis.set_token('antagonism')          
    return

label lbl_edge_ho_booze(card):
    $ player.remove_money -= 1
    $ dif = 2 + visavis.spirit - visavis.need_level('amusement')
    $ result = core.skillcheck(player, 'spirit', dif)
    if result > 0:
        $ visavis.communications_done.append('booze')  
        $ player.satisfy_need('amusement', 2)
        $ visavis.set_token('contribution')
    elif result == 0:
        $ player.satisfy_need('amusement', 2)
        'No progress in relationship. At least you get some amusement.' 
    else:
        $ visavis.communications_done.append('booze')  
        $ visavis.set_token('antagonism')            
    return

label lbl_makelove(card):
    $ SimpleSex((player, 'controled'), (visavis, 'wishful'))
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
    return
