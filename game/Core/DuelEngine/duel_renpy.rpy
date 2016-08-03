init 1 python:
    import sys
    sys.path.append(renpy.loader.transfn("Core/FastFightEngine/scripts"))
    
init 2 python:
    from ffe_engine import *
    
label duel_start:
    $ fight = FFEngine([FFCombatant(game.actor)], [FFCombatant(ffe_enemy)])
    $ fight.start()
    show expression "interface/bg_base.jpg" as bg
    show screen ffe_battle
    call ffe_user_turn
    return

label duel_user_turn:    
    $ act = fight.actor_move(ui.interact()[1])        
    call expression act
    return

label duel_turn_resolution:
    $ act = fight.resolution_phase()
    call expression act
    return

label duel_new_turn:
    "New Turn"
    call ffe_user_turn
    return

label duel_defeat:
    hide screen ffe_battle
    "Defeat"
    return

label duel_victory:
    hide screen ffe_battle
    "Victory"
    return  