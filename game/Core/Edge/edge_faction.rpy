##############################################################################
# The Edge of Mists faction
#
# Factions menu

    
label lbl_edge_faction_livein:
    $ faction = player.factions[0]
    $ master = player.supervisor
    $ favor = encolor_text(show_favor[master.favor], master.favor)
    $ free = encolor_text('free', 5)
    $ f_1 = encolor_resource_text(1)
    $ f_2 = encolor_resource_text(2)
    $ f_3 = encolor_resource_text(3)
    $ f_4 = encolor_resource_text(4)
    $ f_5 = encolor_resource_text(5)    
    $ consumption_level = master.get_favor_consumption()
    $ show_consumption = encolor_text(favor_rate[consumption_level], 5-consumption_level) 
       
    
    menu:        
        "You have [favor] with a faction leader. Your demands are [show_consumption]."
        'Occupation':
            call lbl  
        'Clanmates':
            $ pass
        'Accomodation':
            call lbl_edge_faction_accomodation            
        'Equipement':
           call lbl   
        'Ration (food & drugs)':
            call lbl
        'Services':
            call lbl
        'Earnings share':
            call lbl
        'Carry on':
            call lbl_edge_turn
   
    jump lbl_edge_faction_livein
    return
    
label lbl_edge_faction_accomodation:

    menu:
        'Tiny mat in common room ([free])':
            $ target.schedule.add_action('accommodation_mat', single=False) 
            $ cost = 0
        'Cot & bkanket ([f_1])':
            $ target.schedule.add_action('accommodation_cot', single=False) 
            $ cost = 1
        'Apartments ([f_2])':
            $ target.schedule.add_action('accommodation_appartment', single=False) 
            $ cost = 3            
            
    $  master.add_favor_consumption(target, cost, 'accomodation_favor', time=None, description="")
    # call lbl_edge_faction_livein
    return




