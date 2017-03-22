screen sc_player_hud:
    vbox:
        textbutton 'info':
            action Show('sc_character_info_screen', person=player)
        textbutton 'equipment':
            action Show('sc_person_equipment', person=player)
        textbutton 'contacts':
            action Show('sc_player_contacts')
        textbutton "schedule":
            action Show('sc_schedule', person=player)
        textbutton "tests":
            action Function(renpy.call_in_new_context, 'lbl_tests')
        python:
            quest_text = __('quests')
            if core.quest_tracker.new_quests:
                quest_text += '{color=#f00}!{/color}'
        textbutton quest_text:
            action Show('sc_quests')
        if player.has_slaves():
            textbutton 'Slave':
                action Show('sc_character_info_screen', person=player.get_slaves()[0], communicate=True)
            textbutton 'Release Slave':
                action Function(player.remove_slave, player.get_slaves()[0])
        if core.is_tokens_game_active():
            textbutton 'divination':
                action Function(core.start_tokens_game, player)
        else:
            textbutton 'divination':
                style 'gray_button'
                action NullAction()
        text encolor_text(__('energy'), player.energy)
    if core.can_skip_turn():
        textbutton 'Skip Turn' action Function(core.current_world.new_turn):
            xalign 0.5
            xsize 150
    else:
        textbutton 'Skip Turn':
            xsize 150
            xalign 0.5
            style 'gray_button'
            hovered Show('sc_text_popup', text=__("Not enough money"))
            unhovered Hide('sc_text_popup')
            action NullAction()