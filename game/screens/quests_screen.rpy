screen sc_quests:
    window:
        xfill True
        yfill True
        frame:
            vbox:
                for i in core.quest_tracker.active_quests:
                    if i.reminder:
                        python:
                            name = i.name()
                            if core.quest_tracker.is_new(i):
                                name += encolor_text('!', 'red')
                        textbutton name:
                            action NullAction()
                            hovered Show('sc_text_popup', text=i.description())
                            unhovered Hide('sc_text_popup')
                    elif i.completed(player):
                        python:
                            name = encolor_text(i.name(), 'green')
                            if core.quest_tracker.is_new(i):
                                name += encolor_text('!', 'red')
                        textbutton name:
                            action Function(core.quest_tracker.finish_quest, i, player)
                            hovered Show('sc_text_popup', text=i.description())
                            unhovered Hide('sc_text_popup')
                    else:
                        python:
                            name = encolor_text(i.name(), 'red')
                            if core.quest_tracker.is_new(i):
                                name += encolor_text('!', 'red')
                        textbutton name:
                            action NullAction()
                            hovered Show('sc_text_popup', text=i.description())
                            unhovered Hide('sc_text_popup')
                textbutton 'Leave':
                    action Hide('sc_quests')
    on 'hide':
        action Hide('sc_text_popup'), Function(core.quest_tracker.check)
