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
    
label shd_edge_job_scmunition(action):
    python:
        actor = action.actor
        name = actor.name
        moral = None
        result = core.skillcheck(actor, 'survival', difficulty = 1, tense_needs=['amusement', 'comfort'], satisfy_needs=['prosperity'], beneficiar=actor, morality=moral, special_motivators=[])        
        gain = result*result
        core.resources.munition += gain
        actor.skill('survival').get_expirience(result)
    '[name] scavenging munition on the gim battlefield. Yelds [gain] munition.'
    return
    
label shd_edge_job_dbexctraction(action):
    python:
        actor = action.actor
        name = actor.name
        moral = None
        result = core.skillcheck(actor, 'athletics', difficulty = 1, tense_needs=['amusement', 'comfort'], satisfy_needs=['prosperity'], beneficiar=actor, morality=moral, special_motivators=[])        
        gain = result*result
        core.resources.fuel += gain
        actor.skill('athletics').get_expirience(result)
    '[name] extracting demon blood from the crimson pit. Yelds [gain] fuel.'
    return
    
label shd_edge_job_scjunc(action):
    python:
        actor = action.actor
        name = actor.name
        moral = None
        result = core.skillcheck(actor, 'survival', difficulty = 2, tense_needs=['amusement', 'comfort'], satisfy_needs=['prosperity'], beneficiar=actor, morality=moral, special_motivators=[])        
        gain = result*result
        core.resources.hardware += gain
        actor.skill('survival').get_expirience(result)
    '[name] scavenging junk. Yelds [gain] hardware.'
    return
    
label shd_edge_job_disassemble(action):
    python:
        actor = action.actor
        name = actor.name
        moral = None
        result = core.skillcheck(actor, 'mechanics', difficulty = 1, tense_needs=['amusement', 'comfort'], satisfy_needs=['prosperity'], beneficiar=actor, morality=moral, special_motivators=[])        
        gain = result*result
        core.resources.hardware += gain
        actor.skill('mechanics').get_expirience(result)
    '[name] disasembles old machinery on the ruined factory. Yelds [gain] hardware.'
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
    
label shd_edge_overtime_foundcamp(action):
    python:
        edge.locations.remove('outworld ruines')
        edge.locations.append('your base camp')
        camp.found()
    'Encamped in outworld ruines.'
    return       
    
    
    