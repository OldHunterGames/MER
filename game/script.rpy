# MER main RenPy script

init -10 python:
    sys.path.append(renpy.loader.transfn("scripts"))
    from mer_core import *
    from mer_faction import *
    from mer_item import *
    from mer_person import *
    from mer_stock import *
    
init python:
    outer_worlds = []
    renpy.block_rollback()

# The game starts here.
label start:
    $ game = MistsOfEternalRome(Person())
    $ game.protagonist.sparks = 25
    show expression "interface/bg_base.jpg" as bg
    call new_turn
    return
    
label new_turn:
    "You have [game.protagonist.sparks] sparks left. You need to pay [game.protagonist.lifestyle] sparks this decade to a major House."    
    
    menu:
        "Discover new world" if outer_worlds:
            $ loc_to_call = game.discover_world(outer_worlds)
        "Relax":
            $ loc_to_call = game.end_turn()    
            
    call expression loc_to_call       
    
    return

label get_sparks:
    $ game.protagonist.sparks += 15
    "You get 15 sparks for your discovery."
    call new_turn
    return
    
label game_over:
    "GAME OVER"
    return
