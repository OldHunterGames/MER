init -10 python:
    sys.path.append(renpy.loader.transfn('Core/SexEngine'))
    from sexengine import *

screen sc_sexengine_main(sexengine):
    frame:
        yalign 1.0
        vbox:
            box_reverse True
            spacing 10
            for i in sexengine.participants:
                hbox:
                    vbox:
                        text 'drive: %s'%i.drive
                        text 'stamina: %s'%i.stamina
                        imagebutton:
                            idle im.Scale(i.avatar, 100, 100)
                            hover im.MatrixColor(im.Scale(i.avatar, 100, 100), im.matrix.brightness(0.05))
                            action NullAction()
                    vbox:
                        for n in i.actions:
                            textbutton n.name