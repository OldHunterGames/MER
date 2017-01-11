screen sc_player_hud:
    vbox:
        textbutton 'info':
            action Show('sc_character_info_screen', person=player)
        textbutton 'equipment':
            action Show('sc_person_equipment', person=player)
        textbutton 'contacts':
            action Show('sc_player_contacts')
        textbutton "schedule":
            action Show('sc_schedule_organaizer')
        if player.energy >= 0:
            textbutton encolor_text(__('divination'), player.energy):
                action Function(renpy.call_in_new_context, 'lbl_tokens_game_glue', player)
        else:
            textbutton 'divination':
                style 'gray_button'
                action NullAction()
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

label lbl_tokens_game_glue(person):
    $ TokensGame(person)
    return