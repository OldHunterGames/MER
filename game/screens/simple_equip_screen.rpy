init python:
    class UnequipCard(MenuCard):
        def __init__(self, person, slot):
            super(UnequipCard, self).__init__('Unequip', 'Unequip Item')
            self.slot = slot
            self.person = person

        def _run(self, *args, **kwargs):
            self.person.equip_on_slot(self.slot, None)

    class EquipCard(Card):

        def __init__(self, person, item, slot, *args, **kwargs):
            self._person = person
            self._item = item
            self._slot = slot

        def name(self):
            return self._item.name()

        def description(self):
            return self._item.description()

        def image(self):
            return self._item.image()

        def _run(self):
            self._person.equip_on_slot(self._slot, self._item)


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
            for i in ('weapon', 'garment', 'accessories'):
                python:
                    item = person.get_slot(i).get_item()
                    if item is None:
                        name = i
                        img = im.Scale(card_back(), 200, 300)
                    else:
                        name = item.name()
                        img = im.Scale(item.image(), 200, 300)
                        item = EquipCard(person, person.get_slot(i).get_item(), i)
                    items = [
                        EquipCard(person, j, i) for j in person.available_for_slot(i)]

                    if person.get_slot(i).current is not None:
                        items.append(
                            UnequipCard(person, i))
                vbox:
                    imagebutton:
                        idle img
                        action Function(CardMenu(items,
                            item).show, False)
                    text name:
                        xalign 0.5
        python:
            size = person.main_hand.size
            items =items = [
                        EquipCard(person, j, 'weapon2') for j in person.available_for_slot('weapon2')]
            if person.get_slot('weapon2').current is not None:
                        items.append(
                            UnequipCard(person, 'weapons2'))
            if size == 'twohand':
                name = person.main_hand.name()
                img = im.Scale(im.Grayscale(person.main_hand.image()), 200, 300)
            else:
                name = person.other_hand.name()
                img = im.Scale(person.other_hand.image(), 200, 300)
            current = EquipCard(person, person.other_hand, 'weapon2')

        vbox:
            xpos 230
            ypos 330    
            imagebutton:
                idle img
                action If(person.main_hand.size=='twohand', NullAction(),
                    false=Function(CardMenu(items, current).show, False))
            text name:
                xalign 0.5



