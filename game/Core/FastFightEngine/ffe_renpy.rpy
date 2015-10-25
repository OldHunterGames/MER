init 1 python:
    import sys
    sys.path.append(renpy.loader.transfn("Core/FastFightEngine/scripts"))
    
init 2 python:
    from ffe_engine import *
    
label ffe_start:
    $ fight = FFEngine([FFCombatant(game.actor)], [FFCombatant(ffe_enemy)])
    $ fight.start()
    show expression "interface/bg_base.jpg" as bg
    show screen ffe_battle
    call ffe_user_turn
    return

label ffe_user_turn:    
    $ act = fight.actor_move(ui.interact()[1])        
    call expression act
    return

label ffe_turn_resolution:
    $ act = fight.resolution_phase()
    call expression act
    return

label ffe_new_turn:
    "New Turn"
    call ffe_user_turn
    return

label ffe_defeat:
    hide screen ffe_battle
    "Defeat"
    return

label ffe_victory:
    hide screen ffe_battle
    "Victory"
    return  