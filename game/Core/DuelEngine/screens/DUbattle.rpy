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
        if not fight.ended and fight.passed:
            textbutton 'Star next round':
                action Function(fight.round_end)
        elif fight.ended:
            textbutton 'Leave' action Return()
    vbox:
        align(0.5, 0.0)
        text 'player: [fight.enemies_loose_points] - enemies: [fight.allies_loose_points]'
        text 'currently [fight.current_loser] are loosig'
    frame:
        align (0.01, 0.98)
        xsize 200
        ysize 320

        vbox:
            spacing 10
            frame:
                vbox:
                    align(0.5, 0.07)
                    text str("{color=#ff0000}onslaught: %s{/color}"%fight.points['allies']['onslaught'].value)
                    text str("{color=#64f742}maneuver: %s{/color}"%fight.points['allies']['maneuver'].value)
                    text str("{color=#00007f}fortitude: %s{/color}"%fight.points['allies']['fortitude'].value)
                    text str("{color=#000000}excellence: %s{/color}"%fight.points['allies']['excellence'].value)
                    text str("summary: %s"%(fight.summary('allies')))
            frame:
                align (0.5, 0.05)
                text fight.current_ally.name
            imagebutton: # PLAYER AVATAR
                align (0.05, 0.1)
                idle im.Scale(fight.current_ally.avatar, 200, 200)
                hover im.MatrixColor(im.Scale(fight.current_ally.avatar, 200, 200), im.matrix.brightness(0.05))
                hovered Show('sc_fighter_stats', fight=fight)
                unhovered Hide('sc_fighter_stats')
                action Return("show_your_role")
    vbox:
        xalign 0.3
        yalign 0.1
        for card in fight.current_ally.hand:
            textbutton card.name:
                hovered Show('sc_card_info', card=card)
                unhovered Hide('sc_card_info')
                action [Function(fight.current_ally.use_action, card), Function(fight.enemy_run)]                  
                     
                         
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
                vbox:
                    align(0.5, 0.07)
                    text str("{color=#ff0000}onslaught: %s{/color}"%fight.points['enemies']['onslaught'].value)
                    text str("{color=#64f742}maneuver: %s{/color}"%fight.points['enemies']['maneuver'].value)
                    text str("{color=#00007f}fortitude: %s{/color}"%fight.points['enemies']['fortitude'].value)
                    text str("{color=#000000}excellence: %s{/color}"%fight.points['enemies']['excellence'].value)
                    text str("summary: %s"%(fight.summary('enemies')))


label lbl_duel_battle_end(fight):
    "loosed side is [fight.loser]"
    return 


screen sc_fighter_stats(fight):
    python:
        txt = ''
        weapons = fight.current_ally.get_weapons()
        for i in range(len(weapons)):
            txt += encolor_text(weapons[i].name, weapons[i].quality)
            if i != len(weapons)-1:
                txt += ', '
    frame:
        align (0.01, 0.98)
        xsize 200
        ysize 320
        text '[txt]'


screen sc_card_info(card):
    vbox:
        xalign 0.5
        yalign 0.5
        text card.show()