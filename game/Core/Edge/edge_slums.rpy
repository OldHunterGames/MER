##############################################################################
# The Edge of Mists living in slums
#
# Slums menu

label lbl_edge_slums_accomodation:
    python:
        cost_mat = 5
        cost_cot = 10
        cost_apps = 25

    menu:
        'Tiny mat in common room ([cost_mat] brs/decade)':
            $ cost = cost_mat
            $ target.schedule.add_action('accommodation_mat', single=False, spends = cost) 
        'Cot & bkanket ([cost_cot] brs/decade)':
            $ cost = cost_cot
            $ target.schedule.add_action('accommodation_cot', single=False, spends = cost) 
        'Apartments ([cost_apps] brs/decade)':
            $ cost = cost_apps        
            $ target.schedule.add_action('accommodation_appartment', single=False, spends = cost) 
 
        'Rough ground, out of the walls (free)':
            $ target.schedule.add_action('accommodation_makeshift', single=False, spends = 0) 
            
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
        'Miserable sunsistence':
            call lbl_edge_slums_work_food
        'Proper work':
            call lbl_edge_slums_work_res
        'Special plan':
            call lbl_edge_slums_work_special   
        'Just relax':
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
        
        'Manual labor (athletics, simple)':
            $ skill_id = 'athletics'
            $ description = _('doing manual labor at the slums and gains fixed ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 1, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['activity'], 'beneficiar': player,}
            # $ target.schedule.add_action('job_simplework', single=False, special_values=special_values)  
            $ player.set_job('manual', skill='athletics', single=False, target=None, difficulty=1)
            
        'Household services (housekeeping, simple)':
            $ skill_id = 'housekeeping'
            $ description = _('providing household services at the slums and gains fixed ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 1, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['order'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', single=False, special_values=special_values)  
        
        'Repair stuff (craft, hard)' if 'repair_job' in edge.options:
            $ skill_id = 'craft'
            $ description = _('repairing various stuff for a price. ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': [], 'tense': ['amusement'], 'statisfy': ['prosperity', 'ambition'], 'beneficiar': player,}
            $ target.schedule.add_action('job_hardwork', single=False, special_values=special_values)  
        
        'Scavenger (survival, hard)' if 'scavenge' in edge.options:
            $ skill_id = 'survival'
            $ description = _('repairing various stuff for a price. ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': [], 'tense': ['amusement'], 'statisfy': ['prosperity', 'ambition'], 'beneficiar': player,}
            $ target.schedule.add_action('job_hardwork', single=False, special_values=special_values)  
        
        'Entertainer (expression, hard)' if 'entertain_job' in edge.options:
            $ skill_id = 'expression'
            $ description = _('repairing various stuff for a price. ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': [], 'tense': ['amusement'], 'statisfy': ['prosperity', 'ambition'], 'beneficiar': player,}
            $ target.schedule.add_action('job_hardwork', single=False, special_values=special_values)  
        
        'Brew alchohol (alchemy, hard)' if 'brewery' in edge.options:
            $ skill_id = 'alchemy'
            $ description = _('repairing various stuff for a price. ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': [], 'tense': ['amusement'], 'statisfy': ['prosperity', 'ambition'], 'beneficiar': player,}
            $ target.schedule.add_action('job_hardwork', single=False, special_values=special_values)  
        
        'Disassembly old machinery (any tech skill, hard)' if 'machinery' in edge.options:
            python:
                skills = {'mechanics': target.skill('mechanics').level, 'electronics': target.skill('electronics').level, 'scholarship': target.skill('scholarship').level}
                skill = 'mechanics'
                level = skills['mechanics']
                for key, value in skills.items():
                    if value > level:
                        skill = key
                        level = value
                skill_id = skill
                description = _('repairing various stuff for a price. ')
                special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': [], 'tense': ['amusement'], 'statisfy': ['prosperity', 'ambition'], 'beneficiar': player,}
                target.schedule.add_action('job_hardwork', single=False, special_values=special_values)  
                                                                                                          
        'Newermind':
            call lbl_edge_slums_jobs
            
    jump lbl_edge_manage
    return

label lbl_edge_slums_work_special:
    menu:
        'Range the Edge':
            $ target.schedule.add_action('job_range', single = False, )
            
        'Trasure hunt in Dying Grove (observation)' if 'treasure_hunt_dying_grove' in edge.options:
            $ description = _('seek treasures in Dying Grove.')
            $ dif = 5 - edge.stash_quality('dying_grove')
            $ special_values = {'description': description,  'difficulty' : dif, 'moral': ['chaotic', 'evil'], 'tense': ['communication', 'comfort', 'altruism'], 'statisfy': ['prosperity', 'activity', 'trill'], 'beneficiar': player,}
            $ target.schedule.add_action('job_treasurehunt', single=True, special_values=special_values)  

        'Trasure hunt in Hazy Marsh (observation)' if 'treasure_hunt_hazy_marshes' in edge.options:
            $ description = _('seek treasures in Hazy Marshes.')
            $ dif = 5 - edge.stash_quality('hazy_marshes')
            $ special_values = {'description': description,  'difficulty' : dif, 'moral': ['chaotic', 'evil'], 'tense': ['communication', 'comfort', 'altruism'], 'statisfy': ['prosperity', 'activity', 'trill'], 'beneficiar': player,}
            $ target.schedule.add_action('job_treasurehunt', single=True, special_values=special_values)  

        'Trasure hunt in Echoing Hills (observation)' if 'treasure_hunt_echoing_hills' in edge.options:
            $ description = _('seek treasures in Echoing Hills.')
            $ dif = 5 - edge.stash_quality('echoing_hills')            
            $ special_values = {'description': description,  'difficulty' : dif, 'moral': ['chaotic', 'evil'], 'tense': ['communication', 'comfort', 'altruism'], 'statisfy': ['prosperity', 'activity', 'trill'], 'beneficiar': player,}
            $ target.schedule.add_action('job_treasurehunt', single=True, special_values=special_values)  
                                                          
        'Newermind':
            call lbl_edge_slums_jobs
            
    jump lbl_edge_manage
    return    

