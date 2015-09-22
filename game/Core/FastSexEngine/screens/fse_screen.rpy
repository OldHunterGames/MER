# Custom screens for MER Fast Sex Engine

##############################################################################
# Main 
#

screen fse_main():    # MAIN SCREEN OF MINI-GAME WITH ALL THE STATICSTICS

    frame: # PLAYER STATBLOCK
        xysize (300, 650) # A size of this frame in pixels.
        align (0.05, 0.2) # Positioning on the screen.
        has vbox spacing 10
        text sex.hero.name 
        
        imagebutton: # PLAYER AVATAR
            align (0.05, 0.03)
            idle im.Scale(sex.hero.avatar, 200, 200)
            hover im.MatrixColor(im.Scale(sex.hero.avatar, 200, 200), im.matrix.brightness(0.05))
            action Return(["show hero"])
        
        text "\n Choose action: \n"
        for act in sex.hero.potential:
            textbutton "[act.name]":
                action Return(["act", act])
        text "\n AR: [sex.hero.arousal]"
                
    vbox:
        xysize (20, 200)
        align (0.24,0.08)
        vbar range sex.hero.arousal_threshold value sex.hero.arousal         

    frame: # AI STATBLOCK
        xysize (300, 650)         
        align (0.95, 0.05)
        has vbox spacing 10
        align (0.96, 0.03)
        text sex.opponent.name 
        
        imagebutton: 
            idle im.Scale(sex.opponent.avatar, 200, 200)
            hover im.MatrixColor(im.Scale(sex.opponent.avatar, 200, 200), im.matrix.brightness(0.05))
            action Return(["show opponent"])
            
        text "\n [sex.opponent.name] action: \n"        
        textbutton "[sex.opponent.action.name]":
            action Return(["show ops action", sex.opponent.action])
        text "\n AR: [sex.opponent.arousal]"
           
    vbox:
        xysize (20, 220)
        align (0.76,0.1)
        vbar range sex.opponent.arousal_threshold value sex.opponent.arousal

    
