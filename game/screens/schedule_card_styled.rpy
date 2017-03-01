init python:
    picker = None


screen sc_schedule(person, return_=False):
    modal True
    window:
        xfill True
        yfill True
        vbox:
            imagebutton:
                idle im.Scale(person.avatar_path, 200, 200)
                action Show('sc_character_info_screen', person=person, communicate=True)
                hovered Show('sc_info_popup', person=person)
                unhovered Hide('sc_info_popup')
            text 'LIFESTYLE'
            text 'Money: %s'%person.money
            text 'Bill: %s'%person.decade_bill()
        textbutton 'Leave':
            yalign 1.0
            action If(return_, Return(), false=Hide('sc_schedule'))
        hbox:
            xalign 0.35
            spacing 5
            for i in ('job', 'accommodation', 'ration'):
                vbox:
                    imagebutton:
                        idle getattr(person, i).image()
                        action Show('sc_pick_schedule', person=person), SetVariable('picker',
                            ActionPicker(getattr(person.schedule, 'available_'+i+'s')(core.current_world.name), None, i))
                    text getattr(person, i).name:
                        xalign 0.5
        hbox:
            xalign 0.35
            yalign 1.0
            spacing 5
            for key, value in person.schedule.get_all_optionals().items():
                python:
                    if value is None:
                        img = im.Scale(empty_card(), 200, 300)
                        txt = __("Free slot")
                    else:
                        img = value.image()
                        txt = value.name
                vbox:
                    imagebutton:
                        idle img
                        action Show('sc_pick_schedule', person=person), SetVariable('picker',
                            ActionPicker(getattr(person.schedule, 'available_'+'optionals')(core.current_world.name), key, 'optional'))
                    text txt:
                        xalign 0.5

init python:
    class ActionPicker(object):

        def __init__(self, cards_list, slot, type_):
            self._cards_list = cards_list
            self.current_card = None
            self.slot = slot
            self.type = type_

        @property
        def cards_list(self):
            return sorted(self._cards_list, key=lambda card: card.name)

        def set_card(self, card):
            if self.current_card is not None:
                self._cards_list.append(self.current_card)
            self.current_card = card
            try:
                self._cards_list.remove(card)
            except ValueError:
                pass

screen sc_pick_schedule(person):
    modal True
    python:
        if picker.current_card is None:
            if picker.slot is None:
                if getattr(person, picker.type) is not None:
                    picker.set_card(getattr(person, picker.type))
            else:
                if person.schedule.get_optional(picker.slot) is not None:
                    picker.set_card(person.schedule.get_optional(picker.slot))
        available = getattr(person.schedule, 'available_'+picker.type+'s')(core.current_world.name)
        setter = getattr(person.schedule, 'set_'+picker.type)
        if picker.current_card is None:
            img = card_back()
        else:
            img = picker.current_card.image()

    window:
        xfill True
        yfill True
        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xmaximum 880
            hbox:
                xmaximum 880
                box_wrap True
                spacing 5
                for i in picker.cards_list:
                    vbox:
                        imagebutton:
                            idle i.image()
                            action Function(picker.set_card, i)
                        text i.name:
                            xalign 0.5
        vbox:
            xpos 900
            xsize 380
            box_wrap True
            imagebutton:
                idle im.Scale(img, 300, 400)
                
                action [If(picker.slot is None, Function(setter, picker.current_card), 
                    false=Function(setter, picker.slot, picker.current_card)), Hide('sc_pick_schedule'),
                    SensitiveIf(picker.current_card is not None)]
                xalign 0.5
            if picker.current_card is not None:
                text picker.current_card.description:
                    xalign 0.5
                    xmaximum 400

    vbox:
        xalign 0.5
        yalign 1.0
        textbutton 'leave':
            action Hide('sc_pick_schedule')
        if picker.slot is not None:
            textbutton "Remove":
                action Function(setter, picker.slot, None), Hide('sc_pick_schedule')

    on 'hide':
        action SetVariable('picker', None)
