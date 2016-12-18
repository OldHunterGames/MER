init -10 python:
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
                if not sexengine.inactive_targeted():

                    textbutton 'next' action Function(sexengine.get_actions)
                else:
                    textbutton '{b}chose new target{/b}' action NullAction()
            for i in sexengine.participants:
                hbox:
                    vbox:
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
                        text 'feelings: %s'%i.feelings
                    if not sex.ended():
                        vbox:
                            for n in i.actions:
                                textbutton n.name:
                                    action Function(i.use_action, n), Function(sexengine.clear_actions)
                                    hovered Show('sc_sexengine_info', info_object=n)
                                    unhovered Hide('sc_sexengine_info')

screen sc_sexengine_info(info_object):
    window:
        xalign 1.0
        xsize 320
        yalign 0.0
        if isinstance(info_object, SexParticipant):
            vbox:
                box_wrap True
                text info_object.name
                text 'gender: %s'%info_object.gender
                text 'morphology: %s'%info_object.genus.type
                text 'standart: %s'%info_object.standart
                text '{b}anatomy:{/b}'
                for i in info_object.anatomy():
                    text i.name
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
                text '{b}pay{/b}:'
                for k, v in info_object.pay.items():
                    text '[k]: [v]'
                text '{b}markers:{/b}'
                for i in info_object.markers.values():
                    text i

