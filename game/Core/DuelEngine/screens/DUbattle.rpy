##############################################################################
# Duel Battle Screen
#
# Screen that's used to display battle in duel mode.
label duel_battle_init(fight):
    call screen duel_battle(fight)
    return 

screen duel_battle(fight):
    hbox:
        if not fight.passed:
            textbutton 'Pass':
                align(0.5, 0.08)
                action [Function(fight.make_pass), Function(fight.enemy_run)]
        if not fight.ended:
            textbutton 'Star next round':
                action Function(fight.round_end)
        else:
            textbutton 'Leave' action Return()
    hbox:
        align(0.5, 0.0)
        text 'player: [fight.enemies_loose_points] - enemies: [fight.allies_loose_points]'
    frame:
        align (0.01, 0.98)
        xsize 200
        ysize 320

        vbox:
            spacing 10
            frame:
                hbox:
                    align(0.5, 0.07)
                    text str("{color=#ff0000}%s{/color}"%fight.points['allies']['onslaught'].value)
                    text str("{color=#64f742}%s{/color}"%fight.points['allies']['maneuver'].value)
                    text str("{color=#00007f}%s{/color}"%fight.points['allies']['fortitude'].value)
                    text str("{color=#000000}%s{/color}"%fight.points['allies']['excellence'].value)
                    text str(fight.summary('allies'))
            frame:
                align (0.5, 0.05)
                text fight.current_ally.name
            imagebutton: # PLAYER AVATAR
                align (0.05, 0.1)
                idle im.Scale(fight.current_ally.avatar, 200, 200)
                hover im.MatrixColor(im.Scale(fight.current_ally.avatar, 200, 200), im.matrix.brightness(0.05))
                action Return("show_your_role")

    fixed:
        ypos 0.50
        xpos 0.2
        xsize 1000
        ysize 320    
        
        hbox:
            spacing 10
            xalign 0.45
            yalign 0.99
            if not fight.passed:
                for card in fight.current_ally.hand:
                    frame:
                        xalign 0.5
                        xsize 200
                        ysize 320
                        vbox:
                            xalign 0.5
                            spacing 10
                            textbutton card.name:
                                action [Function(fight.current_ally.use_action, card), Function(fight.enemy_run)]
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
                text fight.current_enemy.name
            imagebutton: # ENEMY AVATAR
                align (0.05, 0.1)
                idle im.Scale(fight.current_enemy.avatar, 200, 200)
                hover im.MatrixColor(im.Scale(fight.current_enemy.avatar, 200, 200), im.matrix.brightness(0.05))
                action Return("show_your_role")
            frame:
                hbox:
                    align(0.5, 0.07)
                    text str("{color=#ff0000}%s{/color}"%fight.points['enemies']['onslaught'].value)
                    text str("{color=#64f742}%s{/color}"%fight.points['enemies']['maneuver'].value)
                    text str("{color=#00007f}%s{/color}"%fight.points['enemies']['fortitude'].value)
                    text str("{color=#000000}%s{/color}"%fight.points['enemies']['excellence'].value)
                    text str(fight.summary('enemies'))


label lbl_duel_battle_end(fight):
    "loosed side is [fight.loser]"
    return 