##############################################################################
# The Edge of Mists events
#
# Script for EOM main events

 
# !!!!!! REGISTER EACH EVENT HERE !!!!
label edge_init_events:
    python:
        register_event('evn_edge_uneventful')
        register_event('evn_edge_outpost')
        register_event('evn_edge_recruiter')
        register_event('evn_edge_slaver')
        register_event('evn_edge_junker')        
        register_event('evn_edge_bukake')
#        register_event('evn_edge_echoing_hills')
#        register_event('evn_edge_dying_grove')
#        register_event('evn_edge_hazy_marshes')        
       
    
    return True
    
#TESTS & TEMPLATES 

label evn_edge_blank:
   $pass   
   return True


############## AQUITANCE EVENTS ##################

label evn_edge_slaver(event):
    
    if not event.skipcheck:
        if 'slaver' not in edge.options:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False

    python:
        edge.options.append('slaver')
        player.relations(edge_slaver)
        core.quest_tracker.add_quest(Quest(**quests_data['edge_slave_quest'])) 

    call lbl_communicate(edge_slaver)
    call lbl_edge_slavery
    return True
      
label evn_edge_recruiter(event):
    
    if not event.skipcheck:
        if 'recruiter' not in edge.options:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
       
    edge_recruiter 'Hey! Do you wanna be a Noble House servant?!'
    python: 
        edge.options.append('recruiter')
        player.relations(edge_recruiter)
        core.quest_tracker.add_quest(Quest(**quests_data['edge_bond_quest']))
        fate = None

    call lbl_communicate(edge_recruiter)    
    call lbl_edge_hiring
    return True

label evn_edge_outpost(event):
    
    if not event.skipcheck:
        if 'guard' not in edge.options:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False

    edge_guard "Stop right there, criminal scum!"
    edge_guard "State your buissines."
    $ player.relations(edge_guard)
    call lbl_communicate(edge_guard)    
    $ edge.options.append('guard')

    python:  
        options = CardsMaker()
        if 'recruiter' not in edge.options:
            options.add_entry('opp_find_recruiter', edge_option_cards)                        
        if 'slaver' not in edge.options:
            options.add_entry('opp_find_slaver', edge_option_cards)
        if 'junker' not in edge.options:
            options.add_entry('opp_find_junker', edge_option_cards)                 
        options.add_entry('nevermind', edge_option_cards)  
        CardMenu(options.run()).show()                
    hide card    

    'Now you know the guard and can go to the outpost.'

    return True

label evn_edge_junker(event):
    
    if not event.skipcheck:
        if 'junker' not in edge.options:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False

    $ edge.options.append('junker')
    $ player.relations(edge_junker)
    edge_junker "Hey, you! I'll give you some food for your stuff from Outworlds! Interested?"
    call lbl_communicate(edge_junker)  
    call lbl_edge_spc_sellall(None)
    'Now you know the junker who will buy all outworld stuff.'

    return True

############## HERO EVENTS ##################



############## EXPLORATION ##################
      
      
label evn_edge_bukake(event):
    
    if not event.skipcheck:
        if 'bukake' not in edge.options:
            $ event.skipcheck = True
    if not event.skipcheck:
        return False
    
    'Some bukake slut sucks.'
    $ obj = ScheduleJob('bukake', edge_jobs_data)
    $ img = obj.image()
    show expression img at truecenter

    if 'male' in core.orientation[player.gender]:
        'You can be a bukake slut now'
        $ player.schedule.unlock('job', ScheduleJob('bukake', edge_jobs_data))

    if player.has_body_part('penis'):
        'You can use bukake-sluts now'
        $ player.schedule.unlock('optional', ScheduleObject('bukake', edge_services_data))

    $ edge.options.append('bukake')
    return True
                              
                
############## NO CHARACTER EVENTS ##################

label evn_edge_uneventful(event):    
    'Unevetful decade...'    
    return True




# label evn_edge_dying_grove(event):
    
#     if not event.skipcheck:
#         if 'dying_grove' not in edge.options:
#             $ event.skipcheck = True

#     if not event.skipcheck:
#         return False
        
#     "You found a Dying Grove location. Here you can make a hidden stash or look for other's stashes"
#     $ edge.explore_stash('dying_grove')
#     return True
      
# label evn_edge_hazy_marshes(event):
    
#     if not event.skipcheck:
#         if 'hazy_marshes' not in edge.options:
#             $ event.skipcheck = True
            
#     if not event.skipcheck:
#         return False
        
#     "You found a Hazy Marshes location. Here you can make a hidden stash or look for other's stashes"
#     $ edge.explore_stash('hazy_marshes')
#     return True
   
      
# label evn_edge_echoing_hills(event):
    
#     if not event.skipcheck:
#         if 'echoing_hills' not in edge.options:
#             $ event.skipcheck = True

#     if not event.skipcheck:
#         return False
        
#     "You found a Echoing Hills location. Here you can make a hidden stash or look for other's stashes"
#     $ edge.explore_stash('echoing_hills')
#     return True