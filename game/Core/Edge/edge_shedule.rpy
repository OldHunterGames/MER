##############################################################################
# The Edge of Mists schedule
#
# Script for EOM shedule events

label edge_None_template(actor):
    $ d = actor.description()
    '[d] TOASTED!'
    return
 

         
## OVERTIME SLOT
label edge_optional_nap(actor):
    python:
        name = actor.name
        actor.gain_energy()
        # actor.add_buff('rested')
    return      

label edge_optional_whores(actor):
    python:
        name = actor.name
        actor.satisfy_need('eros', 3)
#    "[name]fucks whores."
    return

label edge_optional_booze(actor):
    python:
        name = actor.name
        actor.satisfy_need('wellness', 3)
#    "[name]is drunk. Makes him feel better."
    return

label edge_optional_maid(actor):
    python:
        name = actor.name
        actor.satisfy_need('authority', 2)
        actor.satisfy_need('comfort', 3)
#    "[name]have subservient maid."
    return
    
## FEED SLOT    

label edge_ration_starve(actor):
    python:
        name = actor.name
        ration = actor.food_info()    
    '[name]ration is [ration].'    
    return  

label edge_ration_dry_low(actor):
    python:
        name = actor.name
        actor.eat(1, 0)        
        ration = actor.food_info()  
    'Eating some nutrition bars. [name]ration is [ration].'    
    return  

label edge_ration_dry(actor):
    python:
        name = actor.name
        actor.eat(2, 0)        
        ration = actor.food_info()    
    'Eating nutrition bars. [name]ration is [ration].'    
    return  

label edge_ration_dry_high(actor):
    python:
        name = actor.name
        actor.eat(3, 0)        
        ration = actor.food_info()    
    'Eating nutrition bars greedily. [name]ration is [ration].'    
    return  

label edge_ration_cooked(actor):
    python:
        name = actor.name
        actor.eat(2, 4)        
        ration = actor.food_info()    
    'Eating cooked food in a slums pub. [name]ration is [ration].'    
    return  

label edge_ration_cooked_high(actor):
    python:
        name = actor.name
        actor.eat(3, 4)        
        ration = actor.food_info()  
    'Feasting on a whole grilled girl. [name]ration is [ration].'    
    return  
                    
label edge_ration_canibalism(actor):
    python:
        name = actor.name
        actor.eat(3, player.get_best_corpse().succulence()-1)
        ration = actor.food_info() 
    '[name]is a canibal. [name]ration is [ration]'    
    return  

## ACCOMODATION SLOT    
label edge_accommodation_makeshift(actor):
    python:
        name = actor.name
        actor.tense_need('comfort', 'bad_sleep')
        actor.tense_need('prosperity', 'homeless')
        actor.tense_need('wellness', 'bed_of_rocks')
#    "[name]sleeps on a rocky cold ground. It's painful, uncomfortable and reminds of poverty."
    return

label edge_accommodation_mat(actor):
    python:
        actor.tense_need('comfort', 'bad_sleep')
        actor.tense_need('prosperity', 'poor_accomodation')
        name = actor.name
#    "[name]sleeps on a rugged mat in a common room. It's uncomfortable and reminds of poverty."          
    return 

label edge_accommodation_cot(actor):
    python:
        actor.satisfy_need('comfort', 1)    
        name = actor.name
#    '[name]sleeps on a rough cot under the ruggy blanket. Well, SOME comfort at least...'    
    return 

label edge_accommodation_appartment(actor):
    python:
        actor.satisfy_need('comfort', 3)    
        name = actor.name
#    '[name]sleeps on a real bed in a single apartments. Comfortable and even luxurious by the standards of the border.'    
    return  

## JOB SLOT        
label edge_job_idle(actor):
    python:
        actor.gain_energy()
        #actor.add_buff('rested')

    return
   
label edge_job_beg(actor):
    python:
        actor = actor
        name = actor.name
        actor.moral_action(activity = 'timid') 

        actor.tense_need('wellness', 'unhealthy_job')
        actor.tense_need('prosperity', 'beggar')
        actor.tense_need('authority', 'humiliation')        

        actor.eat(1, -1)
        ration = actor.food_info()    
    '[name]humbly begs for food and gains a few disgustning leftovers. Disgracing, lowly and definetly not healthy experience. [ration]'
    return
    
label edge_job_bukake(actor):
    python:
        name = actor.name
        actor.moral_action(activity = 'good') 
        actor.tense_need('wellness', 'unhealthy_job')
        actor.tense_need('comfort', 'tiresome_job')
        actor.tense_need('authority', 'humiliation')    
        actor.tense_need('eros', 'sexplotation')    
        actor.eat(3, -1)
        ration = actor.food_info()    

    'Cum is your food! Ration: [ration]'
    return
    
