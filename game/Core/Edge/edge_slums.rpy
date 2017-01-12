##############################################################################
# The Edge of Mists living in slums
#
# Slums menu


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

