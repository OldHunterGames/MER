
screen sc_manage_stash(stash):
    modal True
    window:
        xfill True
        yfill True
        hbox:
            vbox:
                frame:
                    xsize 300
                    ysize 300
                    
                    viewport:
                        scrollbars 'vertical'
                        draggable True
                        mousewheel True
                        
                        vbox:
                            text 'Player':
                                xalign 0.5
                            for i in player.items:
                                textbutton i.name:
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
                        
                        vbox:
                            text 'Stash':
                                xalign 0.5
                            for i in stash.items:
                                textbutton i.name:
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