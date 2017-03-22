screen sc_simple_equip(person, look_mode=False):
    modal True
    window:
        xfill True
        yfill True
        style 'char_info_window'
        vbox:
            imagebutton:
                idle im.Scale(person.avatar_path, 200, 200)
                action Show('sc_character_info_screen', person=person, communicate=True)
                hovered Show('sc_info_popup', person=person)
                unhovered Hide('sc_info_popup')
            text 'Money: %s'%person.money
        textbutton 'Leave':
            yalign 1.0
            action Return()
        hbox:
            xalign 0.35
            spacing 5
            for i in ('weapon', 'garment', 'accesories'):
                python:
                    item = person.get_slot(i)
                    if item is None:
                        name = 'No name'
                        img = im.Scale(empty_card(), 200, 300)
                    else:
                        name = item.name()
                        img = im.Scale(item.image(), 200, 300)
                vbox:
                    imagebutton:
                        idle img
                        action Function(CardMenu(person.available_for_slot(i),
                            item, [person, i]).show, False)
                    text name:
                        xalign 0.5