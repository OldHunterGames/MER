screen sc_schedule_organaizer():
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'

        textbutton player.job.name:
            action ShowTransient('sc_schedule_picker', x_pos=360, items=player.schedule.available_jobs(core.current_world.name),
                setter_func=player.schedule.set_job)
            hovered Show('sc_text_popup', text=player.job.description)
            unhovered Hide('sc_text_popup')
            sensitive not player.job.locked
            xsize 200
            yminimum 30
            xpos 355

        textbutton player.accommodation.name:
            action ShowTransient('sc_schedule_picker', x_pos=560, items=player.schedule.available_accommodations(core.current_world.name),
                setter_func=player.schedule.set_accommodation)
            hovered Show('sc_text_popup', text=player.accommodation.description)
            unhovered Hide('sc_text_popup')
            sensitive not player.accommodation.locked
            xsize 200
            yminimum 30
            xpos 555

        textbutton player.overtime.name:
            action ShowTransient('sc_schedule_picker', x_pos=760, items=player.schedule.available_overtimes(core.current_world.name),
                setter_func=player.schedule.set_overtime)
            hovered Show('sc_text_popup', text=player.overtime.description)
            unhovered Hide('sc_text_popup')
            sensitive not player.overtime.locked
            xsize 200
            yminimum 30
            xpos 755
        textbutton player.ration.name:
            action ShowTransient('sc_schedule_picker', x_pos=960, items=player.schedule.available_rations(core.current_world.name),
                setter_func=player.schedule.set_ration)
            hovered Show('sc_text_popup', text=player.ration.description)
            unhovered Hide('sc_text_popup')
            sensitive not player.ration.locked
            xsize 200
            yminimum 30
            xpos 955

        text 'Player money: %s'%player.money:
            yalign 0.90
        if player.decade_bill() > player.money:
            $ txt = '%s({color=#f00}owerdraw{/color})'%player.decade_bill()
        else:
            $ txt = str(player.decade_bill())
        text 'Decade bill: %s'%txt:
            yalign 0.95    
        textbutton 'Leave':
            yalign 1.0
            action Hide('sc_schedule_organaizer')
    on 'hide':
        action [Hide('sc_text_popup'), Hide('sc_job_picker'), Hide('sc_accomodation_picker'),
            Hide('sc_overtime_picker'), Hide('sc_feed_picker')]
screen sc_schedule_picker(x_pos, items, setter_func):
    tag picker
    frame:
        ypos 45
        xpos x_pos
        xsize 200
        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xsize 200
            ysize 350
            vbox:
                for value in items:
                    textbutton value.name:
                        xsize 180
                        action [Function(setter_func, value), Hide('sc_schedule_picker')]
                        hovered Show('sc_text_popup', text=value.description)
                        unhovered Hide('sc_text_popup')
    on 'hide':
        action Hide('sc_text_popup')
