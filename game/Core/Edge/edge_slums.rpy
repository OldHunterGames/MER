##############################################################################
# The Edge of Mists living in slums
#
# Slums menu

    
label lbl_edge_slums_livein:
    $ bill = core.resources.consumption('money')
    
    menu:        
        "Banknotes: [core.resources.money] \n
        Decade bill: ?"
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
            $ target.accommodation = "mat"
            $ target.schedule.add_action('living_mat') 
            $ summ = 10
        'Back':
            call lbl_edge_slums_livein
            
    $ game.res_add_consumption(target, 'accomodation_fee', summ, time=None)        
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