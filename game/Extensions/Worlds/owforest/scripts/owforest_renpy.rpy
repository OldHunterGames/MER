# RenPy scripts for OW
init 1 python:
    sys.path.append(renpy.loader.transfn("Extensions/Worlds/owforest/scripts"))
    from owforest_main import *

init 10 python:
    outer_worlds.append(OWForest)
    
label owforest_arrive:
    $ ow = OWForest()
    "[ow.description]"
    "Rape the native girl to eavaluate this world for a report."
    $ enemy = Person()        
    $ exid_point = "owforest_exid"
    call fse_start   
    return
    
label owforest_exid:
    "The [ow.name] world is scouted. You can return to Eternal Rome to get a reward."
    
    menu:
        "Go back":
            call get_sparks    
    return
