## Slavery quest

label lbl_edge_slavery:
    # $ slaver = gen_random_person(genus='human', occupation='pimp', gender='male')
    # show expression "images/bg/outpost.jpg" as bg 
    # slaver 'EEeeee bleat!'
        
    menu:
        'Slaver offers you a food and protection if you become a slave. He will take you to the city and sell you on the untrained slaves auction.'
        'Become a slave': 
            call lbl_edge_slave_auction
        'Not today':
            pass

    return

label lbl_edge_slave_auction:
    $ buyer = choice(rawstock_buyers)
    'Unknown [buyer] buys you.'
    jump game_over

    return
