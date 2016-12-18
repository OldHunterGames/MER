init -10 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleFightEngine"))
    from simplefight import SimpleFight

screen sc_simple_fight(fight):
    vbox:
        if fight.get_winner() is None:
            textbutton 'end_turn':
                action Function(fight.end_turn), Hide('sc_chose_maneuver')
        elif fight.get_winner() == 'allies':
            textbutton 'You win':
                action Return(), Hide('sc_chose_maneuver')
        elif fight.get_winner() == 'fleed':
            textbutton 'You fleed' action Return(), Hide('sc_chose_maneuver')
        else:
            textbutton 'You loose':
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
                                action Show('sc_chose_maneuver', fight=fight, fighter=i)
                                selected i.active_maneuver is not None
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
                hbox:
                    vbox:
                        imagebutton:
                            idle im.Scale(i.avatar, 100, 100)
                            action Function(fight.set_target, i)
                            hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                            selected i == fight.target
                            selected_idle im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.20))
                            selected_hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.20))
                        if i.active_maneuver is not None:
                            textbutton i.active_maneuver.name:
                                xmaximum 150
                                hovered Show('sc_maneuver_info', maneuver=i.active_maneuver)
                                unhovered Hide('sc_maneuver_info')
                                action NullAction()
                                
                        
                    vbox:
                        text 'hp: %s'%str(i.hp)
                        text 'protection: %s'%str(i.defence)
                        text 'attack: %s'%str(i.attack)

screen sc_maneuver_info(maneuver):
    window:
        xalign 0.0
        yalign 0.5
        xsize 150
        ysize 200
        vbox:
            text 'targets: '
            for n in maneuver.targets:
                image im.Scale(n.avatar, 50, 50)

screen sc_target_picker(fight, maneuver):
    
    if maneuver.can_target_more():
        python:
            if maneuver.type == 'protection':
                targets = fight.allies
            else:
                targets = fight.enemies
        
        window:
            xalign 0.0
            yalign 0.5
            xsize 150
            ymaximum 400
            vbox:
                text 'chose targets'
                for i in targets:
                    if not i.inactive:
                        imagebutton: 
                            idle im.Scale(i.avatar, 50, 50)
                            hover im.MatrixColor(im.Scale(i.avatar, 50, 50), im.matrix.brightness(0.05))
                            action [SensitiveIf(maneuver.can_target_more()),
                                    Function(maneuver.add_target, i)]
                            selected i in maneuver.targets
                            selected_idle im.MatrixColor(im.Scale(i.avatar, 50, 50), im.matrix.brightness(0.10))
                            selected_hover im.MatrixColor(im.Scale(i.avatar, 50, 50), im.matrix.brightness(0.10))
                    else:
                        image im.Grayscale(im.Scale(i.avatar, 100, 100))

screen sc_chose_maneuver(fight, fighter):
    window:
        xalign 0.5
        yalign 0.5
        xsize 150
        ysize 280
        
        vbox:
            for i in fighter.maneuvers:
                textbutton i.name:
                    action [Function(fighter.activate_maneuver, i), Function(i.add_target, fight.target),
                        Hide('sc_chose_maneuver')]

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