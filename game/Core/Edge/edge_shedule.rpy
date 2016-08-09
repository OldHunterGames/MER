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
        name = action.actor.name
    return
    
label shd_edge_job_idle(action):
    python:
        pass
    'idling...'
    return
    
label shd_edge_job_explore(action):
    python:
        while len(edge.locations) < edge.loc_max:
            scouted = choice(edge_locations)
            if scouted not in edge.locations:
                edge.locations.append(scouted)
        
    'All nearby locations explored'
    return

label shd_edge_overtime_nap(action):
    python:
        pass
    'resting...'
    return      
    
label shd_edge_overtime_scout(action):
    python:
        if len(edge.locations) < edge.loc_max:
            scouted = choice(edge_locations)
            if scouted in edge.locations:
                renpy.jump('shd_edge_overtime_scout')
            edge.locations.append(scouted)
            message = 'Found %s location.'% scouted
        else:
            message = 'Already exlored'
        
    '[message]'
    return        