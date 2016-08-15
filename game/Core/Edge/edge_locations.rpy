# Edge of Mists locations

label lbl_edge_shifting_mist(location=None):
    'Battle'
    python:
        ally1 = DuelCombatant(player)
        enemy1 = DuelCombatant(gen_random_person('human'))
        basic_deck = Deck(['clinch', 'hit_n_run', 'rage', 'outsmart', 'fallback', 'bite', 'headbutt', 'recoil', 'dodge', 'deep_breath', 'caution', 'bite', 'bite', 'light_strike', 'strike', 'powerful_strike', 'move', 'dash', 'fast_dash', 'rebound', 'block', 'hard_block'])
        ally1.set_deck(basic_deck)
        enemy1.set_deck(basic_deck)
        
        fight = DuelEngine([ally1],[enemy1], None)
        fight.start()
    return

label lbl_edge_grim_battlefield(location):

    return

label lbl_edge_outpost(location):
    call screen sc_universal_trade
    return