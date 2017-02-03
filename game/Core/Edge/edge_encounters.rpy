##############################################################################
# The Edge of Mists random encounters
#
# Random encounters on the edge

label lbl_edge_randenc_errant:
    python:
        stranger = gen_random_person('human')    
    '[player.name] meets a confused Mist wanderer.'
    stranger "Where am I? What is this place? Can you help me, please?!"
    menu:
        'Engage':
            $ player.moral_action(target=stranger, activity='ardent') 
            if player.check_your_privilege(stranger):
                if stranger.armor_heavier_than(player):
                    call lbl_edge_dominate(stranger)
                else:
                    'Wanderer runs away.'
            else:
                call lbl_edge_errant_fight([player], [stranger]) 
        'Decieve': 
            $ player.moral_action(target=stranger, moral='evil')  
            $ motivation = player.motivation('charisma', ['order'], ['communication'], player, ['chaotic'])
            $ difficulty = stranger.mind - 2
            if difficulty < 0:
                $ difficulty = 0
            call lbl_skillcheck(player, 'charisma', motivation, difficulty)
            $ result = skillcheck.result
            if result > 0:
                '[player.name] are lulled wanderer and went behind him.'
                menu:
                    'Grapple':
                        $ player.moral_action(target=stranger, activity='ardent')   
                        $ fight = SimpleFight([player], [stranger])
                        
                    'Backstab':
                        pass                    
            else:
                'The stranger did not believe [player.name] and walkes away'  
                menu:
                    'Engage':         
                        $ player.moral_action(target=stranger, activity='ardent')   
                        $ fight = SimpleFight([player], [stranger])
                    'Newermind':
                        $ player.moral_action(target=stranger, activity='timid')
                     
        'Hide & stalk': 
            $ player.moral_action(target=stranger, activity='timid')  
            call lbl_edge_errant_stalk 
        'Talk': 
            call lbl_edge_errant_talk 
        'Flee': 
            $ player.moral_action(target=stranger, activity='timid')   
            'oooook'       

    return

label lbl_edge_errant_fight(allies, enemies):
    
    $ fight = SimpleFight(allies, enemies)
    
    $ enemies = fight.get_enemies()
    $ loot = fight.get_loot()
    
    return

label lbl_edge_errant_stalk:
    'You trying to stalk the confused wanderer stealthily. Cautious aproach. Finesse challenge. '
    python:
        dif = max(0, stranger.agility - player.agility)
        result = core.skillcheck(player, 'agility', dif)
    if result:
        'BINGO!'
    else:
        stranger 'Whos there?'
    
    return

    
label lbl_edge_randenc_bandit:
    python:
        enemy = make_combatant('weak_bandit')
        equip_combatant(enemy, 'weak_agile')
        enemy1 = DuelCombatant(enemy)       
    return
    
