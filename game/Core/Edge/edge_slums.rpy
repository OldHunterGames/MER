##############################################################################
# The Edge of Mists living in slums
#
# Slums menu

label lbl_edge_squatted_slums(location):
    menu:
        'Only place to live in if you not in a gang.'
        'Find some work in a slums':
            call lbl_edge_slums_work(location)
        'Sign in':
            $ edge.slums_mode = True
            call lbl_edge_slums_livein
        'Get out':
            return         
    
    call lbl_edge_squatted_slums(location)
    return

label lbl_edge_slums_livein:
    $ bill = core.resources.consumption('money')
    
    menu:        
        "Banknotes: [core.resources.money] \n
        Decade bill: [bill]"
        'Accomodation':
            call lbl_edge_slums_accomodation            
        'Ration (food & drugs)':
            call lbl_edge_slums_ration
        'Services':
            call lbl_edge_slums_services
        'Back':
            call lbl_edge_manage
   
    jump lbl_edge_slums_livein
    return
    
label lbl_edge_slums_accomodation:
    
    menu:
        'Tiny mat in common room (10$/turn)':
            $ target.schedule.add_action('living_mat') 
            $ summ = 10
        'Cot & bkanket (50$/turn)':
            $ target.schedule.add_action('living_cot') 
            $ summ = 50
        'Apartments (100$/turn)':
            $ target.schedule.add_action('living_appartment') 
            $ summ = 100            
        'Back':
            call lbl_edge_slums_livein
            
    $ core.resources.add_consumption(target, 'money', summ, time=1, slot='accomodation_fee')
    return

    
label lbl_edge_slums_ration:
    menu:
        'Back':
            call lbl_edge_slums_livein

    return
    
    
label lbl_edge_slums_services:
    menu:
        'Back':
            call lbl_edge_slums_livein

    return
    

label lbl_edge_slums_work(location):
    menu:
        'You can get some selfemployeed work to get some resources with your skill, or miserablly beg for some leftovers. Any way you will get yor payment after a full decade of an adequate work.'
        'Beg for food (no skill)':
            $ target.schedule.add_action('job_beg')  
            jump lbl_edge_manage
            
        'Manual labor (athletics)':
            $ title = __('Some manual labor (athletics).')
            $ skill_id = 'survival'
            $ description = _('doing manual labor at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
            jump lbl_edge_manage
            
        'Household services (housekeeping)':
            $ title = __('Some labor (housekeeping).')
            $ skill_id = 'survival'
            $ description = _('providing household services at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
            jump lbl_edge_manage
                                    
        'Sexual services (sex)':
            $ title = __('Some labor (sex).')
            $ skill_id = 'survival'
            $ description = _('doing sexual services at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
            jump lbl_edge_manage
                                    
        'Newermind':
            $ pass
            
    call lbl_edge_squatted_slums(location)
    return
    