label edge_job_hooker(actor):
    python:
        name = actor.name
        actor.tense_need('wellness', 'unhealthy_job')
        actor.tense_need('comfort', 'tiresome_job')
        actor.tense_need('authority', 'humiliation')    
        actor.tense_need('eros', 'sexplotation')    
        partner = gen_simple_person(gender='male')
        partner.set_nickname("the client") 
        player.relations(partner) 
        chance = choice([1,2])

    if chance == 1:
        call edge_jbevent_paysex(actor)
    else:
        call edge_jbevent_assault(actor)

    return

label edge_jbevent_paysex(actor):
    'Working as a hooker [actor.name] meets important client...'
    partner "Let's fuck already!"
    python:
        name = actor.name
        sex = SimpleSex((player, 'controlled'), (partner, 'wishful'))
        result = sex.get_results()
        performance = result[partner]
        
    if result[partner] >= 0:
        $ yeld = yeld_table[performance]
        'You earned [yeld] bars this decade.'
        $ player.add_money(yeld)

    else:
        call edge_jbevent_assault(actor)

    return

label edge_jbevent_assault(actor):
    $ stranger = partner
    $ visavis = stranger
    'One of the clients assaults you'
    stranger "Give me all you got, yoy fucking whore!"
        
    python:     
        options = CardsMaker()
        options.add_entry('errant_engage', edge_errant_options)
        options.add_entry('raider_yeld', edge_raider_options)
        CardMenu(options.run()).show()
    hide card    

    return

label edge_jbevent_yeld(card):
    '[stranger.name] takes your bars and equipement.'
    # stranger "I'll be back for more, you slut!"
    $ player.money = 0
    $ actor.tense_need('prosperity', 'robbery') 
    $ player.transfer_all(stranger)

    return

# label edge_job_manual(actor):
#     python:
#         name = actor.name
#         result = actor.job_productivity()
#         actor.moral_action(orderliness = 'lawful') 
#     if result > 0:
#         "[name]earns: 10 nutrition bars for manual labor. It's a boring job but brings life to order"
#         $ player.add_money(10)
#         $ actor.tense_need('amusement', 'boring_job')    
#     elif result < 0: 
#         $ actor.tense_need('ambition', 'failure_at_work')    

#     return

    
label edge_job_construction(actor):
    python:
        name = actor.name
        yeld = yeld_table[actor.job_productivity()]        
    if yeld > 0:
        "[name]yelds: [yeld] nutrition bars. It's a boring job."
        $ player.add_money(yeld)
        $ actor.tense_need('amusement', 'boring_job')  
    else: 
        '[name] have a failure at work wich is bad for buissiness.'
        $ actor.tense_need('prosperity', 'buissiness_fail') 
        $ actor.tense_need('ambition', 'failure_at_work')            
    return
    
label edge_job_extraction(actor):
    python:
        name = actor.name
        yeld = yeld_table[actor.job_productivity()]        
    if yeld > 0:
        "[name]yelds: [yeld] nutrition bars. It's a unhealthy job."
        $ player.add_money(yeld)
        $ actor.tense_need('wellness', 'unhealthy_job')  
    else: 
        '[name] have a failure at work wich is bad for buissiness.'
        $ actor.tense_need('prosperity', 'buissiness_fail') 
        $ actor.tense_need('ambition', 'failure_at_work')            
    return

    
label edge_job_entertain(actor):
    python:
        name = actor.name
        yeld = yeld_table[actor.job_productivity()]        
    if yeld > 0:
        "[name]yelds: [yeld] nutrition bars. It's a humiliating job."
        $ player.add_money(yeld)
        $ actor.tense_need('authority', 'humiliating_job') 
    else: 
        $ actor.tense_need('prosperity', 'buissiness_fail') 
        $ actor.tense_need('ambition', 'failure_at_work')            
    return
    
label edge_job_houseservice(actor):
    python:
        name = actor.name
        yeld = yeld_table[actor.job_productivity()]        
    if yeld > 0:
        "[name]yelds: [yeld] nutrition bars. It's a boring job."
        $ player.add_money(yeld)
        $ actor.tense_need('amusement', 'boring_job')  
    else: 
        $ actor.tense_need('prosperity', 'buissiness_fail') 
        $ actor.tense_need('ambition', 'failure_at_work')            
    return
    
label edge_job_scavenger(actor):
    python:
        name = actor.name
        yeld = yeld_table[actor.job_productivity()]        
    if yeld > 0:
        "[name]yelds: [yeld] nutrition bars. It's an unpleasant job."
        $ player.add_money(yeld)
        $ actor.tense_need('amusement', 'unpleasant_job')  
    else: 
        $ actor.tense_need('prosperity', 'buissiness_fail') 
        $ actor.tense_need('ambition', 'failure_at_work')            
    return

label edge_job_range(actor):
    python:
        name = actor.name
    '[name]patroling the Edge of Mists.'
    $ roll = choice([1,2])
    if choice == 1:
        call lbl_edge_randenc_bandit
    else:
        call lbl_edge_randenc_errant
    return
          
        
