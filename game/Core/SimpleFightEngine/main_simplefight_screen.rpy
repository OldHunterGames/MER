init -10 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleFightEngine"))
    from simplefight import SimpleFight

screen sc_simple_fight(fight):
    tag overlay_hud
    if fight.get_winner() is None:
        textbutton 'end_turn':
            yalign 0.5
            action Function(fight.end_turn), Hide('sc_chose_maneuver')
    elif fight.get_winner() == 'allies':
        textbutton 'You win':
            yalign 0.5
            action Return(), Hide('sc_chose_maneuver')
    elif fight.get_winner() == 'fleed':
        yalign 0.5
        textbutton 'You fleed' action Return(), Hide('sc_chose_maneuver')
    else:
        textbutton 'You loose':
            yalign 0.5
            action Return(), Hide('sc_chose_maneuver')
    frame:
        xalign 0.5
        yalign 1.0
        hbox:
            for i in fight.allies:
                vbox:
                    
                    hbox:
                        if not i.inactive:
                            imagebutton:
                                idle im.Scale(i.avatar, 100, 100)
                                hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                                action [If(fight.selected_ally == i, Show('sc_chose_maneuver', fight=fight, fighter=i)),
                                    If(fight.selected_ally != i, [Function(fight.select, i), Hide('sc_chose_maneuver')])]
                                selected fight.selected_ally == i
                                selected_idle im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.10))
                                selected_hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.10))
                        else:
                            image im.Grayscale(im.Scale(i.avatar, 100, 100))
                        vbox:
                            text 'hp: %s'%str(i.hp)
                            text 'protection: %s'%str(i.defence)
                            text 'attack: %s'%(i.attack)
                    if i.active_maneuver is not None:
                        textbutton i.active_maneuver.name:
                            xmaximum 150
                            hovered Show('sc_maneuver_info', maneuver=i.active_maneuver)
                            unhovered Hide('sc_maneuver_info')
                            action NullAction()
                    

    frame:
        xalign 0.5
        yalign 0.0
        hbox:
            for i in fight.enemies:
                vbox:
                    hbox:
                        if not i.inactive:
                            imagebutton:
                                idle im.Scale(i.avatar, 100, 100)
                                action Function(fight.selected_ally.set_target, i)
                                hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                                selected i == fight.selected_ally.target
                                selected_idle im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.20))
                                selected_hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.20))
                        else:
                            image im.Grayscale(im.Scale(i.avatar, 100, 100))
                        vbox:
                            text 'hp: %s'%str(i.hp)
                            text 'protection: %s'%str(i.defence)
                            text 'attack: %s'%str(i.attack)
                    if i.active_maneuver is not None:
                        textbutton i.active_maneuver.name:
                            xmaximum 150
                            hovered Show('sc_maneuver_info', maneuver=i.active_maneuver)
                            unhovered Hide('sc_maneuver_info')
                            action NullAction()

    frame:
        xalign 1.0
        yalign 0.5
        xsize 500
        ysize 350
        viewport:
            xalign 1.0
            scrollbars 'vertical'
            draggable True
            mousewheel True
            ymaximum 550
            yfill True
            has vbox
            for i in fight.get_log():
                text i
            
                                

screen sc_chose_maneuver(fight, fighter):
    window:
        xalign 0.5
        yalign 0.5
        xsize 170
        ysize 280
        vbox:
            for i in fighter.maneuvers:
                textbutton i.name:
                    xmaximum 170
                    action [Function(fighter.activate_maneuver, i), Function(i.add_target, fighter.target),
                        Hide('sc_chose_maneuver'), Hide('sc_maneuver_info')]
                    hovered Show('sc_maneuver_info', maneuver=i)
                    unhovered Hide('sc_maneuver_info')

screen sc_maneuver_info(maneuver):
    window:
        xalign 0.0
        yalign 0.5
        xsize 200
        ysize 250
        vbox:
            text maneuver.name
            text maneuver.description
            hbox:
                for i in maneuver.targets:
                    image im.Scale(i.avatar, 50, 50) 

label lbl_simple_fight(allies, enemies):

    python:
        
        fight = SimpleFight(allies, enemies)
    call screen sc_simple_fight(fight)
    call lbl_postfight(fight)
    return fight

label lbl_postfight(fight):
    $ winner = fight.get_winner()
    if winner != 'fleed':
        'fight winner is [winner]'
    else:
        'you fleed from fight'
    return