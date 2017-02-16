init -1 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleSex"))
    from SimpleSex import *

screen sc_simplesex(simplesex):
    modal True
    window:
        xfill True
        yfill True

screen sc_show_turn(simplesex):
    window:
        xfill True
        yfill True
        image simplesex.current_card.image():
            xalign 0.4
            yalign 0.5
        image simplesex.target_picker.avatar():
            xalign 0.75
            ypos 80
        text simplesex.get_actor_rating():
            xalign 0.75
            ypos 285

        textbutton 'Forward':
            action Return()
            xalign 0.75
            ypos 350

        image simplesex.target.avatar():
            xalign 0.75
            ypos 440
        text simplesex.get_target_rating():
            xalign 0.75
            ypos 640

screen sc_simplesex_picktarget(simplesex):
    window:
        xfill True
        yfill True
        if simplesex.target is None and simplesex.target_picker is not None:
            hbox:
                xalign 0.5
                yalign 0.0
                spacing 10
                for i in simplesex.available_targets(simplesex.target_picker):
                    imagebutton:
                        idle i.avatar((100, 100))
                        action Function(simplesex.set_target, i)
        if simplesex.target_picker is not None:
            image simplesex.target_picker.avatar():
                xalign 0.4
                ypos 140
        if simplesex.target is not None:
            image simplesex.target.avatar():
                xalign 0.4
                ypos 380

        if simplesex.target_picker is None:
            hbox:
                xalign 0.5
                yalign 1.0
                spacing 10
                for i in simplesex.get_actives():
                    imagebutton:
                        idle i.avatar((100, 100))
                        action Function(simplesex.set_target_picker, i)

        textbutton "Choose action":
            xalign 0.6
            ypos 350
            action Return(), SensitiveIf(simplesex.target is not None and simplesex.target_picker is not None)

screen sc_pick_sexaction(simplesex):
    window:
        xfill True
        yfill True
        
        image simplesex.target.avatar()
        
        image simplesex.target_picker.avatar():
            ypos 480
        if simplesex.current_card is not None:
            text simplesex.get_actor_rating():
                ypos 690
            text simplesex.get_target_rating():
                ypos 210

            imagebutton:
                xalign 0.5
                idle simplesex.current_card.image()
                action Return()
            text simplesex.current_card.name:
                xalign 0.5
                ypos 620

        hbox:
            xalign 1.0
            spacing 5
            for i in range(0, 2):
                $ card = simplesex.current_actions[i]
                imagebutton:
                    
                    idle card.image((200, 300))
                    action Function(simplesex.swap, card)

        hbox:
            xalign 1.0
            yalign 1.0
            spacing 5
            for i in range(2, 4):
                $ card = simplesex.current_actions[i]
                imagebutton:
                    
                    idle card.image((200, 300))
                    action Function(simplesex.swap, card)

screen sc_simplesex_final(simplesex):
    window:
        xfill True
        yfill True

        image simplesex.get_player().avatar(ungray=True):
            xalign 0.5
        text str(simplesex.calc_result(simplesex.get_player())):
            xalign 0.5
            ypos 210

        $ breaker = False
        for i in range(1, len(simplesex.participants)):
            python:
                x_align = 0.25
                y_pos = 200
                participant = simplesex.participants[i]
                if i%2 == 0:
                    y_pos += 240
                elif i != 1:
                    x_align = 0.75
            vbox:
                xalign x_align
                ypos y_pos
                spacing 10
                image participant.avatar(ungray=True)
                text str(simplesex.calc_result(participant)):
                    xalign 0.5

        textbutton 'Leave':
            xalign 0.5
            yalign 1.0
            action Return()





