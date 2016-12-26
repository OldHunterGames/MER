screen sc_player_hud:
    vbox:
        textbutton 'info':
            action Show('sc_character_info_screen', person=player)
        textbutton 'equipment':
            action Show('sc_person_equipment', person=player)
        textbutton 'contacts':
            action Show('sc_player_contacts')