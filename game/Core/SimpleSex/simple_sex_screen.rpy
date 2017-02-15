init -1 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleSex"))
    from SimpleSex import *

label lbl_simplesex(simplesex):
    python:
        simplesex.npc_act()

screen sc_simplesex(simplesex):
    modal True
    window:
        xfill True
        yfill True

screen sc_show_npc_turn(participant):
    window:
        xfill True
        yfill True
        image participant.action.image():
            xalign 0.4
            yalign 0.5
        image participant.avatar():
            xalign 0.75
            ypos 80
        text participant.get_rating_description():
            xalign 0.75
            ypos 285

        textbutton 'Forward':
            action Return()
            xalign 0.75
            ypos 350

        image participant.target.avatar():
            xalign 0.75
            ypos 440
        text participant.target.get_rating_description():
            xalign 0.75
            ypos 640



