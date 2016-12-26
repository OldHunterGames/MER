screen sc_player_contacts():
    modal True
    window:
        textbutton 'Leave':
            yalign 1.0
            action Hide('sc_player_contacts')
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        hbox:
            if player.owned_faction() is not None:
                frame:
                    textbutton player.owned_faction().name:
                        action Show('sc_faction_info', faction=player.owned_faction())
            frame:
                vbox:
                    text "Major houses"
                    for i in great_houses:
                        textbutton i.name:
                            action Show('sc_faction_info', faction=i)
            frame:
                vbox:
                    text 'Guilds'
                    for i in guilds:
                            textbutton i.name:
                                action Show('sc_faction_info', faction=i)
            if len(minor_houses) > 0:
                frame:
                    vbox:
                        text 'Minor houses'
                        for i in minor_houses:
                            textbutton i.name:
                                action Show('sc_faction_info', faction=1)
            if len(core.additional_factions) > 0:
                frame:
                    vbox:
                        text 'Unbound'
                        for i in core.additional_factions:
                            textbutton i.name:
                                action Show('sc_faction_info', faction=i)
            if player.known_characters > 0:
                frame:
                    textbutton 'All relations':
                        action Show('sc_relations')