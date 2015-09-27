# Core Events for Mists of Eternal Rome
python:
    import sys
    import inspect
    sys.path.append(renpy.loader.transfn("Core"))    
    from core_events import *

label evn_init:
    python:
        # TODO: Тут надо будет сделать так чтобы список возможных эвентов генеировался динамически
        #ev_name_list = [
        #EVUnique(game),
        #EVGeneric(game),        
        #]
        #for obj in ev_name_list:
        #    game.event_list.append(obj)
        ev_name_list = []
        for subclass in Event.__subclasses__():
            game.event_list.append(subclass(game))

    return


label evn_template:
   "Event №"
   python:
       pass
   
   return
    

label evn_blank:
   $pass   
   return

   
label evn_unic:
   "Event Unic"
   python:
       pass
   
   return

   
label evn_1:
   "Event №1"
   python:
       pass
   
   return   

