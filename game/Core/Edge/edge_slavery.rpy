## Slavery quest

label lbl_edge_slavery:
    '[player.name] encounters a slaver at the Outpost.'
    edge_slaver "I'm a respected member of the Slavers Guild here at the Eternal Rome. My task is to acquire unbranded slaves for resale on the slave market inside. I'm interested in buying your captives for nutritional bars. Well, if you're tired of living on the border, I can take you to the market as a slave." 
    call lbl_edge_sell_yourself

    return


label lbl_edge_sell_yourself:
    menu:
        'Slaver offers you a food and protection if you become a slave. He will take you to the city and sell you on the untrained slaves auction.'
        'Become a slave': 
            call lbl_edge_slave_auction(None)
        'Not today':
            pass

    return

label lbl_edge_slave_auction(card):
    $ buyer = choice(rawstock_buyers)
    'Unknown [buyer] buys you.'
    jump game_over

    return
