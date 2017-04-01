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
    stranger "Blah"
  
    return

label lbl_edge_enc_engage(card):
    $ player.moral_action(target=stranger, activity='ardent') 
    if player.check_your_privilege(stranger):
        if stranger.armor_heavier_than(player):
            call lbl_edge_dominate(stranger)
        else:
            'Wanderer runs away.'
    else:
        call lbl_edge_errant_fight([player], [stranger]) 
        
    return

label lbl_edge_enc_decieve(card):
    python:
        player.moral_action(target=stranger, activity='chaotic') 
        difficulty = stranger.mind
        result = core.skillcheck(player, 'spirit', difficulty) 
        options = CardsMaker()

        if result > 0:
            txt = '[player.name] deceived the confidence of the wanderer and got a chance to suddenly attack from behind.'
            options.add_entry('errant_subdue', edge_errant_options)
            options.add_entry('errant_backstab', edge_errant_options)
            options.add_entry('flee', edge_option_cards)

        else:
            txt = 'The stranger did not believe [player.name] and walkes away.'  
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
        loot = fight.get_loot()

    return

label lbl_edge_errant_stalk:
    python:
        player.moral_action(target=stranger, activity='timid') 
        difficulty = stranger.agility
        result = core.skillcheck(player, 'agility', difficulty) 
        options = CardsMaker()

        if result > 0:
            txt = '[player.name] stealhily sneaked to the wanderers back.'
            options.add_entry('errant_subdue', edge_errant_options)
            options.add_entry('errant_backstab', edge_errant_options)
            options.add_entry('flee', edge_option_cards)
        else:
            txt = 'Errant spots [player.name] sneaking!'
            options.add_entry('errant_engage', edge_errant_options)
            options.add_entry('flee', edge_errant_options)

    '[txt]'
    $ CardMenu(options.run()).show()
    hide card

    return




    
label lbl_edge_randenc_bandit:
    python:
        enemy = make_combatant('weak_bandit')
        equip_combatant(enemy, 'weak_agile')
        enemy1 = DuelCombatant(enemy)       
    return
    



