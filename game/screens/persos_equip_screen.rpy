
screen sc_person_equipment(person):
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        vbox:
            text 'Weapon:'
            for i in person.inventory.weapon_slots():
                python:
                    sc_equipment_desc = person.inventory.carried_weapons[i]
                    if sc_equipment_desc != None:
                        sc_equipment_desc = i + ': ' + sc_equipment_desc.name
                    else:
                        sc_equipment_desc = i
                textbutton sc_equipment_desc:
                    action [Show('sc_equip_item', person=person, slot=i),
                            SensitiveIf(person.inventory.is_slot_active(i))]
                    if person.inventory.carried_weapons[i] is not None:
                        alternate Show('sc_item_namer', item=person.inventory.carried_weapons[i])
                        hovered Show('sc_item_description', item=person.inventory.carried_weapons[i])
                        unhovered Hide('sc_item_description')
            text 'Armor:'
            for i in person.inventory.armor_slots():
                python:
                    sc_equipment_desc = person.inventory.carried_armor[i]
                    if sc_equipment_desc != None:
                        sc_equipment_desc = i + ': ' + sc_equipment_desc.name
                    else:
                        sc_equipment_desc = i
                textbutton sc_equipment_desc:
                    action [Show('sc_equip_item', person=person, slot=i),
                            SensitiveIf(person.inventory.is_slot_active(i))]
            text ' '
            textbutton 'leave':
                action Hide('sc_person_equipment'), Hide('sc_equip_item')

        frame:
            xalign 0.5
            yalign 0.5
            xsize 350
            ysize 350
            viewport:
                scrollbars 'vertical'
                draggable True
                mousewheel True
                xsize 350
                ysize 350
                vbox:
                    for i in player.get_unequiped():
                        textbutton i.name action Show('sc_item_options', item=i)

        frame:
            xalign 1.0
            viewport:
                scrollbars 'vertical'
                draggable True
                mousewheel True
                xsize 300
                ysize 500
                hbox:
                    spacing 3
                    xsize 300
                    ysize 500
                    box_wrap True
                    for i in player.corpse_storage:
                        imagebutton:
                            idle im.Grayscale(im.Scale(i.avatar_path, 100, 100))
                            action Show('sc_character_info_screen', person=i)
                            hovered Show('sc_info_popup', person=i)
                            unhovered Hide('sc_info_popup') 

    on 'hide':
        action Hide('sc_item_namer'), Hide('sc_equip_item'), Hide('sc_item_description')


screen sc_item_options(item):
    $ x, y = renpy.get_mouse_pos()
    modal True
    frame:
        pos (x, y)
        xsize 200
        ysize 200
        vbox:
            text item.name
            text 'Price: %s'%(int(item.price*0.7))
            textbutton 'Sell':
                action Function(player.remove_item, item, return_item=False), Function(player.add_money, int(item.price*0.7)), Hide('sc_item_options')
            textbutton 'Leave':
                action Hide('sc_item_options')