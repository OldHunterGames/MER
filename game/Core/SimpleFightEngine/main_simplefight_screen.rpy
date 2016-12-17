init -10 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleFightEngine"))
    from simplefight import SimpleFight

screen sc_simple_fight(fight):
    vbox:
        if fight.get_winner() is None:
            textbutton 'end_turn':
                action Function(fight.end_turn), Hide('sc_target_picker')
        elif fight.get_winner() == 'allies':
            textbutton 'You win':
                action Return()
        else:
            textbutton 'You loose':
                action Return()
        if fight.selected_ally is not None:
            if fight.selected_ally.selected_maneuver is not None:
                textbutton 'activate':
                    action [SensitiveIf(fight.selected_ally.selected_maneuver.ready()),
                        Function(fight.selected_ally.activate_maneuver), Function(fight.unselect),
                        Hide('sc_target_picker')]
    frame:
        xalign 0.5
        yalign 1.0
        ysize 120
        hbox:
            for i in fight.allies:
                vbox:
                    if i.active_maneuver is not None:
                        textbutton i.active_maneuver.name:
                            xmaximum 150
                            hovered Show('sc_maneuver_info', maneuver=i.active_maneuver)
                            unhovered Hide('sc_maneuver_info')
                            action NullAction()
                    hbox:
                        imagebutton:
                            idle im.Scale(i.avatar, 100, 100)
                            hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                            action [Function(fight.select, i)]
                            selected i == fight.selected_ally
                            selected_idle im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.10))
                            selected_hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.10))
                        vbox:
                            text 'hp: %s'%str(i.hp)
                            text 'protection: %s'%str(i.defence)
                            text 'attack: %s'%(i.attack)
    if fight.selected_ally is not None:
        window:
            xalign 0.5
            yalign 0.5
            xsize 150
            ysize 280
            
            vbox:
                for i in fight.selected_ally.maneuvers:
                    textbutton i.name:
                        action Function(fight.selected_ally.select_maneuver, i), Show('sc_target_picker', fight=fight, maneuver=i)
                        selected i == fight.selected_ally.selected_maneuver
    frame:
        xalign 0.5
        yalign 0.0
        xsize 250
        hbox:
            for i in fight.enemies:
                hbox:
                    vbox:
                        imagebutton:
                            idle im.Scale(i.avatar, 100, 100)
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
                    imagebutton: 
                        idle im.Scale(i.avatar, 50, 50)
                        hover im.MatrixColor(im.Scale(i.avatar, 50, 50), im.matrix.brightness(0.05))
                        action [SensitiveIf(maneuver.can_target_more()),
                                Function(maneuver.add_target, i)]
                        selected i in maneuver.targets
                        selected_idle im.MatrixColor(im.Scale(i.avatar, 50, 50), im.matrix.brightness(0.10))
                        selected_hover im.MatrixColor(im.Scale(i.avatar, 50, 50), im.matrix.brightness(0.10))

label lbl_simple_fight(allies, enemies):

    python:
        
        fight = SimpleFight(allies, enemies)
    call screen sc_simple_fight(fight)
    call lbl_postfight(fight)
    return fight

label lbl_postfight(fight):
    $ winner = fight.get_winner()
    'fight winner is [winner]'