﻿# MER main RenPy script

init -10 python:
    sys.path.append(renpy.loader.transfn("scripts"))
    sys.path.append(renpy.loader.transfn("scripts/person"))
    sys.path.append(renpy.loader.transfn("Core"))
    sys.path.append(renpy.loader.transfn("Core/DuelEngine/scripts"))
    sys.path.append(renpy.loader.transfn("Core/SimpleFightEngine"))
    from simplefight import SimpleFight
    from mer_core import *
    from mer_utilities import *
    from mer_item import *
    from mer_person import *
    from mer_stock import *
    from mer_metric import *      
    from mer_event import *
    from mer_metaperson import *
    from anatomy import BodyPart
    from schedule import ScheduleObject, ScheduleJob
    from duel_engine import *
    from mer_command import *
    from mer_quest import *
    
init python:
    renpy.block_rollback()
    

# The game starts here.
label start:
    python:
        core = MistsOfEternalRome()
        outer_worlds = []
        p = gen_random_person('human', gender='female')
        g = gen_random_person('human')
        z = gen_random_person('human')

        great_houses = [core.add_faction(gen_random_person(), __('Kamira'), 'major_house', 'kamira'),
            core.add_faction(gen_random_person(), __('Serpis'), 'major_house', 'serpis'),
            core.add_faction(gen_random_person(), __('Corvus'), 'major_house', 'corvus'),
            core.add_faction(gen_random_person(), __('Taurus'), 'major_house', 'taurus')]
        guilds = [core.add_faction(gen_random_person(), __('Slavers guild'), 'guild', 'slavers_guild'),
            core.add_faction(gen_random_person(), __('Merchant guild'), 'guild', 'merchant_guild'),
            core.add_faction(gen_random_person(), __('Entertainment guild'), 'guild', 'entertanment_guild'),
            core.add_faction(gen_random_person(), __('Lanisters guild'), 'guild', 'lanisters_guild'),
            core.add_faction(gen_random_person(), __('Ascencors guild'), 'guild', 'ascencors_guild')]
        minor_houses = []
        discovered_worlds = []
        set_event_game_ref(core)
        Person.game_ref = core
        player = gen_random_person(age='adolescent', gender='male', genus='human')
        core.set_player(player)
        core.protagonist.sparks = 250
        meter = Meter(core.protagonist)
        ap = player.ap
        
        ##SEX_OPTIONS
        
        ##TEST CODE##
        # player.firstname = 'Охотник'
        # player.set_avatar('images/avatar/old_huntsman_ava.jpg')
        # player.skill('survival').training = True
        player.add_feature('penis')
    show expression "interface/bg_base.jpg" as bg
    $ core.set_player(PersonCreator().start().make())
    $ player = core.player
    # call screen sc_faction_info(great_houses[0])
    $ init_taro(core.player)
    # $ fight = SimpleFight([player, g], [p, z])
    # $ SimpleSex((player, 'controlled'), (p, 'wishful')) # sex call example
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
        "Finish":
            jump end_turn
    jump choose_action
   
label end_turn:
    $ core.new_turn()
    call new_turn
    return
    
label new_turn:
    call choose_action
    return

label lbl_edge_fate:
    $ txt = fates_list[fate]
    '[txt]'    
    jump game_over
    return
    
label game_over:
    "Game Over!..."
    "To be continued in next build. Please support us."
    $ renpy.full_restart()

    return

screen sc_token_image(person):
    image im.Scale(person.get_token_image(), 300, 450):
        xalign 0.5
        yalign 0.4

label lbl_notify(person, token):
    show screen sc_token_image(person)
    '[person.name] get token [token]'
    return

label lbl_tests:
    menu:
        'anatomy':
            call screen sc_anatomy_builder
    return