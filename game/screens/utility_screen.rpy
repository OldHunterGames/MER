   
screen sc_person_equipment(person):
    vbox:
        text 'Weapon:'
        for i in person.inventory.weapon_slots():
            python:
                sc_equipment_desc = person.inventory.carried_weapons[i]
                if sc_equipment_desc != None:
                    sc_equipment_desc = i + ': ' + sc_equipment_desc.description
                else:
                    sc_equipment_desc = i
            textbutton sc_equipment_desc:
                action [Show('sc_equip_item', person=person, slot=i),
                        SensitiveIf(person.inventory.is_slot_active(i))]
        text 'Armor:'
        for i in person.inventory.armor_slots():
            python:
                sc_equipment_desc = person.inventory.carried_armor[i]
                if sc_equipment_desc != None:
                    sc_equipment_desc = i + ': ' + sc_equipment_desc.description
                else:
                    sc_equipment_desc = i
            textbutton sc_equipment_desc:
                action [Show('sc_equip_item', person=person, slot=i),
                        SensitiveIf(person.inventory.is_slot_active(i))]
        text ' '
        textbutton 'leave':
            action Hide('sc_person_equipment'), Hide('sc_equip_item'), Return()

screen sc_equip_item(person, slot):
    vbox:
        align(0.0, 0.7)
        text slot + ':'
        for i in person.inventory.available_for_slot(slot):
            textbutton i.description:
                action Function(person.inventory.equip_on_slot, slot, i)
        textbutton 'unequip':
            action Function(person.inventory.equip_on_slot, slot, None)
        textbutton 'leave':
            action Hide('sc_equip_item')

screen sc_prefight_equip(combatant, fight):
    vbox:
        python:
            person = combatant.person
            def is_main_hand_active(person):
                return (any([weapon for weapon in person.inventory.equiped_weapons().values() if not person.inventory.in_hands(weapon)])
                    or person.main_hand is not None)
            def is_other_hand_active(person):
                return (any([weapon for weapon in person.inventory.equiped_weapons().values() if not (person.inventory.in_hands(weapon)
                    or weapon.size == 'versatile')]) or person.other_hand is not None)
            if person.main_hand is None:
                prefight_text1 = "main hand"
            else:
                prefight_text1 = "main hand: %s"%person.main_hand.description
            if person.other_hand is None:
                prefight_text2 = 'other hand'
            else:
                prefight_text2 = 'other hand: %s'%person.other_hand.description
        textbutton prefight_text1:
            action [Show('sc_equip_weapon', person=person, hand='main_hand'),
                SensitiveIf(is_main_hand_active(person))]
        textbutton prefight_text2:
            action [Show('sc_equip_weapon', person=person, hand='other_hand'),
                SensitiveIf(is_other_hand_active(person))]
        text 'Combat style: ' + combatant.get_combat_style()
        textbutton 'Done' action Hide('sc_enemy_stats'), Return()
    vbox:
        xalign(0.5)
        for enemy in fight.enemies:
            textbutton enemy.name:
                action Hide('sc_enemy_stats'), Show('sc_enemy_stats', combatant=enemy)

screen sc_enemy_stats(combatant):
    vbox:
        xalign 0.9
        image im.Scale(combatant.avatar, 200, 200)
        for weapon in combatant.get_weapons():
            text weapon.description
        if combatant.armor is not None:
            text combatant.armor.description
        text combatant.get_combat_style()



screen sc_equip_weapon(person, hand):
    vbox:
        align(0.3, 0.3)
        for weapon in person.inventory.equiped_weapons().values():
            if weapon is not None and not person.inventory.in_hands(weapon):
                if hand == 'other_hand':
                    if weapon.size != 'versatile':
                        textbutton weapon.description:
                            action Function(person.equip_weapon, weapon, hand), Hide('sc_equip_weapon')
                else:
                    textbutton weapon.description:
                        action Function(person.equip_weapon, weapon, hand), Hide('sc_equip_weapon')
        textbutton 'unequip' action Function(person.disarm_weapon, hand), Hide('sc_equip_weapon')

