screen sc_services():
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        frame:
            xsize 350
            ysize 350
            vbox:
                for key, value in services_data.items():
                    hbox:
                        python:
                            if player.has_service(key):
                                name = encolor_text(value['name'], 'green')
                            else:
                                name = encolor_text(value['name'], 'red')
                        textbutton name:
                            style 'hoverable_text'
                            action NullAction()
                            hovered Show('sc_text_popup', text=value['description'])
                            unhovered Hide('sc_text_popup')
                        textbutton "On":
                            xsize 50
                            action [SensitiveIf(not player.has_service(key)), Function(player.add_service, key, value)]
                        textbutton "Off":
                            xsize 50
                            action [SensitiveIf(player.has_service(key)), Function(player.remove_service, key)]
                        if player.has_service(key):
                            text ' '
                            text 'Bill: %s'%value['cost']
        textbutton 'Leave':
            yalign 1.0
            action Return()