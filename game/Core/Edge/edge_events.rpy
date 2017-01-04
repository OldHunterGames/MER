##############################################################################
# The Edge of Mists events
#
# Script for EOM main events

 
# !!!!!! REGISTER EACH EVENT HERE !!!!
label edge_init_events:
    python:
        register_event('evn_edge_uneventful')
        register_event('evn_edge_mistadvance')
        register_event('evn_edge_slaver')
        register_event('evn_edge_recruiter')
        register_event('evn_edge_bukake')
        register_event('evn_edge_echoing_hills')
        register_event('evn_edge_dying_grove')
        register_event('evn_edge_hazy_marshes')        
        register_event('evn_edge_repair_job')    
        register_event('evn_edge_scavenge')    
        register_event('evn_edge_entertain_job')        
        register_event('evn_edge_brewery')    
        register_event('evn_edge_machinery')             
    
    return True
    
#TESTS & TEMPLATES 

label evn_edge_blank:
   $pass   
   return True
  
label evn_edge_template(event):
    
    #Проверка для турн энда
    if not event.skipcheck:
        if True:
            $ event.skipcheck = True
    # Вообще это должно делаться не так, но в сыче пойдет
    if event.target != child:
        $ event.skipcheck = False 
    
    # Отсечка
    if not event.skipcheck:
        return False
       
        
    #тело эвента
    return True

############## HERO EVENTS ##################



############## EXPLORATION ##################
      
label evn_edge_slaver(event):
    
    if not event.skipcheck:
        if 'slaver' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
       
    edge_slaver 'Hey! Now you know me!'
    'You found a slaver, new options in Outpost'
    $ edge.options.append('slaver')
    $ player.relations(edge_slaver)
    $ edge_exploration.remove('slaver')
    return True
      
label evn_edge_recruiter(event):
    
    if not event.skipcheck:
        if 'recruiter' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
       
    edge_recruiter 'Hey! Do you wanna be a Noble House servant?!'
    'You found a recruiter, new options in Outpost'
    $ edge.options.append('recruiter')
    $ player.relations(edge_recruiter)
    $ edge_exploration.remove('recruiter')
    return True
      
label evn_edge_bukake(event):
    
    if not event.skipcheck:
        if 'bukake' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    if 'male' not in core.orientation[player.gender]:
        'Some bukake slut sucks. Work not for you'
    else:
        'You can be a bukake slut now'
        $ edge.options.append('bukake')
    $ edge_exploration.remove('bukake')
    return True
      
label evn_edge_repair_job(event):
    
    if not event.skipcheck:
        if 'repair_job' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    slums_leader 'There are many broken stuff found at the Edge of Mists. It can be repaired for a price - excellent job opportunuty for anyone with a craft skills.'
    $ edge.options.append('repair_job')
    $ edge_exploration.remove('repair_job')
    return True
      
label evn_edge_scavenge(event):
    
    if not event.skipcheck:
        if 'scavenge' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    'Scavenge job opens.'
    $ edge.options.append('scavenge')
    $ edge_exploration.remove('scavenge')
    return True
      
label evn_edge_entertain_job(event):
    
    if not event.skipcheck:
        if 'entertain_job' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    slums_entertainer "I need someone to help me entertain our guests. Can you dance, sing or tall tails mayhaps? Patrons will give you some tips for a good one!"
    $ edge.options.append('entertain_job')
    $ edge_exploration.remove('entertain_job')
    return True
      
label evn_edge_brewery(event):
    
    if not event.skipcheck:
        if 'brewery' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    slums_entertainer "My patrons need booze! If only some alschemist could brew some... Any drug or funny herb goes actualy!"
    $ edge.options.append('brewery')
    $ edge_exploration.remove('brewery')
    return True
      
label evn_edge_machinery(event):
    
    if not event.skipcheck:
        if 'machinery' in edge_exploration:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    slums_leader 'The tide of Mists often brings some ruined factories, spacehulks and steamshipwrecks here to the Edge. Engeneer, hacker or scientist can disassemble some machinery to gain useful resources!'
    $ edge.options.append('machinery')
    $ edge_exploration.remove('machinery')
    return True
                              
label evn_edge_dying_grove(event):
    
    if not event.skipcheck:
        if 'dying_grove' in edge_exploration:
            $ event.skipcheck = True

    if not event.skipcheck:
        return False
        
    "You found a Dying Grove location. Here you can make a hidden stash or look for other's stashes"
    $ edge.explore_stash('dying_grove')
    return True
      
label evn_edge_hazy_marshes(event):
    
    if not event.skipcheck:
        if 'hazy_marshes' in edge_exploration:
            $ event.skipcheck = True
            
    if not event.skipcheck:
        return False
        
    "You found a Hazy Marshes location. Here you can make a hidden stash or look for other's stashes"
    $ edge.explore_stash('hazy_marshes')
    return True
   
      
label evn_edge_echoing_hills(event):
    
    if not event.skipcheck:
        if 'echoing_hills' in edge_exploration:
            $ event.skipcheck = True

    if not event.skipcheck:
        return False
        
    "You found a Echoing Hills location. Here you can make a hidden stash or look for other's stashes"
    $ edge.explore_stash('echoing_hills')
    return True
                
############## NO CHARACTER EVENTS ##################

label evn_edge_uneventful(event):    
    'Unevetful decade...'    
    return True
    
label evn_edge_mistadvance(event):
    if len(edge.locations) == 0:
        $ event.skipcheck = False 
    if not event.skipcheck:
        return False
    python:
        loc_list = [location for location in edge.locations if not location.permanent]
        to_remove = choice(loc_list)
        edge.remove_location(to_remove)
    'Mists take over [to_remove.name] location'
    return True
