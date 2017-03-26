init python:
    class UnequipCard(MenuCard):
        def __init__(self, person, slot):
            super(UnequipCard, self).__init__('Unequip', 'Unequip Item')
            self.slot = slot
            self.person = person

        def _run(self, *args, **kwargs):
            self.person.equip_on_slot(self.slot, None)


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
            action Hide('sc_simple_equip')
        hbox:
            xalign 0.35
            spacing 5
            for i in ('weapon', 'garment', 'accesories'):
                python:
                    item = person.get_slot(i).get_item()
                    if item is None:
                        name = i
                        img = im.Scale(card_back(), 200, 300)
                    else:
                        name = item.name()
                        img = im.Scale(item.image(), 200, 300)
                    items = person.available_for_slot(i)
                    if person.get_slot(i).current is not None:
                        items.append(
                            UnequipCard(person, i))
                vbox:
                    imagebutton:
                        idle img
                        action Function(CardMenu(items,
                            item, [person, i]).show, False)
                    text name:
                        xalign 0.5
        python:
            size = person.main_hand.size
            items = person.available_for_slot('weapon2')
            if size == 'twohand':
                name = person.main_hand.name()
                img = im.Scale(im.Grayscale(person.main_hand.image()), 200, 300)
            else:
                name = person.other_hand.name()
                img = im.Scale(person.other_hand.image(), 200, 300)

        vbox:
            xpos 230
            ypos 330    
            imagebutton:
                idle img
                action If(person.main_hand.size=='twohand', NullAction(),
                    false=Function(CardMenu(items, person.other_hand, [person, 'weapon2']).show, False))
            text name:
                xalign 0.5



