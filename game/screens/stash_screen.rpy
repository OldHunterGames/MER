
screen sc_manage_stash(stash):
    modal True
    window:
        xfill True
        yfill True
        style 'char_info_window'
        hbox:
            vbox:
                frame:
                    xsize 300
                    ysize 300
                    
                    viewport:
                        scrollbars 'vertical'
                        draggable True
                        mousewheel True
                        xsize 300
                        ysize 300
                        vbox:
                            text 'Player':
                                xalign 0.5
                            for i in player.items:
                                python:
                                    if i.amount > 1:
                                        name = "%s(%s)"%(i.name(), i.amount)
                                    else:
                                        name = i.name()
                                textbutton name:
                                    action Function(player.transfer_item, i, stash)
                frame:
                    vbox:
                        text "Nutrition bars(%s)"%player.money
                        if player.money >= 1:
                            textbutton '1' action Function(player.transfer_money, stash, 1)
                        if player.money >= 10:
                            textbutton '10' action Function(player.transfer_money, stash, 10)
                        if player.money >= 100:
                            textbutton '100' action Function(player.transfer_money, stash, 100)
                        if player.money > 0:
                            textbutton 'all' action Function(player.transfer_money, stash, player.money)

            vbox:
                frame:
                    xsize 300
                    ysize 300
                   
                    viewport:
                        scrollbars 'vertical'
                        draggable True
                        mousewheel True
                        xsize 300
                        ysize 300
                        vbox:
                            text 'Stash':
                                xalign 0.5
                            for i in stash.items:
                                python:
                                    if i.amount > 1:
                                        name = "%s(%s)"%(i.name(), i.amount)
                                    else:
                                        name = i.name()
                                textbutton name:
                                    action Function(stash.transfer_item, i, player)
                frame:
                    vbox:
                        text "Nutrition bars(%s)"%stash.money
                        if stash.money >= 1:
                            textbutton '1' action Function(stash.transfer_money, player, 1)
                        if stash.money >= 10:
                            textbutton '10' action Function(stash.transfer_money, player, 10)
                        if stash.money >= 100:
                            textbutton '100' action Function(stash.transfer_money, player, 100)
                        if stash.money > 0:
                            textbutton 'all' action Function(stash.transfer_money, player, player.money)
    frame:
        ypos 501
        xpos 5
        textbutton 'Leave' action Return()

screen sc_trade(stash):
    modal True
    python:
        multiplier = (float(player.trade_level)-float(stash.trade_level)) / 10
        if multiplier < 0:
            buy_multiplier = 1 + abs(multiplier)
            sell_multiplier = 1 - abs(multiplier)
        else:
            buy_multiplier = 1 - abs(multiplier)
            sell_multiplier = 1 + abs(multiplier)
    window:
        xfill True
        yfill True
        style 'char_info_window'
        hbox:
            vbox:
                frame:
                    xsize 300
                    ysize 300
                    
                    viewport:
                        scrollbars 'vertical'
                        draggable True
                        mousewheel True
                        xsize 300
                        ysize 300
                        vbox:
                            text 'Player':
                                xalign 0.5
                            for i in player.items:
                                python:
                                    if i.amount > 1:
                                        name = "%s(%s)"%(i.name(), i.amount)
                                    else:
                                        name = i.name()
                                if i.amount > 1:
                                    text 'Price for 1: %s'%(int(i.price*sell_multiplier))
                                else:
                                    text 'Price: %s'%(int(i.price*sell_multiplier))
                                textbutton name:
                                    action Function(player.transfer_item, i, stash), Function(player.add_money, int(i.price*sell_multiplier))
                frame:
                    vbox:
                        text "Nutrition bars(%s)"%player.money

            vbox:
                frame:
                    xsize 300
                    ysize 300
                   
                    viewport:
                        scrollbars 'vertical'
                        draggable True
                        mousewheel True
                        xsize 300
                        ysize 300
                        vbox:
                            text 'Trader':
                                xalign 0.5
                            for i in stash.items:
                                python:
                                    if i.amount > 1:
                                        name = "%s(%s)"%(i.name(), i.amount)
                                    else:
                                        name = i.name()
                                if i.amount > 1:
                                    text 'Price for 1: %s'%(int(i.price*buy_multiplier))
                                else:
                                    text 'Price: %s'%(int(i.price*buy_multiplier))
                                textbutton name:
                                    action [Function(stash.transfer_item, i, player), Function(player.remove_money, int(i.price*buy_multiplier)),
                                        SensitiveIf(player.has_money(int(i.price*buy_multiplier)))]
        frame:
            ypos 501
            xpos 5
            textbutton 'Leave' action Return()