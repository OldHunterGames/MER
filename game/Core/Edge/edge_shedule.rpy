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
        action.actor.add_buff('bad_sleep')  
        name = action.actor.name
    'Sleeps on a rocky cold ground.'
    return

label shd_edge_accommodation_mat(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        action.actor.wellness.set_tension()    
        name = action.actor.name
    '[name] sleeps on a tiny mat.'          
    return 

label shd_edge_accommodation_cot(action):
    $ action.actor.comfort.satisfaction = 1
    $ name = action.actor.name
    '[name] sleeps on a rough cot.'    
    return 

label shd_edge_accommodation_appartment(action):
    python:
        action.actor.comfort.satisfaction = 3
        action.actor.add_buff('beauty_sleep')        
        name = action.actor.name
    '[name] sleeps in apartments.'    
    return  

label shd_edge_feed_catering(action):
    python:
        action.actor.comfort.satisfaction = 1
        name = action.actor.name
        actor.eat(action.special_values['amount'], action.special_values['qiality'])
    '[name] eats served food.'    
    return  
    
label shd_edge_job_idle(action):
    python:
        pass
    'idling...'
    return
        
label shd_edge_job_moneywork(action):
    python:
        actor = action.actor
        name = actor.name
        moral = action.special_values['moral']
        skill = action.special_values['skill']
        beneficiar = action.special_values['beneficiar']
        tense = action.special_values['tense']
        statisfy = action.special_values['statisfy'] 
        descr = action.special_values['description'] 
        resname = action.special_values['resource_name'] 
        difficulty = action.special_values['difficulty'] 
        result = core.skillcheck(actor, skill, difficulty = difficulty, tense_needs=tense, satisfy_needs=statisfy, beneficiar=beneficiar, morality=moral, special_motivators=[])        
        edge.resources.income(result)
        yeld = encolor_text(__('resources'), result)
        actor.skill(skill).get_expirience(result)
    '[name] [descr] [yeld].'
    return
    
label shd_edge_job_foodwork(action):
    python:
        actor = action.actor
        name = actor.name
        beneficiar = action.special_values['beneficiar']
        difficulty = action.special_values['difficulty']
        skill = action.special_values['skill']
        mrl = action.special_values['moral']
        moral = target.check_moral(mrl, target = beneficiar)
        result = core.threshold_skillcheck(actor, skill, difficulty = difficulty, tense_needs=['amusement', 'comfort'], satisfy_needs=['prosperity'], beneficiar=actor, morality=moral, success_threshold = 1, special_motivators=[])        

        if result[0]:
            text = action.special_values['succes_text']    
            actor.eat(1, 0)
        else:
            text = action.special_values['fail_text'] 
        
    '[name] [text]'
    return
    
label shd_edge_job_beg(action):
    python:
        actor = action.actor
        name = actor.name
        beneficiar = actor
        actor.moral_action('timid') 
        actor.authority.set_tension()
        actor.wellness.set_tension()        
        actor.comfort.set_tension()
        actor.prosperity.set_tension()        
        actor.ambition.set_tension()        
        actor.independence.set_tension()
        actor.power.set_tension()
        actor.approval.set_tension()
        actor.eat(1, -1)
        text = __('humbly begs for food and gains a few disgustning leftovers.')
    '[name] [text]'
    return
    
label shd_edge_job_bukake(action):
    python:
        actor = action.actor
        name = actor.name
        beneficiar = actor
        actor.wellness.set_tension()        
        actor.comfort.set_tension()
        actor.ambition.set_tension()        
        actor.independence.set_tension()
        actor.eat(3, -1)
        text = __('humbly sucks stangers diks and consume their semen for nutrition.')
    '[name] [text]'
    return
        
label shd_edge_job_servitor(action):
    python:
        actor = action.actor
        name = actor.name
        beneficiar = actor
        actor.moral_action('timid') 
        actor.authority.set_tension()
        actor.comfort.set_tension()
        actor.ambition.set_tension()        
        actor.independence.set_tension()
        text = __(' ministering gang members.')
        target.supervisor.gain_favor(1)
    '[name] [text]'
    return
    
label shd_edge_job_simplework(action):
    python:
        actor = action.actor
        skill = action.special_values['skill']
        difficulty = action.special_values['difficulty'] 

        name = actor.name
        descr = action.special_values['description'] 

        moral = action.special_values['moral']
        moral = actor.check_moral(*moral)
        beneficiar = action.special_values['beneficiar']
        tense = action.special_values['tense']
        statisfy = action.special_values['statisfy'] 
        motivation = action.actor.motivation(skill, tense, statisfy, beneficiar, moral)

    call lbl_skillcheck(actor, skill, motivation, difficulty)

    python:
        result = skillcheck.result
        if result > 0:
            actor.moral_action(moral)
        change_needs(actor, tense, satisfy, result)
        yeld = encolor_text(__('resources'), result)
        edge.resources.income(result)
        actor.skill(skill).get_expirience(result)
    '[name] [descr][yeld].'
    return
    
label shd_edge_job_clanwork(action):
    python:
        actor = action.actor
        name = actor.name
        moral = action.special_values['moral']
        skill = action.special_values['skill']
        beneficiar = action.special_values['beneficiar']
        tense = action.special_values['tense']
        statisfy = action.special_values['statisfy'] 
        descr = action.special_values['description'] 
        difficulty = action.special_values['difficulty'] 
        result = core.skillcheck(actor, skill, difficulty = difficulty, tense_needs=tense, satisfy_needs=statisfy, beneficiar=beneficiar, morality=moral, special_motivators=[])        
        yeld = encolor_text(__('favor'), result)
        target.supervisor.gain_favor(result)
        actor.skill(skill).get_expirience(result)
    '[name] [descr][yeld].'
    return
    
    
label job_treasurehunt(action):
    python:
        actor = action.actor
        skill = 'observation'
        difficulty = action.special_values['difficulty'] 

        name = actor.name
        descr = action.special_values['description'] 

        moral = action.special_values['moral']
        beneficiar = action.special_values['beneficiar']
        tense = action.special_values['tense']
        statisfy = action.special_values['statisfy'] 
        motivation = action.actor.motivation(skill, tense, satisfy, beneficiar, moral)

    call lbl_skillcheck(actor, skill, motivation, difficulty)

    python:
        result = skillcheck.result
        if result > 0:
            trs = edge.gen_treasures
            yeld = __('Found: [trs].')
        else:
            yeld = __('Noting found.')

    '[name] [descr][yeld].'
    return
    
label shd_edge_overtime_nap(action):
    python:
        pass
    'resting...'
    return      
    
label shd_edge_overtime_scout(action):
    python:
        if not edge.maximum_scouted():
            scouted = edge.explore_location()
            message = 'Found %s location.'% scouted.name
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
    
    
    
