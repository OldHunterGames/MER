##############################################################################
# The Edge of Mists schedule
#
# Script for EOM shedule events

label shd_edge_None_template(action):
    $ d = action.actor.description()
    '[d] TOASTED!'
    return
    
label shd_edge_accommodation_makeshift(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        action.actor.wellness.set_tension()   
        action.actor.add_buff('bad_sleep', {'vitality': -1}, 1)  
        name = action.actor.name()
    return
    