screen sc_schedule_organaizer():
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        frame:
            xsize 350
            ysize 350
            vbox:
                for key, value in player.available_services().items():
                    $ has_service = player.has_service(key)
                    hbox:
                        python:
                            if has_service:
                                name = encolor_text(value['name'], 'green')
                            else:
                                name = encolor_text(value['name'], 'red')
                        textbutton name:
                            style 'hoverable_text'
                            action NullAction()
                            hovered Show('sc_text_popup', text=value['description'])
                            unhovered Hide('sc_text_popup')
                        if not has_service:
                            textbutton "Off":
                                xsize 50
                                action Function(player.add_service, key)
                        else:
                            textbutton "On":
                                xsize 50
                                action Function(player.remove_service, key)
                        if has_service:
                            text ' '
                            text 'Bill: %s'%value['cost']
        textbutton player.job:
            action Show('sc_job_picker')
            hovered Show('sc_text_popup', text=player.job_description())
            unhovered Hide('sc_text_popup')
            xsize 200
            yminimum 30
            xpos 355

        textbutton player.accommodation:
            action Show('sc_accomodation_picker')
            hovered Show('sc_text_popup', text=player.accommodation_description())
            unhovered Hide('sc_text_popup')
            xsize 200
            yminimum 30
            xpos 555

        textbutton player.overtime:
            action Show('sc_overtime_picker')
            hovered Show('sc_text_popup', text=player.overtime_description())
            unhovered Hide('sc_text_popup')
            xsize 200
            yminimum 30
            xpos 755
        
        frame:
            xsize 200
            ysize 140
            yalign 0.8
            vbox:
                text 'Allowance: %s'%player.pocket_money
                hbox:
                    spacing 5
                    vbox:
                        textbutton '1':
                            action Function(player.add_pocket_money, 1)
                        textbutton '10':
                            action Function(player.add_pocket_money, 10)
                        textbutton '100':
                            action Function(player.add_pocket_money, 100)
                    vbox:
                        textbutton '1':
                            action Function(player.remove_pocket_money, 1)
                        textbutton '10':
                            action Function(player.remove_pocket_money, 10)
                        textbutton '100':
                            action Function(player.remove_pocket_money, 100)

        text 'Total: %s'%player.decade_bill:
            yalign 0.95    
        textbutton 'Leave':
            yalign 1.0
            action Hide('sc_schedule_organaizer')
    on 'hide':
        action Hide('sc_text_popup'), Hide('sc_job_picker')

screen sc_job_picker():
    tag picker
    frame:
        ypos 45
        xpos 360
        xsize 200
        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xsize 200
            ysize 350
            vbox:
                for key, value in player.available_jobs().items():
                    textbutton value['name']:
                        xsize 180
                        action [Function(player.set_job, key), Hide('sc_job_picker')]
                        hovered Show('sc_text_popup', text=value['description'])
                        unhovered Hide('sc_text_popup')
    on 'hide':
        action Hide('sc_text_popup')

screen sc_accomodation_picker():
    tag picker
    frame:
        ypos 45
        xpos 560
        xsize 200
        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xsize 200
            ysize 350
            vbox:
                for key, value in player.available_accommodations().items():
                    textbutton value['name']:
                        xsize 180
                        action [Function(player.set_accommodation, key), Hide('sc_accomodation_picker')]
                        hovered Show('sc_text_popup', text=value['description'])
                        unhovered Hide('sc_text_popup')
    on 'hide':
        action Hide('sc_text_popup')

screen sc_overtime_picker():
    tag picker
    frame:
        ypos 45
        xpos 760
        xsize 200
        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xsize 200
            ysize 350
            vbox:
                for key, value in player.available_overtimes().items():
                    textbutton value['name']:
                        xsize 180
                        action [Function(player.set_overtime, key), Hide('sc_overtime_picker')]
                        hovered Show('sc_text_popup', text=value['description'])
                        unhovered Hide('sc_text_popup')
    on 'hide':
        action Hide('sc_text_popup')