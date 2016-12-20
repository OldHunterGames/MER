init -1 python:
    sys.path.append(renpy.loader.transfn('Core/SexEngine'))
    from sexengine import *

screen sc_sexengine_main(sexengine):
    frame:
        if sexengine.ended():
            textbutton 'end sex' action [Return(), Hide('sc_sexengine_info'),
                Function(sexengine.apply_feelings)]:
                    yalign 0.5
        else:
            if sexengine.inactive_targeted():
                textbutton '{b}chose new target{/b}' action NullAction():
                    yalign 0.5
        vbox:
            box_reverse True
            spacing 10
            hbox:
                for i in sexengine.participants:
                    vbox:
                        text i.name
                        hbox:
                            if i.active:
                                imagebutton:
                                    idle im.Scale(i.avatar, 100, 100)
                                    hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                                    hovered Show('sc_sexengine_info', info_object=i)
                                    unhovered Hide('sc_sexengine_info')
                                    selected sexengine.new_target is i
                                    selected_idle im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.15))
                                    if not sexengine.inactive_targeted():
                                        action If(not i == sexengine.player(), Function(sexengine.set_target, i), NullAction())
                                    else:
                                        action If(not i == sexengine.player(), Function(sexengine.change_target, i),
                                            Function(sexengine.get_actions), NullAction())
                            else:
                                image im.Grayscale(im.Scale(i.avatar, 100, 100))
                            vbox:
                                text 'drive: %s'%i.drive
                                text 'stamina: %s'%i.stamina
                                text 'feelings: %s(%s)'%(i.feelings, i.standart)
                        if not sex.ended():
                            vbox:
                                for n in i.actions:
                                    textbutton n.name:
                                        action Function(i.use_action, n), Function(sexengine.clear_actions)
                                        hovered Show('sc_sexengine_info', info_object=n, owner=i)
                                        unhovered Hide('sc_sexengine_info')

screen sc_sexengine_info(info_object, owner=None):
    python:
        if owner is not None:
            attribute = getattr(owner, info_object.attribute)
    if isinstance(info_object, SexParticipant):
        hbox:
            yalign 1.0
            window:
                xmaximum 250
                ysize 400
                vbox:
                    text '{b}fetishes:{/b}'
                    for i in info_object.revealed_fetishes():
                        text i
            window:
                ysize 400
                xmaximum 250
                vbox:
                    text '{b}taboos:{/b}'
                    for i in info_object.revealed_taboos():
                        text i
            window:
                ysize 150
                xmaximum 250
                vbox:
                    text info_object.name
                    text '%s %s %s (%s)'%(
                        info_object.age, info_object.genus.name, info_object.gender,
                        info_object.kink)


       
    else:
        window:
            xalign 0.0
            yalign 1.0
            xmaximum 250
            ysize 400
            vbox:
                text info_object.name
                text encolor_text(info_object.attribute, attribute)
                text '{b}pay{/b}:'
                for k, v in info_object.pay.items():
                    text '[k]: [v]'
                text '{b}markers:{/b}'
                text '{b}%s:{/b}'%owner.name
                for i in info_object.colored_markers(owner, 'actor'):
                    text i
                text '{b}%s:{/b}'%owner.target.name
                for i in info_object.colored_markers(owner.target, 'target'):
                    text i

label lbl_discover_dirty(who, what):
    who.person '[what]'
    return

