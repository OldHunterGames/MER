##############################################################################
# The Edge of Mists schedule
#
# Script for EOM shedule events

label shd_edge_None_template(action):
    $ d = action.actor.description()
    '[d] TOASTED!'
    return
 
 
## OVERTIME SLOT
label shd_edge_overtime_nap(action):
    python:
        name = action.actor.name
    '[name] resting...'
    return      
   

## ACCOMODATION SLOT    
label shd_edge_accommodation_makeshift(action):
    python:
        name = action.actor.name
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        action.actor.wellness.set_tension()   
        name = action.actor.name
    "[name] sleeps on a rocky cold ground. It's painful, uncomfortable and reminds of poverty."
    return

label shd_edge_accommodation_mat(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        name = action.actor.name
    "[name] sleeps on a tiny mat. It's uncomfortable and reminds of poverty."          
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


## FEED SLOT    
label shd_edge_feed_catering(action):
    python:
        action.actor.comfort.satisfaction = 1
        name = action.actor.name
        actor.eat(action.special_values['amount'], action.special_values['quality'])
    '[name] eats served food.'    
    return  


## JOB SLOT        
label shd_edge_job_idle(action):
    python:
        name = action.actor.name
        action.actor.add_buff('rested')
        txt = encolor_text('some comfort', 2)
    "[name] have no job to do and resting. It's conserves energy and gives [txt]"
    return

label shd_edge_job_range(action):
    '[action.actor.name] patroling the Edge of Mists.'
    call lbl_edge_randenc_errant
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
        motivation = action.actor.motivation(skill, statisfy, tense, beneficiar, moral)

    call lbl_skillcheck(actor, skill, motivation, difficulty)

    python:
        result = skillcheck.result
         
        actor.moral_action(moral)
        change_needs(actor, statisfy, tense, result)
    if result > 0:
        $ salary = encolor_text(__('salary'), 2)
        $ edge.resources.income(2)  
        '[name][descr][salary].'
    else:
        $ actor.ambition.set_tension()
        '[name] fails to deliver.'    
   
    return
    
label shd_edge_job_hardwork(action):
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
        change_needs(actor, tense, statisfy, result)
        yeld = encolor_text(__('resources'), result)
        edge.resources.income(result)
        actor.skill(skill).get_expirience(result)
    '[name][descr][yeld].'
    return
     
    
label shd_edge_job_treasurehunt(action):
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
        motivation = action.actor.motivation(skill, tense, statisfy, beneficiar, moral)

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
       

    
    
