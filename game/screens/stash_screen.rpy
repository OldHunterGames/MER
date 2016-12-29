
screen sc_manage_stash(stash):
    modal True
    window:
        xfill True
        yfill True
        hbox:
            frame:
                xsize 300
                ysize 500
                
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
                xsize 300
                ysize 500
               
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
        ypos 501
        xpos 5
        textbutton 'Leave' action Return()