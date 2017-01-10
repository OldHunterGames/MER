screen sc_services():
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        frame:
            xsize 350
            ysize 350
            vbox:
                for key, value in available_services():
                    $ data = services_data[value['name']]
                    $ has_service = player_has_servicee(value['name'])
                    hbox:
                        python:
                            if has_service(value['name']):
                                name = encolor_text(data['name'], 'green')
                            else:
                                name = encolor_text(data['name'], 'red')
                        textbutton name:
                            style 'hoverable_text'
                            action NullAction()
                            hovered Show('sc_text_popup', text=data['description'])
                            unhovered Hide('sc_text_popup')
                        if not has_service:
                            textbutton "Off":
                                xsize 50
                                action Function(player.add_service, value['name'], data['spends'])
                        else:
                            textbutton "On":
                                xsize 50
                                action Function(player.remove_service, value['name'])
                        if has_service:
                            text ' '
                            text 'Bill: %s'%value['cost']
        textbutton jobs_data[player.job]['name']:
            action Show('sc_job_picker')
            hovered Show('sc_text_popup', text=jobs_data[player.job]['description'])
            unhovered Hide('sc_text_popup')
            xsize 150
            ysize 30
            xpos 355
        
        text 'Total: %s'%player.decade_bill:
            yalign 0.95    
        textbutton 'Leave':
            yalign 1.0
            action Return()

screen sc_job_picker():
    frame:
        ypos 31
        vbox:
            for key, value in available_jobs().items():
                $ name = value['world'] + '_' + value['name']
                $ data = jobs_data[name]
                $ skill = data['skill']
                $ difficulty = data['difficulty']
                textbutton data['name']:
                    action [Function(player.schedule.set_job, value['name'], skill, difficulty=difficulty),
                        Hide('sc_job_picker')]
                    hovered Show('sc_text_popup', text=data['description'])
                    unhovered Hide('sc_text_popup')
    on 'hide':
        action Hide('sc_text_popup')
