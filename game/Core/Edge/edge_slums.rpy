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
    python: 
        cost_sjunk = 5
        cost_junk = 10
        cost_scook = 10
        cost_ljunk = 20        
        cost_cook = 25
        cost_bbq = 50
                                
    menu:
        'Junkfood lunch ([cost_sjunk] brs/decade)':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 1, 'quality': 0}, spends = cost_sjunk) 
        'Junkfood 3 time meals ([cost_junk] brs/decade)':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 2, 'quality': 0}, spends = cost_junk) 
        'Cooked lunch ([cost_scook] brs/decade)':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 1, 'quality': 2}, spends = cost_scook) 
        'All junkfood you can eat ([cost_ljunk] brs/decade)':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 3, 'quality': 0}, spends = cost_ljunk) 
        'Cooked 3 time meals ([cost_cook] brs/decade)':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 2, 'quality': 2}, spends = cost_cook) 
        'Whole roasted girls ([cost_bbq] brs/decade)':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'amount': 3, 'quality': 3}, spends = cost_bbq) 
        'Forage (free)':
            $ target.schedule.remove_action('feed_catering')
            
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
            $ target.set_job('idle', skill=None, single=False, target=None)
            # $ target.schedule.add_action('job_idle', single=False)  
    return
    
label lbl_edge_slums_services:
    menu:
        'Back':
            call lbl_edge_manage

    return

label lbl_edge_slums_work_food:
    menu:
        'Beg for food (no skill)':
            $ target.set_job('beg', skill=None, single=False, target=None, difficulty=0) 
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
        
        'Manual labor (athletics, +10 brs/decade)':
            $ target.set_job('manual', skill='athletics', single=False, target=None, difficulty=2)
            
        'Household services (housekeeping, +10 brs/decade)':
            $ target.set_job('houseservice', skill='housekeeping', single=False, target=None, difficulty=2)
        
        'Repair stuff (craft)' if 'repair_job' in edge.options:
            $ target.set_job('repair', skill='craft', single=False, target=None, difficulty=3)
        
#        'Scavenger (survival)' if 'scavenge' in edge.options:
#            $ target.set_job('scavenge', skill='survival', single=False, target=None, difficulty=3)
                    
        'Entertainer (expression)' if 'entertain_job' in edge.options:
            $ target.set_job('entertain', skill='expression', single=False, target=None, difficulty=3)
                    
        'Alchemy (science)' if 'brewery' in edge.options:
            $ target.set_job('alchemy', skill='science', single=False, target=None, difficulty=3)
                    
        'Disassembly old machinery (engineering)' if 'machinery' in edge.options:
            $ target.set_job('disassembly', skill='engineering', single=False, target=None, difficulty=3)
                                                                                                                      
        'Newermind':
            call lbl_edge_slums_jobs
            
    jump lbl_edge_manage
    return

label lbl_edge_slums_work_special:
    menu:
        'Range the Edge':
            $ target.set_job('range', skill=None, single=False, target=None, difficulty=0)
            
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

