screen sc_player_hud:
    vbox:
        textbutton 'info':
            action Show('sc_character_info_screen', person=player)
        if player.has_slaves():
            textbutton 'Slave':
                action Show('sc_character_info_screen', person=player.get_slaves()[0], communicate=True)
            textbutton 'Release Slave':
                action Function(player.remove_slave, player.get_slaves()[0])
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