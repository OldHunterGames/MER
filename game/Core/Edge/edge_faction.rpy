##############################################################################
# The Edge of Mists faction
#
# Factions menu

    
label lbl_edge_faction_livein:
    $ resources = encolor_text(show_resource[edge.resources.value], edge.resources.value)
    $ faction = player.factions[0]
    
    menu:        
        "You have [resources] \nLeader's favor: ?"
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
