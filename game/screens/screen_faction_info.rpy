screen sc_faction_info(faction):
    python:
        if player.know_person(faction.owner):
            relations = player.relations(faction)
        else:
            relations = None
    modal True
    hbox:
        frame:
            ysize 600
            vbox:
                text 'Faction: ' + faction.name
                text ' '
                text 'Leader:'
                if player.know_person(faction.owner):
                    imagebutton:
                        idle im.Scale(faction.owner.avatar_path, 50, 50)
                        action Show('sc_character_info_screen', person=faction.owner, communicate=True)
                        hovered Show('sc_info_popup', person=faction.owner)
                        unhovered Hide('sc_info_popup')
                    text ' ' 
                    text 'faction alignment:'
                    text 'morality: ' + faction.owner.alignment.show_morality()
                    text 'activity: ' + faction.owner.alignment.show_activity()
                    text 'orderliness: ' + faction.owner.alignment.show_orderliness()
                    text ' '
                    text 'Relations: '
                    text 'fervor: ' + relations.show_fervor(True)
                    text 'distance: ' + relations.show_distance(True)
                    text 'congruence: ' + relations.show_congruence(True)
                    text ' '
                    text 'Stance:' + str(relations.colored_stance())
                    # text 'level: ' + str(stance.show_stance())
                    text ' '
                else:
                    image im.Scale(default_avatar_path(), 50, 50)
                
                text ' '
                textbutton 'leave':
                    action Hide('sc_faction_info')
        frame:
            viewport:
                scrollbars 'vertical'
                draggable True
                mousewheel True
                xsize 360
                ysize 500
                hbox:
                    spacing 3
                    xsize 380
                    ysize 500
                    box_wrap True
                    for i in faction.get_members():
                        vbox:
                            python:
                                person = i[0]
                                role = i[1]
                                try:
                                    title = factions_roles[role]
                                except KeyError:
                                    title = role
                            if title is not None:
                                text title
                            spacing 2
                            if player.know_person(person):
                                imagebutton:
                                    idle im.Scale(person.avatar_path, 100, 100)
                                    action Show('sc_character_info_screen', person=person, communicate=True)
                                    hovered Show('sc_info_popup', person=person)
                                    unhovered Hide('sc_info_popup')
                                text person.name[0:8]
                            else:
                                image im.Scale(default_avatar_path(), 100, 100)
                                text 'Unknown'

    on 'hide':
        action Hide('sc_info_popup')