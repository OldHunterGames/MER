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
                        action Show('sc_pick_schedule', person=person, type_=i)
                    text getattr(person, i).name:
                        xalign 0.5
        hbox:
            xalign 0.3
            yalign 1.0
            for key, value in person.schedule.get_optional().items():
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
                        action Show('sc_pick_optional', person=person, slot=key)
                    text txt:
                        xalign 0.5

screen sc_pick_optional(person, slot):
    modal True
    window:
        xfill True
        yfill True
        hbox:
            box_wrap True
            for i in person.schedule.available_optionals(core.current_world):
                vbox:
                    imagebutton:
                        idle i.image()
                        action Function(person.schedule.set_optional(slot, i)), Hide('sc_pick_optional')
                    text i.name:
                        xalign 0.5
        textbutton 'leave':
            xalign 0.5
            yalign 1.0
            action Hide('sc_pick_optional')

screen sc_pick_schedule(person, type_):
    modal True
    $ available = getattr(person.schedule, 'available_'+type_+'s')(core.current_world.name)
    $ setter = getattr(person.schedule, 'set_'+type_)
    window:
        xfill True
        yfill True
        hbox:
            box_wrap True
            for i in available:
                vbox:
                    imagebutton:
                        idle i.image()
                        action Function(setter, i), Hide('sc_pick_schedule')
                    text i.name:
                        xalign 0.5
    textbutton 'leave':
            xalign 0.5
            yalign 1.0
            action Hide('sc_pick_schedule')
