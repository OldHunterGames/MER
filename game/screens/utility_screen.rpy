   
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
            action [ShowTransient('sc_equip_weapon', person=person, hand='main_hand'),
                SensitiveIf(is_main_hand_active(person))]
        textbutton prefight_text2:
            action [ShowTransient('sc_equip_weapon', person=person, hand='other_hand'),
                SensitiveIf(is_other_hand_active(person))]
        textbutton 'Make deck':
            action Show('deck_creator', overlay=True)
        textbutton "Choose deck":
            action [ShowTransient('sc_choose_deck', combatant=combatant)]
        text 'Combat style: ' + combatant.get_combat_style()
        text 'Current deck: '
        textbutton combatant.deck.name:
            action ShowTransient('sc_show_deck', deck=combatant.deck)

        textbutton 'Done' action Hide('sc_enemy_stats'), Return()
    vbox:
        xalign(0.5)
        for enemy in fight.enemies:
            textbutton enemy.name:
                action Hide('sc_enemy_stats'), ShowTransient('sc_enemy_stats', combatant=enemy)

screen sc_enemy_stats(combatant):
    tag prefight
    vbox:
        xalign 0.9
        image im.Scale(combatant.avatar, 200, 200)
        for weapon in combatant.get_weapons():
            text weapon.description
        if combatant.armor is not None:
            text combatant.armor.description
        text combatant.get_combat_style()



screen sc_equip_weapon(person, hand):
    tag prefight
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
        textbutton 'leave' action Hide('sc_equip_weapon')
screen sc_choose_deck(combatant):
    tag prefight
    frame:
        align(0.3, 0.3)
        vbox:
            text 'Available decks'
            for i in combatant.decks:
                if i.is_completed():
                    textbutton i.name:
                        action Function(combatant.set_deck, i), Hide('sc_choose_deck')
            textbutton 'Leave':
                action Hide('sc_choose_deck')

screen sc_show_deck(deck):
    tag prefight
    frame:
        align(0.3, 0.3)
        vbox:
            for i in deck.cards_list:
                $ i = make_card(i)
                textbutton i.name:
                    hovered ShowTransient('sc_card_description', card=i)
                    unhovered Hide('sc_card_description')
                    action NullAction()
            text ""
            textbutton 'leave' action Hide('sc_show_deck')

screen sc_card_description(card):
    frame:
        xmaximum 300
        ymaximum 100
        align(0.5, 0.5)
        if not isinstance(card, DuelAction):
            $ card = make_card(card)
        text card.show()



screen sc_faction_info(faction):
    frame:
        hbox:
            vbox:
                text 'Faction: ' + faction.name
                text ' '
                text 'Leader:'
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

screen sc_gang_info(gang):
    use sc_faction_info(gang)
    frame:
        xalign 0.5
        hbox:
            vbox:
                textbutton "Leader: %s"%gang.owner.name:
                    action Hide('sc_person_info'), ShowTransient('sc_person_info', person=gang.owner, xalign=1.0, yalign=1.0)
                for k, v in gang.roles.items():
                    if v is not None:
                        textbutton "%s: %s"%(k, v.name):
                            action Hide('sc_person_info'), ShowTransient('sc_person_info', person=v, xalign=1.0, yalign=1.0)
                for i in gang.get_common_members():
                    textbutton "member: %s"%i.name:
                        action Hide('sc_person_info'), ShowTransient('sc_person_info', person=i, xalign=1.0, yalign=1.0)

screen sc_person_info(person, xalign=0.0, yalign=0.0):
    frame:
        align(xalign, yalign)
        xmaximum 400
        ymaximum 400
        vbox:
            hbox:
                image im.Scale(person.avatar_path, 200, 200)
                text "Name: %s"%person.name
            vbox:
                hbox:
                    text person.alignment.show_morality()
                    text ' '
                    text person.alignment.show_activity()
                    text ' '
                    text person.alignment.show_orderliness()
                if not person == player:
                    hbox:
                        text person.relations(player).show_fervor()
                        text ' '
                        text person.relations(player).show_distance()
                        text ' '
                        text person.relations(player).show_congruence()
                text "Features: "
                hbox:
                    spacing 5
                    box_wrap True
                    python:
                        features = person.get_visible_features()
                        features_text = ''
                        for i in features:
                            features_text += i.name
                            if i != features[-1]:
                                features_text += ', '
                    text features_text
            textbutton "Leave":
                action Hide('sc_person_info')


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
init python:
    deck_creator_choosed_deck = None
    deck_creator_current_name = ' '
