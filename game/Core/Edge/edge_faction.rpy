##############################################################################
# The Edge of Mists faction
#
# Factions menu

    
label lbl_edge_faction_livein:
   
    menu:        
        "Banknotes: [core.resources.money] \n
        Favor: ?"
        'Occupation':
            call lbl  
        'Clanmates':
            call lbl
        'Services':
            call lbl
        'Accomodation':
            call lbl            
        'Equipement':
            call lbl   
        'Ration (food & drugs)':
            call lbl
        'Earnings share (money)':
            call lbl
        'Carry on':
            call lbl_edge_turn
    
    jump lbl_edge_faction_livein
    return
