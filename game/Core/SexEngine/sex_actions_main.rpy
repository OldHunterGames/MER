init -1 python:
    sys.path.append(renpy.loader.transfn('Core/SexEngine'))
    from sexengine import *

screen sc_sexengine_main(sexengine):
    frame:
        yalign 1.0
        vbox:
            box_reverse True
            spacing 10
            if sexengine.ended():
                textbutton 'end sex' action [Return(), Hide('sc_sexengine_info'),
                    Function(sexengine.apply_feelings)]
            else:
                if sexengine.inactive_targeted():
                    textbutton '{b}chose new target{/b}' action NullAction()
            for i in sexengine.participants:
                hbox:
                    vbox:
                        text i.name
                        if i.active:
                            imagebutton:
                                idle im.Scale(i.avatar, 100, 100)
                                hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                                hovered Show('sc_sexengine_info', info_object=i)
                                unhovered Hide('sc_sexengine_info')
                                selected sexengine.new_target is i
                                selected_idle im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.15))
                                if not sexengine.inactive_targeted():
                                    action Function(sexengine.set_target, i)
                                else:
                                    action Function(sexengine.change_target, i), Function(sexengine.get_actions)
                        else:
                            image im.Grayscale(im.Scale(i.avatar, 100, 100))
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
    window:
        xalign 1.0
        xsize 320
        yalign 0.0
        if isinstance(info_object, SexParticipant):
            vbox:
                box_wrap True
                text info_object.name
                text '%s %s %s (%s)'%(
                    info_object.age, info_object.genus.name, info_object.gender,
                    info_object.kink)
                text '{b}fetishes:{/b}'
                for i in info_object.revealed_fetishes():
                    text i
                text '{b}taboos:{/b}'
                for i in info_object.revealed_taboos():
                    text i
                text '{b}target{/b}: '
                text info_object.target.name
        else:
            vbox:
                text info_object.name
                text encolor_text(info_object.attribute, attribute)
                text '{b}pay{/b}:'
                for k, v in info_object.pay.items():
                    text '[k]: [v]'
                text '{b}markers:{/b}'
                text '{b}actor:{/b}'
                for i in info_object.colored_markers(owner, 'actor'):
                    text i
                text '{b}target:{/b}'
                for i in info_object.colored_markers(owner.target, 'target'):
                    text i

