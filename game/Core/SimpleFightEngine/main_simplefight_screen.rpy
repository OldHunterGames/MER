init -10 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleFightEngine"))
    from simplefight import SimpleFight, FightQuest

screen sc_simple_fight(fight):
    if fight.get_winner() is None:
        textbutton 'end_turn':
            yalign 0.5
            action [Function(fight.end_turn), Hide('sc_chose_maneuver'), 
                SensitiveIf(all([i.active_maneuver is not None for i in fight.active_allies()]))]
    else:
        timer 0.01:
            action Return()
    frame:
        xalign 0.5
        yalign 1.0
        hbox:
            for i in fight.allies:
                vbox:
                    text i.name
                    if i.weight() is None:
                        $ txt = combat_styles_translation[i.combat_style()]
                    else:
                        $ txt = '%s %s'%(combat_weight[i.weight()], combat_styles_translation[i.combat_style()])
                    text txt
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
                    text i.name
                    if i.weight() is None:
                        $ txt = combat_styles_translation[i.combat_style()]
                    else:
                        $ txt = '%s %s'%(combat_weight[i.weight()], combat_styles_translation[i.combat_style()])
                    text txt
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
        xsize 550
        ysize 300
        viewport:
            xalign 1.0
            scrollbars 'vertical'
            draggable True
            mousewheel True
            ymaximum 550
            yfill True
            has vbox
            for i in fight.get_log().values():
                for n in i:
                    text n
            
                                

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

label lbl_simple_fight(fight, allies):

    # call screen sc_simplefight_equip(allies[0])
    call screen sc_simple_fight(fight)
    call lbl_postfight(fight)
    return fight

label lbl_postfight(fight):
    $ winner = fight.get_winner()
    $ fight.end()
    if winner != 'fleed':
        'fight winner is [winner]'
        if winner == 'allies' and not fight.friendly_fight:
            call screen sc_postfight_win(fight)
    else:
        'you fleed from fight'
    return

screen sc_postfight_win(fight):
    python:
        def take_all_items(player, items):
            to_remove = []
            for i in items:
                player.add_item(i)
                to_remove.append(i)
            for i in to_remove:
                items.remove(i)

        def take_all_corpses(player, corpses):
            to_remove = []
            for i in corpses:
                player.add_corpse(i)
                to_remove.append(i)
            for i in to_remove:
                corpses.remove(i)

        def take_all_captives(player, captives):
            to_remove = []
            for i in captives:
                player.enslave(i)
                to_remove.append(i)
            for i in to_remove:
                captives.remove(i)
    window:
        xfill True
        yfill True

        hbox:
            vbox:
                frame:
                    xsize 200

                    vbox:
                        text 'Loot'
                        for item in fight.loot:
                                textbutton item.name():
                                    action Function(player.add_item, item), Function(fight.loot.remove, item)
                textbutton 'Take all' action Function(take_all_items, player, fight.loot):
                    xsize 200
            vbox:
                frame:
                    xsize 200
                    vbox:
                        text 'Corpses'
                        for i in fight.corpses:
                            textbutton i.name:
                                action Function(player.add_corpse, i), Function(fight.corpses.remove, i)
                textbutton 'Take all' action Function(take_all_corpses, player, fight.corpses):
                    xsize 200
            vbox:
                frame:
                    xsize 200
                    vbox:
                        text 'Captives'
                        for i in fight.captives:
                            textbutton i.name:
                                action [Function(player.enslave, i), Function(fight.captives.remove, i),
                                    SensitiveIf(player.slaves.has_space())]
                # textbutton 'Take all':
                    # action [Function(take_all_captives, player, fight.captives),
                        # SensitiveIf(player.slaves.has_space())]

        textbutton 'Leave' action Return():
            yalign 1.0
