﻿# MER main RenPy script

init -10 python:
    sys.path.append(renpy.loader.transfn("scripts"))
    sys.path.append(renpy.loader.transfn("scripts/person"))
    sys.path.append(renpy.loader.transfn("Core"))
    from mer_core import *
    from mer_utilities import *
    from mer_item import *
    from mer_person import *
    from mer_stock import *
    from mer_metric import *      
    from mer_event import *
    from mer_metaperson import *
    
init python:
    outer_worlds = []
    renpy.block_rollback()
    register_actions()

# The game starts here.
label start:
    python:
        great_houses = [Faction(gen_random_person(), __('Kamira'),'kamira'),
            Faction(gen_random_person(), __('Serpis'), 'serpis'),
            Faction(gen_random_person(), __('Corvus'), 'corvus'),
            Faction(gen_random_person(), __('Taurus'), 'taurus')]
        discovered_worlds = []
        core = MistsOfEternalRome()
        set_event_game_ref(core)
        player = Person('adolescent', 'male', 'human')
        # player = gen_random_person('human')
        core.set_player(player)
        core.protagonist.sparks = 250
        meter = Meter(core.protagonist)
        ap = player.ap
        
        ##TEST CODE##
        player.firstname = 'Охотник'
        player.set_avatar('images/avatar/old_huntsman_ava.jpg')
        player.skill('survival').training = True
        
        light_armor = Armor('light_armor')
        heavy_armor = Armor('heavy_armor')
        knife = Weapon('offhand', 'slashing')
        stiletto = Weapon('offhand', 'piercing')
        mace = Weapon('versatile', 'impact')
        sword = Weapon('versatile', 'slashing')
        halberd = Weapon('twohand', 'slashing')        
        
        player.equip_armor(light_armor, 'overgarments') 
        player.equip_on_slot('belt1', knife)
        player.equip_on_slot('belt2', stiletto)
        player.equip_on_slot('armband', mace)       
        player.equip_on_slot('ankleband', sword) 
        player.equip_on_slot('harness', halberd) 

    
    show expression "interface/bg_base.jpg" as bg
    call evn_init
    call lbl_edge_main
    
    return
    
label choose_action:
    "You have [core.protagonist.sparks] sparks left. You need to pay [core.protagonist.allowance] sparks this decade to a major House. Mood: [player.mood]. Actions left: [ap]"    
    $ loc_to_call = "choose_acton"
    $ world_to_go = None
    menu:
        "Visit discovered world" if discovered_worlds:
            python:
                items = [(i.name, i) for i in discovered_worlds if hasattr(i, 'name')]
                items.append(("Don't go anywhere", "choose_acton"))
                world_to_go = renpy.display_menu(items)
                if isinstance(world_to_go, str):
                    loc_to_call = world_to_go
                else:
                    loc_to_call = world_to_go.point_of_arrival
        "Discover new world" if outer_worlds:
            $ loc_to_call = core.discover_world(outer_worlds)
        "Relax":
            $ loc_to_call = "end_turn"
        "finish":
            jump end_turn
    jump choose_action
   
label end_turn:
    $ core.new_turn()
    call new_turn
    return
    
label new_turn:
    call choose_action
    return
    
label game_over:
    "Game Over!"
    $ renpy.full_restart()

