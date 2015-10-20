# Fast Sex Engine RenPy scripts
init 1 python:
    import sys
    sys.path.append(renpy.loader.transfn("Core/FastSexEngine/scripts"))
    
init 2 python:
    from fse_engine import *
    
label fse_start:
    $ sex = FSEngine((FSECombatant(game.actor), FSECombatant(enemy)))
    $ sex.start()
    show expression "interface/bg_base.jpg" as bg
    show screen fse_main
    call user_turn
    return

label user_turn:    
    $ location_to_call = sex.render_input(ui.interact())
    call expression location_to_call
    return
    
label resolution_phase:
    $ location_to_call = sex.resolution()
    call expression location_to_call
    return

label you_win:
    hide screen fse_main
    menu:
        "You Win!":
            $ fse_result = "win"
            call fse_exid
    return
label you_lose:
    hide screen fse_main
    menu:
        "You Lose!":
            $ fse_result = "lose"
            call fse_exid
    return
label fse_exid:
    hide screen fse_main
    jump expression exid_point
    return
