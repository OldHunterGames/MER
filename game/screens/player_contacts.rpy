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
                if any([i.type == 'major_house' for i in player.known_factions()]):
                    textbutton 'Major houses':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('major_house'))
                if any([i.type == 'guild' for i in player.known_factions()]):
                    textbutton 'Guilds':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('guild'))
                if any([i.type == 'minor_house' for i in player.known_factions()]):
                    textbutton 'Minor houses':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('minor_house'))
                if any([i.type == 'unbound' for i in player.known_factions()]):
                    textbutton 'Unbound':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('unbound'), show_others=True)
                textbutton 'Leave':
                    action Hide('sc_player_contacts')

screen sc_list_factions(factions, show_others=False):
    frame:
        xalign 0.5
        vbox:
            for i in factions:
                if player.know_faction(i):
                    textbutton i.name:
                        action Show('sc_faction_info', faction=i)
            if show_others:
                if any([i for i in player.known_characters if not i.has_faction()]):
                    textbutton 'others':
                        action Show('sc_relations')
