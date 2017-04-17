##############################################################################
# The Edge of Mists random encounters
#
# Random encounters on the edge

label lbl_edge_randenc_errant:
    $ stranger = gen_random_person('human')    
    '[player.name] meets a confused Mist wanderer.'
    stranger "Where am I? What is this place? Can you help me, please?!"
        
    python:     
        options = CardsMaker()
        options.add_entry('errant_talk', edge_errant_options)
        options.add_entry('errant_stalk', edge_errant_options)
        options.add_entry('errant_engage', edge_errant_options)
        options.add_entry('errant_decieve', edge_errant_options)
        options.add_entry('flee', edge_option_cards)
        CardMenu(options.run()).show()
    hide card
    
    return

label lbl_edge_enc_flee(card):
    $ player.moral_action(target=stranger, activity='timid')     
    return

label lbl_edge_errant_talk(card):
    call lbl_communicate_act(stranger)
  
    return

label lbl_edge_enc_engage(card):
    $ player.moral_action(target=stranger, activity='ardent') 
    if player.check_your_privilege(stranger):
        '[stranger.name] tries to run away.'
        $ difficulty = stranger.physique
        $ result = core.skillcheck(player, 'physique', difficulty)         
        if result > 0:
            call lbl_edge_dominate(stranger)
        else:
            'Wanderer runs away.'
    else:
        call lbl_edge_errant_fight([player], [stranger]) 
        
    return

label lbl_edge_dominate(target):
    '[target.name] does not resist and surrenders.'
    target 'Fucking bastard... I yeld!'
    call lbl_captive(target)

    return

label lbl_edge_enc_decieve(card):
    python:
        player.moral_action(target=stranger, activity='chaotic') 
        difficulty = stranger.mind
        result = core.skillcheck(player, 'spirit', difficulty) 
        options = CardsMaker()

        if result > 0:
            txt = 'You deceived the confidence of the wanderer and got a chance to suddenly attack from behind.'
            options.add_entry('errant_subdue', edge_errant_options)
            options.add_entry('errant_backstab', edge_errant_options)
            options.add_entry('flee', edge_option_cards)

        else:
            txt = 'The stranger did not believe you and walkes away.'  
            options.add_entry('errant_engage', edge_errant_options)
            options.add_entry('flee', edge_option_cards)

    '[txt]'
    $ CardMenu(options.run()).show()
    hide card

    return

label lbl_edge_errant_fight(allies, enemies):
    python:
        fight = SimpleFight(allies, enemies)
        enemies = fight.get_enemies()
        winner = fight.get_winner()

    if winner == 'enemies':
        call edge_jbevent_yeld(None)

    return

label lbl_edge_errant_stalk(card):
    python:
        player.moral_action(target=stranger, activity='timid') 
        difficulty = stranger.agility
        result = core.skillcheck(player, 'agility', difficulty) 
        options = CardsMaker()

        if result > 0:
            txt = 'You stealhily sneaked to the wanderers back.'
            options.add_entry('errant_subdue', edge_errant_options)
            options.add_entry('errant_backstab', edge_errant_options)
            options.add_entry('flee', edge_option_cards)
        else:
            txt = 'Errant spots you sneaking!'
            options.add_entry('errant_engage', edge_errant_options)
            options.add_entry('flee', edge_option_cards)

    '[txt]'
    $ CardMenu(options.run()).show()
    hide card

    return

label lbl_edge_errant_subdue(card):
    'Gotcha!'
    $ player.enslave(stranger)
    return


label lbl_edge_errant_backstab(card):
    'Killed!'
    $ stranger.die()
    $ player.add_corpse(stranger)
    return
    



label lbl_edge_randenc_bandit:
    $ bandit = gen_raider_leader()  
    $ edge_guard.set_nickname("Raider") 
    '[player.name]ran into a group of thugs on the Edge of Mists.'
    bandit "Hey you! Get over here."
    python:
        options = CardsMaker()
        options.add_entry('raider_engage', edge_raider_options)
        options.add_entry('raider_flee', edge_raider_options)
        options.add_entry('raider_hide', edge_raider_options)        
        options.add_entry('raider_talk', edge_raider_options)
        options.add_entry('raider_yeld', edge_raider_options)
        CardMenu(options.run()).show()

    hide card     

    return
    
label lbl_edge_raider_fight(card):
    $ player.moral_action(target=bandit, activity='ardent') 
    python:
        allies = [player]
        enemies = [bandit, 'raider_club']
        fight = SimpleFight(allies, enemies)
        enemies = fight.get_enemies()
        winner = fight.get_winner()

    if winner == 'enemies':
        'Raiders sell you to slavedriver.'
        call lbl_edge_slave_auction(None)

    return

label lbl_edge_raider_flee(card):
    $ player.moral_action(target=bandit, activity='timid') 
    '[player.name] tries to run away.'
    $ difficulty = 1
    $ result = core.skillcheck(player, 'physique', difficulty)         
    if result < 1:
        'Too slow... the raiders caught up with [player.name].'
        call lbl_edge_raider_yeld(None)
    else:
        'That was close! But you manage to run away.'
        
    return

label lbl_edge_raider_hide(card):
    $ player.moral_action(target=bandit, activity='timid') 
    '[player.name] tries to hide away.'
    $ difficulty = 1
    $ result = core.skillcheck(player, 'agility', difficulty)         
    if result < 1:
        'No luck... the raiders have found [player.name].'
        call lbl_edge_raider_yeld(None)
    else:
        'That was close! But you manage to run away.'
        
    return

label lbl_edge_raider_talk(card):
    '[player.name]tries to be bold and dangerous. Perhaps they will be careful not to get involved in a fight.'
    $ difficulty = 5 - player.menace()
    $ result = core.skillcheck(player, 'spirit', difficulty)    
    player "Lokin for troubles, pal?"     
    if result < 1:
        bandit "I'll get you, motherfucker!"
        call lbl_edge_raider_fight(None)
    else:
        bandit "We cool... go your way, buddy."
        
    return

label lbl_edge_raider_yeld(card):
    player "Do not hurt me, please..."    
    bandit "Oh, we were not going to. Take off your clothes, you will not need it on the slave market."
    call lbl_edge_slave_auction(None)

    return