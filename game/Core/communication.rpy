##############################################################################
# Communication with NPCs
#

label lbl_captive(target):
    python: 
        visavis = target
        target.say_phrase('captive_hello')
        options = CardsMaker()
        if visavis.has_items():
            options.add_entry('captive_loot', edge_captive_options)     
        if 'slaver' in edge.options:
            options.add_entry('captive_sell', edge_captive_options)  
        options.add_entry('captive_rape', edge_captive_options)          
        options.add_entry('captive_slay', edge_captive_options)  
        options.add_entry('captive_cannibalise', edge_captive_options)          
        options.add_entry('captive_capture', edge_captive_options)     
        options.add_entry('captive_release', edge_captive_options)  
        CardMenu(options.run()).show()                
    hide card
    return

label lbl_communicate(target):
    if target in player.slaves.slaves():
        call lbl_captive(target)
    else:
        call lbl_communicate_act(target)

    return

label lbl_communicate_act(target):
    $ player.drain_energy()
    $ visavis = target
    if not player.relations(visavis).first_impression:
        $ player.relations(visavis).first_impression = True
        jump lbl_first_impression

    $ target.say_phrase('hello')
    python:     
        options = CardsMaker()
        options.add_entry('com_hungout', edge_option_cards)
        if target.has_available_quests(player):
            options.add_entry('com_takequest', edge_option_cards)
        if target.obligation:
            options.add_entry('com_obligation', edge_option_cards)
        if target == edge_slaver:
            options.add_entry('spc_become_slave', edge_option_cards)    
        elif target == edge_junker:
            options.add_entry('spc_sellall', edge_option_cards)    
        elif target == edge_recruiter:
            if not fate:
                options.add_entry('spc_recruiter_bond', edge_option_cards)  
            options.add_entry('spc_recruiter_citisen', edge_option_cards)  
        elif target != edge_guard:
            options.add_entry('spc_enslave', edge_option_cards)   
        if target.quest_completed(player): 
            options.add_entry('com_quest_completed', edge_option_cards)        
        options.add_entry('nevermind', edge_option_cards)  
        cards = options.run()
        cards.extend(target.get_interactions())
        CardMenu(cards).show()
                
    hide card
    return

label lbl_edge_enslave(card):
    $ dif = visavis.spirit
    $ result = core.skillcheck(player, 'spirit', dif)
    if result > 0:
        visavis "Yeah... I'm tired of this surviving. Maybe you right, bring me to a slaver."
        $ player.enslave(visavis)
        "[visavis.name] is your captive now."
    elif result < 0:
        visavis "No way! I'll better be free."
    return

label lbl_edge_spc_sellall(card):
    $ SellItems(player, CardMenu).run()
    return

label lbl_comm_garantor(card):
    visavis 'Ok. I will be your garantor.'
    $ garantor = visavis    
    
    return

label lbl_edge_comm_call_quest(card):
    call lbl_quests(visavis)
    
    return

label lbl_edge_comm_obligation(card):
    $ CardMenu(visavis.rewards.run()).show()
    hide card
    return
    
label lbl_edge_comm_nevermind(card):
    pass
    
    return
    
label lbl_edge_comm_complete_quest(card):
    $ core.quest_tracker.finish_quest(visavis.active_quest, player)
    call lbl_edge_comm_obligation(card)
    
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
        for item in player.all_items():
            if item.id == 'jewel':
                player.remove_item(item)
                sparkgem = create_item('sparkgem', 'accessory')
                player.add_item(sparkgem)
                flag = True
                break

    if flag:
        $ visavis.obligation = False
        'Jewel infused with Sparks of Creation turns to a shiny sparkgem!'
    else:
        'You need a clear gem (jewel for instance) to infuse it with Sparks.'

    return
        
label lbl_edge_reward_banknotes(card):
    $ visavis.obligation = False
    '[player.name] got bundle of banknotes.'
    $ notes = create_item('notes', 'treasure')
    $ player.add_item(notes)

    return
    
label lbl_edge_reward_bars(card):
    $ visavis.obligation = False
    '[player.name] got 100 bars'
    $ player.money += 100
    
    return

label lbl_edge_reward_relations(card):  
    $ visavis.obligation = False
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
        options.add_entry('fi_intimidate', edge_option_cards)
        options.add_entry('fi_getknow', edge_option_cards)
        options.add_entry('fi_flatter', edge_option_cards)
        options.add_entry('fi_joke', edge_option_cards)
        options.add_entry('fi_mock', edge_option_cards)
        options.add_entry('fi_reticence', edge_option_cards)        
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
        $ visavis.relations(player).stance += 1
        'stance up'
    elif rnd == 'minus':
        $ visavis.relations(player).stance -= 1
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
            options.add_entry('ho_promenade', edge_option_cards)
        if 'booze' not in visavis.communications_done and player.money > 0:
            options.add_entry('ho_booze', edge_option_cards)
        if 'dinner' not in visavis.communications_done and player.money > 2:
            options.add_entry('ho_dinner', edge_option_cards)
        if 'discussion' not in visavis.communications_done:
            options.add_entry('ho_discussion', edge_option_cards)
        if 'impress' not in visavis.communications_done:
            options.add_entry('ho_erudition', edge_option_cards)
            options.add_entry('ho_prank', edge_option_cards)
            options.add_entry('ho_might', edge_option_cards)
        if 'favor' not in visavis.communications_done:
            options.add_entry('ho_favor', edge_option_cards)        
        if 'dance' not in visavis.communications_done:
            options.add_entry('ho_dance', edge_option_cards)
        options.add_entry('makelove', edge_option_cards)    
        options.add_entry('nevermind', edge_option_cards)          
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
    $ SimpleSex((player, 'controlled'), (visavis, 'wishful'))
    return

label lbl_edge_duel(card):
    python:
        fight = SimpleFight([player], [visavis], friendly_fight=True)
        enemies = fight.get_enemies()

    return
    

label lbl_edge_captive_sell(card):
    python:
        price = visavis.get_price()
        if visavis in player.slaves.slaves():
            player.remove_slave()
        player.add_money(price)
        player.forget_person(visavis)
    edge_slaver "I'll give you [price] bars for this slave."

    return    

label lbl_edge_captive_capture(card):
    python:
        slaver = player
        slaver.enslave(visavis)
    return

label lbl_edge_captive_loot(card):
    python:
        loot = ''
        for item in visavis.all_items():
            loot += item.colored_name()
            loot += ' '

        visavis.transfer_all(player)
    
    'looted: [loot]'
    call lbl_captive(visavis)
    return

label lbl_edge_captive_rape(card):
    python:
        sex = SimpleSex((player, 'controlled'), (visavis, 'forced'))
        result = sex.get_results()

    call lbl_captive(visavis)
    return

label lbl_edge_captive_slay(card):
    "slayed"
    python:
        visavis.die()
        player.add_corpse(visavis)

    return

label lbl_edge_captive_cannibalise(card):
    "[player.name] slays [visavis.name] to roast its meat on a demonblood fire."
    player "Munch-munch... At last I'm full"
    python:
        visavis.die()
        player.add_corpse(visavis)
        player.eat_corpse(visavis)

    return

label lbl_edge_captive_release(card):
    python:
        if visavis in player.slaves.slaves():
            player.remove_slave()

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
