screen sc_player_contacts():
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        frame:
            vbox:
                if player.owned_faction() is not None:
                        textbutton player.owned_faction().name:
                            action Show('sc_faction_info', faction=player.owned_faction())
                if any([player.know_faction(i) for i in core.get_factions_by_type('major_house')]):
                    textbutton 'Major houses':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('major_house'))
                if any([player.know_faction(i) for i in core.get_factions_by_type('guild')]):
                    textbutton 'Guilds':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('guild'))
                if any([player.know_faction(i) for i in core.get_factions_by_type('minor_house')]):
                    textbutton 'Minor houses':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('minor_house'))
                if len(core.get_factions_by_type('unbound')) > 0:
                    textbutton 'Unbound':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('unbound'))
                if len(player.known_characters) > 0:
                    textbutton 'all relations':
                        action Show('sc_relations')
                textbutton 'Leave':
                    action Hide('sc_player_contacts')

screen sc_list_factions(factions):
    frame:
        xalign 0.5
        vbox:
            for i in factions:
                if player.know_person(i.owner):
                    textbutton i.name:
                        action Show('sc_faction_info', faction=i)
