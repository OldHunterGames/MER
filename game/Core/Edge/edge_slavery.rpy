## Slavery quest

label lbl_edge_slavery:
    menu:
        'Slaver offers you a food and protection if you become a slave. He will take you to the city and sell you on the untrained slaves auction.'
        'Become a slave': 
            call lbl_edge_slave_auction
        'Not today':
            call lbl_edge_outpost(location)

    return

label lbl_edge_slave_auction:
    $ buyer = choice(rawstock_buyers)
    'Unknown [buyer] buys you.'
    jump game_over

    return
