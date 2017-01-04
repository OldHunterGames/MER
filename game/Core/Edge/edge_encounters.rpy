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
        'Fight':
            call lbl_simple_fight([player], [stranger])
        'Flee':
            pass        

    return
    
label lbl_edge_randenc_bandit:
    python:
        enemy = make_combatant('weak_bandit')
        equip_combatant(enemy, 'weak_agile')
        enemy1 = DuelCombatant(enemy)       
    return
    
