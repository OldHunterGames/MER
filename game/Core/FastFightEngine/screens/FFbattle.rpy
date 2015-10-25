##############################################################################
# FaFiEn Battle Screen
#
# Screen that's used to display battle in FaFiEn mode.

screen ffe_battle():
    frame:
        align (0.01, 0.98)
        xsize 200
        ysize 320
        
        vbox:
            spacing 10
            frame:
                align (0.5, 0.05)
                text fight.actor.name
            imagebutton: # PLAYER AVATAR
                align (0.05, 0.1)
                idle im.Scale(fight.actor.avatar, 200, 200)
                hover im.MatrixColor(im.Scale(fight.actor.avatar, 200, 200), im.matrix.brightness(0.05))
                action Return("show_your_role")
            hbox:
                align (0.5, 0.95)
                text "[fight.actor.hp]"
                bar value fight.actor.hp range fight.actor.max_hp

    fixed:
        ypos 0.50
        xpos 0.2
        xsize 1000
        ysize 320    
        
        hbox:
         spacing 10
         xalign 0.45
         yalign 0.99
         for card in fight.actor.potential:
             frame:
                 xalign 0.5
                 xsize 200
                 ysize 320
                 vbox:
                     xalign 0.5
                     spacing 10
                     textbutton card.name:
                         action Return(["make_action", card])  
                     fixed:
                         text card.show()                   
                     
                         
    frame:
        align (0.98, 0.01)
        xsize 200
        ysize 320
        
        vbox:
            spacing 10
            frame:
                align (0.5, 0.05)
                text fight.target.name
            imagebutton: # ENEMY AVATAR
                align (0.05, 0.1)
                idle im.Scale(fight.target.avatar, 200, 200)
                hover im.MatrixColor(im.Scale(fight.target.avatar, 200, 200), im.matrix.brightness(0.05))
                action Return("show_your_role")
            hbox:
                align (0.5, 0.95)
                text "[fight.target.hp] "
                bar value fight.target.hp range fight.target.max_hp
        
    fixed:
        xalign 0.5
        xsize 1000
        ysize 320    
        
        hbox:
             xalign 0.5
             spacing 10
             frame:
                 xalign 0.5
                 xsize 200
                 ysize 320
                 vbox:
                     xalign 0.5
                     spacing 10
                     frame:
                         align (0.5, 0.05)
                         text fight.target.action.name
                     fixed:
                         align (0.5, 0.05)
                         text fight.target.action.show()
