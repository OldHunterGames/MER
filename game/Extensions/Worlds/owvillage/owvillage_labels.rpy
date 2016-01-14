init 1 python:
    sys.path.append(renpy.loader.transfn("Extensions/Worlds/owvillage/scripts"))
    from owvillage_main import *
init 10 python:
    outer_worlds.append(OWVillage)


label owvillage_gates:
    $ current_world = OWVillage() if not world_to_go else world_to_go
    if current_world.visited:
        current_world.steward.name "Wellcome back"
    else:
        $ current_world.visited = True
        $ current_world.steward = GenPersonByGender("male")
        $ current_world.steward.firstname = "Steward"
        current_world.steward.name "Wellcome to our village, stranger"
        $ discovered_worlds.append(current_world)
        $ outer_worlds.remove(OWVillage)
    call owvillage_main
    return
label owvillage_main:
    while True:
        menu:
            "Visit Tavern":
                python:
                    for i in game.event_list:
                        if isinstance(i, OWVillageTavernEvent):
                            owvillage_event = i
                if owvillage_event.seen < 1:
                    $ owvillage_event.decision = None
                    $ owvillage_startevent = owvillage_event.trigger()
                    call expression owvillage_startevent
                else:
                    "You've spend some time at tavern"

            "Rape villager":
                call owvillage_villager_rape

            "Start fight":
                $ ffe_enemy = GenPerson()
                call ffe_start
            
            "Back to mists":
                call choose_acton
    return
label owvillage_villager_rape:
    $ enemy = GenPersonByGender("female")
    $ exid_point = "owvillage_get_sparks_for_rape"
    call fse_start
    return


label owvillage_get_sparks_for_rape:
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
label owvillage_event:
    if owvillage_event.seen > 0 and owvillage_event.decision:
        $ owvillage_event.unique = True
        "A smuggler you met at world, which you have visited some time ago, brought you the promised item"
        menu:
            "Pay smuggler" if game.protagonist.sparks >= 250:
                $ game.protagonist.sparks -= 250
                "You paid smuggler and you both went in different directions fast"
            "Refuse to pay":
                "Smuggler hits you and run away"
    else:
        "While drinking, you noticed suspicious man in opposite side of tavern"
        "After some time he sat in front of you and started to talk"
        $ owvillage_smuggler = GenPersonByGender('male')
        $ owvillage_smuggler.firstname = "Smuggler"
        owvillage_smuggler.name "I see you are not local here. You got here from Eternal Rome just like me"
        owvillage_smuggler.name "I have one thing in another world, which you may be instereted in"
        owvillage_smuggler.name "I'll bring it to you if you can pay me, let's say, 250 sparks"
        menu:
            "Tell him you are interrested":
                $ owvillage_event.decision = True
                $ owvillage_event.natures.append('turn_end')
                owvillage_smuggler.name "Let's deal than! I'll visit you at Rome when i'm ready, don't forget to prepare my sparks"
            "Say no to smuggler":
                $ owvillage_event.decision = False
                owvillage_smuggler.name "Ok, I thougth you are a man I can deal with..."
    return
