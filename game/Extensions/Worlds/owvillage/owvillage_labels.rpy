init 1 python:
    sys.path.append(renpy.loader.transfn("Extensions/Worlds/owvillage/scripts"))
    from owvillage_main import *
init 10 python:
    outer_worlds.append(OWVillage)


label owvillage_gates():
    $ current_world = OWVillage() if not world_to_go else world_to_go
    if current_world.visited:
        current_world.steward.name "Wellcome back"
    else:
        $ current_world.visited = True
        $ current_world.steward = GenPersonByGender("male")
        $ current_world.steward.name = "Steward"
        current_world.steward.name "Wellcome to our village, stranger"
        $ discovered_worlds.append(current_world)
        $ outer_worlds.remove(OWVillage)
    call village_main
    return
label village_main:
    while True:
        menu:
            "Visit Tavern":
                pass
            "Rape villager":
                call villager_rape
            
            "Back to mists":
                call choose_acton
    return
label villager_rape:
    $ enemy = GenPersonByGender("female")
    $ exid_point = "get_sparks_for_rape"
    call fse_start
    return


label get_sparks_for_rape:
    python:
        sparks = choice(xrange(20))
        if fse_result == 'win':
            game.protagonist.sparks += sparks
            text = "You get %s sparks"%(sparks)
        elif fse_result == 'lose':
            game.protagonist.sparks -= sparks
            text = "You lost %s sparks"%(sparks)
    "[text]"
    
    return