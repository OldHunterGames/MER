screen sc_player_hud:
    window:
        style 'char_info_window'

        xalign 1.0
        yalign 0.0
        yfill True
        xsize 220
        has vbox
        frame:
            imagebutton:
                idle im.Scale(player.avatar_path, 200, 200)
                action Show('sc_character_info_screen', person=player)
        text player.name
