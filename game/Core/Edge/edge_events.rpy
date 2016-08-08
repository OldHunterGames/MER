##############################################################################
# The Edge of Mists events
#
# Script for EOM main events

 
# !!!!!! REGISTER EACH EVENT HERE !!!!
label init_events:
    $ register_event('evn_edge_mistadvance')
    
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
    
############## NO CHARACTER EVENTS ##################

label evn_edge_mistadvance(event):
    if len(edge.locations) = 0:
        $ event.skipcheck = False 
        
    $ poped = edge.locations.pop()
    'Mists take over [poped] location'
    return
    
    
    