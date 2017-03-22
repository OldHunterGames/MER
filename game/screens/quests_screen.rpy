screen sc_quests:
    window:
        xfill True
        yfill True
        frame:
            vbox:
                for i in core.quest_tracker.active_quests:
                    if i.reminder:
                        textbutton i.name():
                            style 'hoverable_text'
                            action NullAction()
                            hovered Show('sc_text_popup', text=i.description())
                            unhovered Hide('sc_text_popup')
                    if i.completed(player):
                        textbutton encolor_text(i.name(), 'green'):
                            action Function(core.quest_tracker.finish_quest, i, player)
                            hovered Show('sc_text_popup', text=i.description())
                            unhovered Hide('sc_text_popup')
                    else:
                        textbutton encolor_text(i.name(), 'red'):
                            action NullAction()
                            hovered Show('sc_text_popup', text=i.description())
                            unhovered Hide('sc_text_popup')
                textbutton 'Leave':
                    action Hide('sc_quests')
    on 'hide':
        action Hide('sc_text_popup'), Function(core.quest_tracker.check)
