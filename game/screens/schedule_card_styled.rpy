init python:
    picker = None


screen sc_schedule(person, return_=False):
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
            xalign 0.3
            for i in ('job', 'accommodation', 'ration'):
                vbox:
                    imagebutton:
                        idle getattr(person, i).image()
                        action Show('sc_pick_schedule', person=person, type_=i), SetVariable('picker',
                            ActionPicker(getattr(person.schedule, 'available_'+i+'s')(core.current_world.name)))
                    text getattr(person, i).name:
                        xalign 0.5
        hbox:
            xalign 0.3
            yalign 1.0
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
                        action Show('sc_pick_schedule', person=person, type_='optional', slot=key), SetVariable('picker',
                            ActionPicker(getattr(person.schedule, 'available_'+'optionals')(core.current_world.name)))
                    text txt:
                        xalign 0.5

init python:
    class ActionPicker(object):

        def __init__(self, cards_list):
            self.cards_list = cards_list
            self.current_card = None
        
        def swap(self, old_card, new_card):
            index = self.cards_list.index(old_card)
            self.cards_list.insert(index, new_card)
            self.cards_list.remove(old_card)
            self.set_card(old_card)

        def set_card(self, card):
            self.current_card = card
            try:
                self.cards_list.remove(card)
            except ValueError:
                pass

screen sc_pick_schedule(person, type_, slot=None):
    modal True
    
    python:
        if picker.current_card is None:
            if slot is None:
                if getattr(person, type_) is not None:
                    picker.set_card(getattr(person, type_))
            else:
                if person.schedule.get_optional(slot) is not None:
                    picker.set_card(person.schedule.get_optional(slot))
        available = getattr(person.schedule, 'available_'+type_+'s')(core.current_world.name)
        setter = getattr(person.schedule, 'set_'+type_)
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
                            action Function(picker.swap, i, picker.current_card)
                        text i.name:
                            xalign 0.5
        vbox:
            xpos 900
            xsize 380
            box_wrap True
            imagebutton:
                idle im.Scale(img, 300, 400)
                
                action [If(slot is None, Function(setter, picker.current_card), 
                    false=Function(setter, slot, picker.current_card)), Hide('sc_pick_schedule'),
                    SensitiveIf(picker.current_card is not None)]
                xalign 0.5
            if picker.current_card is not None:
                text picker.current_card.description:
                    xalign 0.5
                    xmaximum 400


    textbutton 'leave':
            xalign 0.5
            yalign 1.0
            action Hide('sc_pick_schedule')
