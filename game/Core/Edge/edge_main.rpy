##############################################################################
# The Edge of Mists main
#
# Main script for EOM core module


label lbl_edge_main:
    'The Mist gives you a way...'    
    call lbl_edge_manage
    return
    
label lbl_edge_manage:
    
    menu:        
        'Carry on':
            call lbl_edge_turn
    
    return
    
label lbl_edge_turn:
    'New turn'
    call lbl_edge_manage
    return
    