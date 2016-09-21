##############################################################################
# The Edge of Mists living in slums
#
# Slums menu

    
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