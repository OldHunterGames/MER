##############################################################################
# Duel Battle Screen
#
# Screen that's used to display battle in duel mode.
style hoverable_text_text:
    take text
    hover_color '#000'
style hoverable_text:
    take hyperlink_text

label duel_battle_init(fight):
    call screen duel_battle(fight)
    return 

screen duel_battle(fight):
    hbox:
        if not fight.passed:
            textbutton 'Pass':
                align(0.5, 0.08)
                action [Function(fight.make_pass), Function(fight.enemy_run), SensitiveIf(fight.player_turn)]
        if not fight.ended and fight.passed:
            textbutton 'Star next round':
                action Function(fight.round_end), SensitiveIf(fight.player_turn)
        elif fight.ended:
            textbutton 'Leave' action Return()
        textbutton 'show fight summary':
            action Function(fight.set_show_summary, True)
    if fight.show_summary:
        vbox:
            align(0.7, 0.5)
            hbox:
                vbox:
                    $ stack = fight.use_stack['allies']
                    text 'allies'
                    for i in range(len(stack)):
                        $ card = stack[i]
                        $ number = i+1
                        text '[number]: [card.name]'
                vbox:
                    text ' '
                vbox:
                    $ stack = fight.use_stack['enemies']
                    text 'enemies'
                    for i in range(len(stack)):
                        $ card = stack[i]
                        $ number = i+1
                        text '[number]: [card.name]'
            textbutton 'Hide':
                xalign 0.5
                action Function(fight.set_show_summary, False)
    vbox:
        align(0.5, 0.0)
        text 'player: [fight.enemies_loose_points] - enemies: [fight.allies_loose_points]'
        text 'currently [fight.current_loser] are loosig'
        if fight.enemy_passed:
            text 'enemy passed'
    frame:
        align (0.01, 0.98)
        xsize 200
        ysize 320

        vbox:
            spacing 10
            frame:
                vbox:
                    align(0.5, 0.07)
                    text str("escalation: %s"%fight.current_ally.escalation)
                    text str(fight.points['allies']['onslaught'].description)
                    text str(fight.points['allies']['maneuver'].description)
                    text str(fight.points['allies']['fortitude'].description)
                    text str(fight.points['allies']['excellence'].description)
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
    if not fight.ended:
        vbox:
            xalign 0.3
            yalign 0.1
            for card in fight.current_ally.hand:
                textbutton card.name:
                    hovered Show('sc_card_info', card=card)
                    unhovered Hide('sc_card_info')
                    action [Function(fight.current_ally.use_action, card), Hide('sc_card_info'),
                            SensitiveIf(fight.player_turn)] 
        frame:
            yalign 0.9
            xalign 0.25
            xsize 200
            ysize 300
            vbox:
                text 'persistent_effects:'
                for action in fight.persistent_actions:
                    text action.name                 
                         
                         
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
                    text str("escalation: %s"%fight.current_enemy.escalation)
                    text str(fight.points['enemies']['onslaught'].description)
                    text str(fight.points['enemies']['maneuver'].description)
                    text str(fight.points['enemies']['fortitude'].description)
                    text str(fight.points['enemies']['excellence'].description)
                    text str("summary: %s"%(fight.summary('enemies')))
                    text 'last played card:'
                    if not fight.passed and fight.current_enemy.last_played_card != None:
                        textbutton fight.current_enemy.last_played_card.name:
                            style style.hoverable_text
                            hovered Show('sc_card_info', card=fight.current_enemy.last_played_card)
                            unhovered Hide('sc_card_info')
                            action NullAction()



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
        xalign 0.6
        yalign 0.5
        text card.show():
            xsize 350