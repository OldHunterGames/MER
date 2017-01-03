##############################################################################
# The Edge of Mists living in slums
#
# Slums menu

label lbl_edge_slums_accomodation:

    menu:
        'Tiny mat in common room ([cost_1])':
            $ target.schedule.add_action('accommodation_mat', single=False) 
            $ cost = 1
        'Cot & bkanket ([cost_2])':
            $ target.schedule.add_action('accommodation_cot', single=False) 
            $ cost = 2
        'Apartments ([cost_3])':
            $ target.schedule.add_action('accommodation_appartment', single=False) 
            $ cost = 3            
        'Rough ground, out of the walls ([free])':
            $ target.schedule.add_action('accommodation_makeshift', single=False) 
            $ cost = 0
            
    $ edge.resources.add_consumption(target, 'accomodation fee', cost, 'accomodation', time = None)
    call lbl_edge_manage
    return

    
label lbl_edge_slums_ration:
    menu:
        'Junkfood lunch ([cost_1])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 1, 'quality': 0}) 
            $ cost = 1           
        'Junkfood 3 time meals ([cost_2])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 2, 'quality': 0}) 
            $ cost = 2           
        'Cooked lunch ([cost_2])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 1, 'quality': 2}) 
            $ cost = 2   
        'All junkfood you can eat ([cost_3])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 3, 'quality': 0}) 
            $ cost = 3           
        'Cooked 3 time meals ([cost_3])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 2, 'quality': 2}) 
            $ cost = 3   
        'Whole roasted girl ([cost_4])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 3, 'quality': 3}) 
            $ cost = 4               
        'Eat your own food ([free])':
            $ target.schedule.remove_action('feed_catering')
            $ cost = 0
            
    $ edge.resources.add_consumption(target, 'catering cost',  cost, 'nutrition', time = None)            
    call lbl_edge_manage
    return

label lbl_edge_slums_jobs:
    menu:
        'You can work for food (easy but no gains) or find a way to earn some valueables (hard work). Or maybe you have a special plan? Anyways, more you know about people and places around you, more opportunities you have!'
        'Earn some food':
            call lbl_edge_slums_work_food
        'Gain resources':
            call lbl_edge_slums_work_res
        'Special plan':
            call lbl_edge_slums_work_special   
        'Relax':
            $ target.schedule.add_action('job_idle', single=False)  
    return
    
label lbl_edge_slums_services:
    menu:
        'Back':
            call lbl_edge_manage

    return

label lbl_edge_slums_work_food:
    menu:
        'Beg for food (no skill)':
            $ target.schedule.add_action('job_beg', single=False)  
            jump lbl_edge_manage
                                  
        'Bukake slut' if 'bukake' in edge.options:
            $ target.schedule.add_action('job_bukake', single=False)  
            jump lbl_edge_manage
                                    
        'Newermind':
            $ pass
            
    call lbl_edge_slums_jobs
    return
        

label lbl_edge_slums_work_res:
    menu:
        'Check your skill':
            call lbl_skillcheck(player, 'sex', 1)
            $ resl = skillcheck.result
            'Результат: [resl]'
        
        'Manual labor (athletics)':
            $ title = __('Some manual labor (athletics).')
            $ skill_id = 'athletics'
            $ description = _('doing manual labor at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 1, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', single=False, special_values=special_values)  
            
        'Household services (housekeeping)':
            $ title = __('Some labor (housekeeping).')
            $ skill_id = 'housekeeping'
            $ description = _('providing household services at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 1, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', single=False, special_values=special_values)  
                                    
        'Sexual services (sex)':
            $ title = __('Some labor (sex).')
            $ skill_id = 'sex'
            $ description = _('doing sexual services at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 1, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', single=False, special_values=special_values)  
                                                
        'Newermind':
            call lbl_edge_slums_jobs
            
    jump lbl_edge_manage
    return

label lbl_edge_slums_work_special:
    menu:
        'Trasure hunt in Dying Grove (observation)' if 'treasure_hunt_dying_grove' in edge.options:
            $ description = _('seek treasures in Dying Grove.')
            $ special_values = {'description': description,  'difficulty' : 5 - edge.stash_quality('dying_grove'), 'moral': ['chaotic', 'evil'], 'tense': ['communication', 'comfort', 'altruism'], 'statisfy': ['prosperity', 'activity', 'trill'], 'beneficiar': player,}
            $ target.schedule.add_action('job_treasurehunt', single=True, special_values=special_values)  

        'Trasure hunt in Hazy Marsh (observation)' if 'treasure_hunt_hazy_marsh' in edge.options:
            $ description = _('seek treasures in Echoing Hills.')
            $ special_values = {'description': description,  'difficulty' : 5 - edge.stash_quality('hazy_marsh'), 'moral': ['chaotic', 'evil'], 'tense': ['communication', 'comfort', 'altruism'], 'statisfy': ['prosperity', 'activity', 'trill'], 'beneficiar': player,}
            $ target.schedule.add_action('job_treasurehunt', single=True, special_values=special_values)  

        'Trasure hunt in Echoing Hills (observation)' if 'treasure_hunt_echoing_hills' in edge.options:
            $ description = _('seek treasures in Echoing Hills.')
            $ special_values = {'description': description,  'difficulty' : 5 - edge.stash_quality('echoing_hills'), 'moral': ['chaotic', 'evil'], 'tense': ['communication', 'comfort', 'altruism'], 'statisfy': ['prosperity', 'activity', 'trill'], 'beneficiar': player,}
            $ target.schedule.add_action('job_treasurehunt', single=True, special_values=special_values)  
                                                          
        'Newermind':
            call lbl_edge_slums_jobs
            
    jump lbl_edge_manage
    return    