screen sc_make_deck(person):
        vbox:
            xalign 0.0
            text 'current deck:'
            for card in person.deck.cards_list:
                textbutton card.name:
                    hovered Show('sc_card_description', card=card)
                    unhovered Hide('sc_card_description')
                    action Function(person.deck.remove_card, card)
        vbox:
            xalign 0.3
            text 'available:'
            for card in person.cards_list:
                if card not in person.deck.cards_list:
                    textbutton card.name:
                        hovered Show('sc_card_description', card=card)
                        unhovered Hide('sc_card_description')
                        action Function(person.deck.add_card, card)
        textbutton 'done':
            xalign 0.6
            action Return()



screen sc_card_description(card):
    text card.show():
        align(0.5, 0.5)


screen sc_faction_info(faction):
    frame:
        hbox:
            vbox:
                text 'Faction: ' + faction.name
                text ' '
                text 'Leaded:'
                text faction.owner.name
                text ' ' 
                text 'faction alignment:'
                text 'morality: ' + faction.owner.alignment.show_morality()
                text 'activity: ' + faction.owner.alignment.show_activity()
                text 'orderliness: ' + faction.owner.alignment.show_orderliness()
                text ' '
                text 'Relations: '
                text 'fervor: ' + player.relations(faction).show_fervor()
                text 'distance: ' + player.relations(faction).show_distance()
                text 'congruence: ' + player.relations(faction).show_congruence()
                text ' '
                text 'Stance:'
                text 'type: ' + str(player.stance(faction).show_type())
                text 'level: ' + str(player.stance(faction).show_stance())
                text ' '
                text 'Harmony: ' + str(player.relations(faction).harmony()[0])
                $ axis = player.relations(faction).show_harmony_axis()
                if len(axis[0]) > 0:
                    text 'harmonized_axis: ' + str(axis[0])
                if len(axis[1]) > 0:
                    text 'bad harmony: ' + str(axis[1])
                text ' '
                textbutton 'leave':
                    action Return()

screen sc_item_creator(creator_item_properties):
    python:
        munition_needed = 0
        def is_ready(item_properties):
            return all([value for value in item_properties.values()])
        def change_item_type(dict_, type_):
            if dict_['type'] != type_:
                for key in dict_.keys():
                    del dict_[key]
            dict_['type'] = type_
            if type_ == 'armor':
                dict_['armor_rate'] = None
            elif type_ == 'weapon':
                dict_['size'] = None
                dict_['damage_type'] = None
    vbox:
        xalign 0.0
        text 'choose type:'
        textbutton 'weapon' action [Function(change_item_type, creator_item_properties, 'weapon'),
            Show('sc_weapon_properties', item_properties=creator_item_properties),
            Hide('sc_armor_properties')]
        textbutton 'armor' action [Function(change_item_type, creator_item_properties, 'armor'),
            Show('sc_armor_properties', item_properties=creator_item_properties),
            Hide('sc_weapon_properties')]
        text ''
        textbutton 'Done' action [SensitiveIf(is_ready(creator_item_properties)),
            Hide('sc_weapon_properties'),
            Hide('sc_armor_properties'),
            Return('make')]

screen sc_weapon_properties(item_properties):
    hbox:
        yalign 0.5
        vbox:
            text 'size:'
            for key, value in item_features.items():
                if value['slot'] == 'wpn_size':
                    if key == 'shield':
                        textbutton value['name'] action SetDict(item_properties, 'size', key), SetDict(item_properties, 'damage_type', key)
                    else:
                        textbutton value['name'] action SetDict(item_properties, 'size', key), SetDict(item_properties, 'damage_type', None)
        vbox:
            text 'damage_type:'
            for key, value in item_features.items():
                if value['slot'] == 'wpn_dmg':
                    textbutton value['name'] action [SetDict(item_properties, 'damage_type', key),
                        SensitiveIf(item_properties.get('size') != 'shield')]

screen sc_armor_properties(item_properties):
    hbox:
        yalign 0.5
        vbox:
            text 'armor rate:'
            for key, value in item_features.items():
                if value['slot'] == 'armor_rate':
                    textbutton value['name'] action SetDict(item_properties, 'armor_rate', key)
