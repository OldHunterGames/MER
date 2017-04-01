style hoverable_text is text:
    color '#fff'
    underline True
    hover_background '#fff'
style char_info_window is window:
    background Color((0, 0, 0, 255))

style gray_button is button:
    idle_background Frame(im.Grayscale('interface/bg_base.jpg'),0,0)
    hover_background Frame(im.Grayscale('interface/bg_base.jpg'),0,0)



screen sc_character_info_screen(person, return_l=False, communicate=False):
    modal True
    window:
        xfill True
        yfill True
        frame:
            xsize 960
            ysize 160
            hbox:
                spacing 10
                image im.Scale(person.avatar_path, 150, 150)
                vbox:
                    python:
                        energy_text = utilities.encolor_text(__('Energy'), person.energy)
                        if person.player_controlled or person.master == core.player:
                            items_look_mode = False
                        else:
                            items_look_mode = True
                    if person.player_controlled:
                        textbutton energy_text: 
                            action [SensitiveIf(person.energy > 0), 
                                    Function(renpy.call_in_new_context, 'lbl_edge_opportunities')]
                    else:
                        textbutton 'Energy':
                            style 'gray_button'
                            action NullAction()
                    textbutton 'Schedule':
                        action [SensitiveIf(person.player_controlled or
                                person.master == core.player), Show('sc_schedule', person=person)]
                    textbutton 'Equipment':
                        action [SensitiveIf(person.player_controlled or 
                                person.any_equiped()), Show('sc_simple_equip', person=person, look_mode=items_look_mode)]
                    textbutton 'Done': 
                        action If(return_l, Return(), false=Hide('sc_character_info_screen'))

                vbox:
                    for i in ['physique', 'mind', 'spirit', 'agility']:
                        python:
                            txt = encolor_text(attributes_translation[i], getattr(person, i))
                        text txt

                vbox:
                    for i in ['physique', 'mind', 'spirit', 'agility']:
                        python:
                            skill = skills_translation[i]
                            txt = encolor_text(attributes_translation[i], getattr(person, i))
                            if skill is not None:
                                txt = encolor_text(skill, person.skill(i)+2)
                        if skill > 0:
                            text txt
        frame:
            xsize 960
            ypos 161
            ysize 550
            text DescriptionMaker(person).description()

        frame:
            xpos 961
            xsize 310
            ysize 200
            vbox:
                text encolor_text(__('Allure'), person.allure())
                text encolor_text(__('Hardiness'), person.hardiness())
                text encolor_text(__('Succulence'), person.succulence())
                text encolor_text(__('Purity'), person.purity())
                text encolor_text(__('Exotic'), person.exotic())
                text encolor_text(__('Style'), person.style())
                text encolor_text(__('Menace'), person.menace())
        frame:
            xpos 961
            ypos 201
            python:
                card_x_size = 310
                card_y_size = 500
            if person.player_controlled:
                imagebutton:  
                    idle im.Scale('images/tarot/card_deck.jpg', card_x_size, card_y_size)
                    action Show('sc_tokens', person=player)
            elif communicate:
                if player.has_energy():
                    imagebutton:
                        idle im.Scale(person.get_token_image(), card_x_size, card_y_size)
                        hover im.MatrixColor(im.Scale(person.get_token_image(), card_x_size, card_y_size), im.matrix.brightness(0.05))
                        action Function(core.shift_relations, person) 
                else:
                    imagebutton:
                        idle im.Grayscale(im.Scale(person.get_token_image(), card_x_size, card_y_size))
                        hovered Show('sc_text_popup', text=__("Not enough energy"))
                        unhovered Hide('sc_text_popup')
                        action NullAction()

init python:
    active_determination = None

screen sc_tokens(person):
    $ tokens = person.inner_resources
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        hbox:
            box_wrap True
            for i in person.active_resources:
                image im.Scale(i.image, 150, 250)


        textbutton 'Leave' action Hide('sc_tokens'):
            xalign 0.5
            yalign 1.0
            xsize 200
       
screen sc_info_popup(person):
    python:
        if player.know_person(person):
            relations = player.relations(person)
        else:
            relations = None

    window:
        xsize 300
        ysize 300
        yalign 0.5
        text person.name:
            xalign 0.5
        vbox:
            yalign 0.15
            python:
                line1 = '{person.age} {person.gender} {person.genus.name}'.format(person=person)
                line2 = '{0} {1} {2}'.format(*person.alignment.description())
                sexual_suite = person.sexual_suite['name']
                orientation = person.sexual_orientation['name']
                line3 = '{0} {1}'.format(sexual_suite, orientation)
            text line1
            text line2
            text line3
            if relations is not None:
                text DescriptionMaker(person).relations_text(protected=False)

              
screen sc_weapon_info(weapon):
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            spacing 5
            text weapon.stats()
            if weapon.description() is not None:
                text weapon.description()
            text 'price: ' + str(weapon.price)

screen sc_vitality_info(person):
    $ d, l = person.vitality_info()
    python:
        list_ = list(d.items())
        for i in l:
            list_.append(i)
    frame:
        xalign 0.5
        yalign 0.5
        hbox:
            spacing 10
            vbox:
                text 'Good'
                for k, v in list_:
                    if v > 0:
                        text encolor_text(k, v)
            vbox:
                text 'Bad'
                for k, v in list_:
                    if v < 0:
                        text encolor_text(k, 0)
            vbox:
                text 'Nonfactors'
                for k, v in list_:
                    if v == 0:
                        text encolor_text(k, 6)


screen sc_text_popup(text):
    frame:
        xalign 0.5
        yalign 0.5
        text text
