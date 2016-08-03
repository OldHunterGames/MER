init 1 python:
    import sys
    sys.path.append(renpy.loader.transfn("Core/DuelEngine/scripts"))
    
init 2 python:
    from duel_engine import *
    
label duel_start:
    $ fight = DuelEngine([DuelCombatant(game.actor)], [DuelCombatant(duel_enemy)])
    $ fight.start()
    show expression "interface/bg_base.jpg" as bg
    show screen duel_battle
    call duel_user_turn
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
    call duel_user_turn
    return

label duel_defeat:
    hide screen duel_battle
    "Defeat"
    return

label duel_victory:
    hide screen duel_battle
    "Victory"
    return  