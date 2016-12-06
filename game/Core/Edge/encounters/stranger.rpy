# Encounter type: 'stranger'

label lbl_edge_enc_stranger:
    
    'Stranger encounter'
    python:
        occupations = ['lumberjack', 'miner']# not full list
        stranger = gen_random_person('human', occupation=choice(occupations))
        combatant1 = DuelCombatant(player)
        combatant2 = DuelCombatant(stranger)
        fight = DuelEngine([combatant1], [combatant2], None)
        fight.start()
    return