screen deck_creator(overlay=False):
    if overlay:
        image 'interface/bg_base.jpg'
    $ storage = player.decks
    hbox:
        frame:
            xmaximum 300
            vbox:
                for i in storage:
                    textbutton i.description():
                        action SetVariable('deck_creator_choosed_deck', i)
                textbutton 'Create new deck':
                    action Function(storage.append, Deck())
                textbutton 'Leave':
                    action SetVariable('deck_creator_choosed_deck', None), If(overlay, true=Hide('deck_creator'), false=Return())

        if deck_creator_choosed_deck is not None:
            frame:
                vbox:
                    text deck_creator_choosed_deck.name
                    textbutton 'Rename deck':
                        action ShowTransient('sc_deck_namer', deck=deck_creator_choosed_deck)
                    textbutton 'Modify deck':
                        action ShowTransient('sc_deck_modifier', deck=deck_creator_choosed_deck)
                    textbutton 'Combat style: %s'%(str(deck_creator_choosed_deck.combat_style)):
                        action [ShowTransient('sc_deck_style', deck=deck_creator_choosed_deck)]
                    textbutton 'Remove deck':
                        action [Function(storage.remove, deck_creator_choosed_deck), SetVariable('deck_creator_choosed_deck', None),
                                Hide('sc_deck_modifier')]
                    if deck_creator_choosed_deck.is_completed():
                        textbutton 'Finish':
                            action SetVariable('deck_creator_choosed_deck', None), Hide('sc_deck_modifier')
                    else:
                        textbutton 'Leave uncompleted':
                            action SetVariable('deck_creator_choosed_deck', None), Hide('sc_deck_modifier')
screen sc_deck_modifier(deck):
    tag deck_editor
    python:
        card_list = set(player.card_storage.cards)
    frame:
        xalign 0.6
        hbox:
            spacing 10
            vbox:
                box_wrap True
                text 'Current cards'
                for i in set(deck.cards_list):
                    textbutton make_card(i).name + " (%s)"%(deck.count_cards(i)):
                        hovered ShowTransient('sc_card_description', card=i)
                        unhovered Hide('sc_card_description')
                        action Function(deck.remove_card, i)
            vbox:
                box_wrap True
                text 'Available cards'
                for i in card_list:
                    textbutton make_card(i).name + " (%s)"%(player.card_storage.count_for_deck(deck, i)):
                        hovered ShowTransient('sc_card_description', card=i)
                        unhovered Hide('sc_card_description')
                        action Function(deck.add_card, i), SensitiveIf(deck.can_be_added(i, player.card_storage))

screen sc_deck_namer(deck):
    tag deck_editor
    modal True
    frame:
        xmaximum 200
        ymaximum 50
        xalign 0.6
        vbox:
            input value VariableInputValue('deck_creator_current_name')
            textbutton "Apply":
                action [Function(deck.set_name, deck_creator_current_name), Hide('sc_deck_namer')]

screen sc_deck_style(deck):
    tag deck_editor
    frame:
        xalign 0.6
        vbox:
            textbutton 'wrestler':
                action [Function(deck.set_style, 'wrestler'), Hide('sc_deck_style')]
            textbutton 'desperado':
                action [Function(deck.set_style, 'desperado'), Hide('sc_deck_style')]
            textbutton 'rookie':
                action [Function(deck.set_style, 'rookie'), Hide('sc_deck_style')]
            textbutton 'breter':
                action [Function(deck.set_style, 'breter'), Hide('sc_deck_style')]
            textbutton 'juggernaut':
                action [Function(deck.set_style, 'juggernaut'), Hide('sc_deck_style')]
            textbutton 'shieldbearer':
                action [Function(deck.set_style, 'shieldbearer'), Hide('sc_deck_style')]
            textbutton 'beast':
                action [Function(deck.set_style, 'beast'), Hide('sc_deck_style')]


screen sc_character_info_screen(person):
    modal True
    window:
        hbox:
            xalign 0.0
            yalign 0.0
            image im.Scale(person.avatar_path, 150, 150)
            textbutton 'Leave' action Return()
            
        xfill True
        yfill True
        vbox:
            xalign 0.5
            text person.full_name():
                size 25
            text person.age + ' ' + person.gender + ' ' + person.genus.name + ' ' + '(%s)'%person.kink
            text "{0} {1} {2} ({mood})".format(*person.alignment.description(),
                mood=encolor_text(person.show_mood(), person.mood))
            if person != player:
                text (person.stance(player).show_type() + ' ' +
                    '{0} {1} {2}'.format(*person.relations(player).description()))
        hbox:
            spacing 10
            yalign 0.38
            vbox:
                for i in person.visible_features():
                    text i.name
            vbox:
                for i in person.equiped_items():
                    text i.description

screen sc_info_popup(person):
    window:  
        xfill False
        xalign 0.5
        yalign 0.0
        vbox:
            xalign 0.5
            text person.full_name():
                size 25
            text person.age + ' ' + person.gender + ' ' + person.genus.name + ' ' + '(%s)'%person.kink
            text "{0} {1} {2} ({mood})".format(*person.alignment.description(),
                mood=encolor_text(person.show_mood(), person.mood))
            if person != player:
                text (person.stance(player).show_type() + ' ' +
                    '{0} {1} {2}'.format(*person.relations(player).description()))
            for i in person.visible_features():
                text i.name
            for i in person.equiped_items():
                text i.description