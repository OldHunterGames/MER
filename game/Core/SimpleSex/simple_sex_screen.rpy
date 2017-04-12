init -1 python:
    sys.path.append(renpy.loader.transfn("Core/SimpleSex"))
    from SimpleSex import *

screen sc_simplesex(simplesex):
    modal True
    window:
        xfill True
        yfill True

screen sc_show_turn(simplesex):
    python:
        target = simplesex.target
        picker = simplesex.target_picker
    window:
        xfill True
        yfill True
        image simplesex.current_card.image():
            xalign 0.4
            yalign 0.5
        vbox:
            xalign 0.75
            ypos 50
            image picker.avatar()
            vbox:
                xsize 200
                box_wrap True
                xalign 0.5
                text picker.name
                text '%s %s'%(picker.sexual_suite['name'], picker.sexual_orientation['name'])
                text simplesex.get_actor_rating()

        textbutton 'Forward':
            action Return()
            xalign 0.75
            ypos 360
        vbox:
            xalign 0.75
            ypos 400
            image target.avatar()
            vbox:
                xalign 0.5
                xsize 200
                box_wrap True
                text target.name
                text '%s %s'%(target.sexual_suite['name'], target.sexual_orientation['name'])
                text simplesex.get_target_rating()

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
                    vbox:
                        imagebutton:
                            idle i.avatar((100, 100))
                            action Function(simplesex.set_target, i)
                        text i.name
                        text '%s %s'%(i.sexual_suite['name'], i.sexual_orientation['name'])
                        text i.get_rating_description(i.calc_rating())
        if simplesex.target_picker is not None:
            vbox:
                xalign 0.0
                ypos 20
                box_wrap True
                xmaximum 200
                image simplesex.target_picker.avatar()
                text simplesex.target_picker.name
                text '%s %s'%(simplesex.target_picker.sexual_suite['name'], simplesex.target_picker.sexual_orientation['name'])
                text simplesex.target_picker.get_rating_description(simplesex.target_picker.calc_rating())
        if simplesex.target is not None:
            vbox:
                xalign 0.0
                ypos 330
                box_wrap True
                xmaximum 200
                image simplesex.target.avatar()
                text simplesex.target.name
                text '%s %s'%(simplesex.target.sexual_suite['name'], simplesex.target.sexual_orientation['name'])
                text simplesex.target.get_rating_description(simplesex.target.calc_rating())

        if simplesex.target_picker is None:
            hbox:
                xalign 0.5
                yalign 1.0
                spacing 10
                for i in simplesex.get_actives():
                    vbox:
                        box_wrap True
                        imagebutton:
                            idle i.avatar((100, 100))
                            action Function(simplesex.set_target_picker, i)
                        text i.name
                        text '%s %s'%(i.sexual_suite['name'], i.sexual_orientation['name'])
                        text i.get_rating_description(i.calc_rating())

        textbutton "Choose action":
            xalign 0.6
            ypos 350
            action Return(), SensitiveIf(simplesex.target is not None and simplesex.target_picker is not None)

screen sc_pick_sexaction(simplesex):
    window:
        xfill True
        yfill True
        
        vbox:
            xmaximum 200
            box_wrap True
            image simplesex.target.avatar()
            text simplesex.get_target_rating()
            text '%s %s'%(simplesex.target.sexual_suite['name'], simplesex.target.sexual_orientation['name'])
        
        vbox:
            ypos 380
            xmaximum 200
            box_wrap True
            image simplesex.target_picker.avatar()
            text simplesex.get_actor_rating()
            text '%s %s'%(simplesex.target_picker.sexual_suite['name'], simplesex.target_picker.sexual_orientation['name'])

        imagebutton:
            xalign 0.4
            idle simplesex.current_card.image()
            action Return()
        text simplesex.current_card.name:
            xalign 0.4
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
            action Return(), Function(simplesex.finish)





