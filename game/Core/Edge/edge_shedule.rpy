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
        action.actor.add_buff('rested')
    '[name]resting.'
    return      
   

## ACCOMODATION SLOT    
label edge_accommodation_makeshift(action):
    python:
        name = action.actor.name
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        action.actor.wellness.set_tension()   
        name = action.actor.name
    "[name]sleeps on a rocky cold ground. It's painful, uncomfortable and reminds of poverty."
    return

label edge_accommodation_mat(action):
    python:
        action.actor.comfort.set_tension()
        action.actor.prosperity.set_tension()
        name = action.actor.name
    "[name]sleeps on a rugged mat in a common room. It's uncomfortable and reminds of poverty."          
    return 

label edge_accommodation_cot(action):
    $ action.actor.comfort.satisfaction = 1
    $ name = action.actor.name
    '[name]sleeps on a rough cot under the holy blanket. Well, SOME comfort at least...'    
    return 

label edge_accommodation_appartment(action):
    python:
        action.actor.comfort.satisfaction = 3
        action.actor.prosperity.satisfaction = 1
        name = action.actor.name
    '[name]sleeps on a real bed in a single apartments. Comfortable and even luxurious by the standards of the border.'    
    return  


## FEED SLOT    
label shd_edge_feed_catering(action):
    python:
        name = action.actor.name
        actor.eat(action.special_values['amount'], action.special_values['quality'])
    '[name]eats at the common room.'    
    return  


## JOB SLOT        
label shd_edge_job_idle(action):
    python:
        name = action.actor.name
        action.actor.add_buff('rested')
        txt = encolor_text('some comfort', 2)
    "[name]have no job to do and resting. It's conserves energy and gives [txt]"
    return
   
label shd_edge_job_beg(action):
    python:
        actor = action.actor
        name = actor.name
        actor.moral_action('timid') 

        actor.wellness.set_tension()        
        actor.prosperity.set_tension()        
        actor.authority.set_tension()

        actor.eat(1, -1)
    '[name]humbly begs for food and gains a few disgustning leftovers. Disgracing, lowly and definetly not healthy experience.'
    return
    
label shd_edge_job_bukake(action):
    python:
        actor = action.actor
        name = actor.name
        actor.wellness.set_tension()    
        actor.comfort.set_tension()
        actor.authority.set_tension()        
        actor.eros.set_tension()    
        actor.eat(3, -1)
        text = __('')
    '[name]humbly sucks stangers diks and consume their semen for nutrition. Nutritive but disgusting. This labor is disgracing, uncomfortable and even painful.'
    return
    
label shd_edge_job_manual(action):
    python:
        actor = action.actor
        name = actor.name
        result = actor.job_productivity()
        actor.moral_action('lawful') 
    if result > 0:
        "[name]earns: 10 nutrition bars for manual labor. It's a boring job but brings life to order"
        $ player.add_money(10)
        $ action.actor.amusement.set_tension()
    else: 
        $ action.actor.ambition.set_tension()

    return
    
label shd_edge_job_houseservice(action):
    python:
        actor = action.actor
        name = actor.name
        result = actor.job_productivity()
        actor.moral_action('lawful') 
    if result > 0:
        "[name]earns: 10 nutrition bars for househod services. It's a boring job but brings life to order."
        $ player.add_money(10)
        $ action.actor.amusement.set_tension()
    else: 
        $ action.actor.ambition.set_tension()

    return
    
label shd_edge_job_repair(action):
    python:
        actor = action.actor
        name = actor.name
        yeld = yeld_table[actor.job_productivity()]        
    if yeld > 0:
        "[name]yelds: [yeld] nutrition bars. It's a boring job."
        $ player.add_money(yeld)
        $ action.actor.amusement.set_tension()
    else: 
        $ action.actor.ambition.set_tension()
    return
        
label shd_edge_job_range(action):
    python:
        actor = action.actor
        name = actor.name
    '[name]patroling the Edge of Mists.'
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
       

    
    
