##############################################################################
# The Edge of Mists random encounters
#
# Random encounters on the edge

label lbl_edge_randenc_errant:
    python:
        # enemy_weapon = Weapon('twohand', 'subdual', quality=1)
        # enemy_armor = Armor('heavy_armor', quality=1)
        # enemy.main_hand = enemy_weapon
        # enemy.armor = enemy_armor
        enemy = gen_random_person('human')
        enemy1 = DuelCombatant(enemy)

    return
    
label lbl_edge_randenc_bandit:
    python:
        enemy = make_combatant('weak_bandit')
        equip_combatant(enemy, 'weak_agile')
        enemy1 = DuelCombatant(enemy)       
    return
    