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
            $ player.moral_action('ardent', stranger)   
            call lbl_simple_fight([player], [stranger]) 
        'Decieve': 
            $ player.moral_action('evil', stranger)  
            call lbl_edge_errant_decive 
        'Hide & stalk': 
            $ player.moral_action('timid', stranger)  
            call lbl_edge_errant_stalk 
        'Talk': 
            call lbl_edge_errant_talk 
        'Flee': 
            pass         
            $ player.moral_action('timid', stranger)          

    return
    
label lbl_edge_randenc_bandit:
    python:
        enemy = make_combatant('weak_bandit')
        equip_combatant(enemy, 'weak_agile')
        enemy1 = DuelCombatant(enemy)       
    return
    
