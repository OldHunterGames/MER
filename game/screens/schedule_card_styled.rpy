init python:
    picker = None


screen sc_schedule(person, return_=False):
    modal True
    window:
        xfill True
        yfill True
        style 'char_info_window'
        vbox:
            imagebutton:
                idle im.Scale(person.avatar_path, 150, 150)
                action If(return_, Return(), false=Hide('sc_schedule'))
                hovered Show('sc_info_popup', person=person)
                unhovered Hide('sc_info_popup')
            text core.get_lifestyle(person)
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
                            ActionPicker(person.schedule.available(i, core.current_world.name), None, i))
                    text getattr(person, i).name():
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
                        txt = value.name()
                vbox:
                    imagebutton:
                        idle img
                        action Show('sc_pick_schedule', person=person), SetVariable('picker',
                            ActionPicker(person.schedule.available('optional', core.current_world.name), key, 'optional'))
                    text txt:
                        xalign 0.5
    on 'hide':
        action Hide('sc_info_popup')

init python:
    class ActionPicker(object):

        def __init__(self, cards_list, slot, type_):
            self._cards_list = cards_list
            self.current_card = None
            self.slot = slot
            self.type = type_

        @property
        def cards_list(self):
            return sorted(self._cards_list, key=lambda card: card.name())

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
        setter = person.schedule.set
        if picker.slot is not None:
            setter = person.schedule.set_optional
        if picker.current_card is None:
            if picker.slot is None:
                if getattr(person, picker.type) is not None:
                    picker.set_card(getattr(person, picker.type))
            else:
                if person.schedule.get_optional(picker.slot) is not None:
                    picker.set_card(person.schedule.get_optional(picker.slot))
        available = person.schedule.available(picker.type, core.current_world.name)
        
        if picker.current_card is None:
            img = card_back()
        else:
            img = picker.current_card.image()

    window:
        style 'char_info_window'
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
                        xsize 200
                        box_wrap True
                        imagebutton:
                            idle i.image()
                            action Function(picker.set_card, i)
                        text i.name():
                            xalign 0.5
                if picker.slot is not None:
                    vbox:
                        imagebutton:
                            idle im.Scale(card_back(), 200, 300)
                            action Function(setter, picker.slot, None), Hide('sc_pick_schedule')

        vbox:
            xpos 900
            xsize 380
            box_wrap False
            imagebutton:
                idle im.Scale(img, 300, 400)
                
                action [If(picker.slot is None, Function(setter, picker.type, picker.current_card), 
                    false=Function(setter, picker.slot, picker.current_card)), Hide('sc_pick_schedule'),
                    SensitiveIf(picker.current_card is not None)]
                xalign 0.5
            if picker.current_card is not None:
                viewport:
                    scrollbars 'vertical'
                    draggable True
                    mousewheel True
                    xmaximum 380
                    text picker.current_card.description():
                        xalign 0.5
                        xmaximum 380

    vbox:
        xalign 0.5
        yalign 1.0

    on 'hide':
        action SetVariable('picker', None)
