
screen sc_equip_item(person, slot):
    vbox:
        align(0.0, 0.7)
        text slot + ':'
        for i in person.inventory.available_for_slot(slot):
            textbutton i.name:
                action Function(person.inventory.equip_on_slot, slot, i)
                if i.mutable_name:
                    alternate Show('sc_item_namer', item=i)
                hovered Show('sc_item_description', item=i)
                unhovered Hide('sc_item_description')
        textbutton 'unequip':
            action Function(person.inventory.equip_on_slot, slot, None)

init python:
    item_namer_name = ''
    item_namer_description = False

screen sc_item_namer(item):
    window:
        xalign 0.5
        yalign 0.5
        xmaximum 250
        ymaximum 250
        key 'K_RETURN':
            if item_namer_description:
                action Function(item.set_description, item_namer_name), Hide('sc_item_namer')
            else:
                action Function(item.set_name, item_namer_name), Hide('sc_item_namer')
        
        vbox:
            input value VariableInputValue('item_namer_name'):
                if item_namer_description:
                    length 256
            hbox:
                textbutton 'Description':
                    if not item_namer_description:
                        action SetVariable('item_namer_description', True)
                    else:
                        action SetVariable('item_namer_description', False)
                    selected item_namer_description
            textbutton "Apply":
                if item_namer_description:

                    action [Function(item.set_description, item_namer_name), Hide('sc_item_namer')]
                else:
                    action [Function(item.set_name, item_namer_name), Hide('sc_item_namer')]
    on 'show':
        action SetVariable('item_namer_name', '')
screen sc_item_description(item):
    frame:
        xalign 1.0
        xsize 400
        ysize 300
        vbox:
            text item.name
            text item.stats()
            if item.description is not None:
                text item.description


screen sc_simplefight_equip(person):
    python:
        def is_main_hand_active(person):
                return (any([weapon for weapon in person.inventory.equiped_weapons().values() if not person.inventory.in_hands(weapon)])
                    or person.main_hand is not None)
        def is_other_hand_active(person):
            return (any([weapon for weapon in person.inventory.equiped_weapons().values() if not (person.inventory.in_hands(weapon)
                or weapon.size == 'versatile')]) or person.other_hand is not None)

    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        vbox:
            python:
                if person.main_hand is None:
                    prefight_text1 = "main hand"
                else:
                    prefight_text1 = "main hand: %s"%person.main_hand.name
                if person.other_hand is None:
                    prefight_text2 = 'other hand'
                else:
                    prefight_text2 = 'other hand: %s'%person.other_hand.name
            text 'Prefight equip'
            textbutton prefight_text1:
                action [ShowTransient('sc_equip_weapon', person=person, hand='main_hand'),
                SensitiveIf(is_main_hand_active(person))]
                if person.main_hand is not None:
                    hovered Show('sc_item_description', item=person.main_hand)
                    unhovered Hide('sc_item_description')
            textbutton prefight_text2:
                action [ShowTransient('sc_equip_weapon', person=person, hand='other_hand'),
                SensitiveIf(is_other_hand_active(person))]
                if person.other_hand is not None:
                    hovered Show('sc_item_description', item=person.other_hand)
                    unhovered Hide('sc_item_description')
            textbutton 'leave':
                action Return()


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

        textbutton "prefight_text1":
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
                        textbutton weapon.name:
                            action Function(person.equip_weapon, weapon, hand), Hide('sc_equip_weapon')
                else:
                    textbutton weapon.name:
                        action Function(person.equip_weapon, weapon, hand), Hide('sc_equip_weapon')
        textbutton 'unequip' action Function(person.disarm_weapon, hand), Hide('sc_equip_weapon')

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


screen sc_relations():
    modal True
    textbutton 'leave':
        action Hide('sc_relations')
        xpos 447
        ypos 512
    frame:
        xalign 0.5
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
                for i in player.known_characters:
                    if not i.has_faction():
                        vbox:
                            spacing 2
                            
                            imagebutton:
                                idle im.Scale(i.avatar_path, 100, 100)
                                action Show('sc_character_info_screen', person=i, communicate=True)
                                hovered Show('sc_info_popup', person=i)
                                unhovered Hide('sc_info_popup')
                            text i.name[0:8]
    on 'hide':
        action Hide('sc_info_popup')

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


label lbl_gen_player:
    call screen sc_generate_player
    $ player = core.player
    return 


init python:
    player_generator_garbage = []
    def gen_player(core):
        person = gen_random_person(genus='human')
        person.player_controlled = True
        old = core.player
        core.set_player(person)

        
screen sc_generate_player:
    if core.player is not None:
        use sc_character_info_screen(core.player, True)
    textbutton 'generate':
        xalign 0.6
        yalign 0.6
        action Function(gen_player, core)


label lbl_skillcheck(skillcheck):
    call screen sc_skillcheck(skillcheck)
    return skillcheck


screen sc_skillcheck(skillcheck):
    hbox:
        xalign 0.5
        xmaximum 400
        
        frame:
            xsize 200
            ysize 300
            has vbox
            text 'Resources'
            for i in skillcheck.resources.items():
                textbutton encolor_text(attributes_translation[i[0]], i[1]):
                    if skillcheck.has_cons():
                        action [Function(skillcheck.use_resource, i[0]),
                            SensitiveIf(i[1] >= min(skillcheck.cons_values()))]
                    else:
                        action [Function(skillcheck.use_resource, i[0]),
                            SensitiveIf(i[1] > skillcheck.skill_level)]

        frame:
            xsize 200
            ysize 300
            has vbox
            text 'Cons'
            for i in skillcheck.cons:
                if i[0] == 'anxiety':
                    text encolor_text(attributes_translation['anxiety'], i[1])
                else:
                    text encolor_text(__('difficulty'), i[1])
    frame:
        xsize 400
        xalign 0.5
        ypos 301
        has vbox
        xalign 0.5
        text skillcheck_quality[skillcheck.result]
        textbutton 'End check':
            action Return(), Function(skillcheck.end)
        textbutton 'Sabotage':
            action Function(skillcheck.sabotage), Return()

screen edge_sell_screen(person, item_type):
    
    frame:
        has vbox
        for i in person.get_items(item_type):
            textbutton "%s(%s)"%(i.name, encolor_text(show_resource[i.price], i.price)):
                action Function(person.remove_item, i, return_item=False), Function(edge.resources.income, i.price)
        textbutton 'Leave':
            action Return()
    frame:
        xalign 1.0
        has vbox
        text "Current resources: %s"%(encolor_text(show_resource[edge.resources.value], edge.resources.value))


init python:
    class SkillcheckGame(object):


        def __init__(self, person, attribute, difficulty, text, resource, job=False):
            self.text = text
            self.randomed = None
            self.attribute = attribute
            self.person = person
            self.difficulty = difficulty
            self.job = job
            self.result = 0
            self.resource = resource

        def get_random_resource(self):
            resources_list = self.get_player_cards()
            resource = choice(resources_list)
            if resource == 'tower':
                self.bad_result('tower')
            elif resource == 'fool':
                self.result = 0
                self.text = '{person.name} had to try better'.format(person=self.person)
                self.randomed = im.Scale('images/tarot/arcana_fool.jpg', 300, 450)
            elif resource == 'hangman':
                self.bad_result(resource)
            elif resource == 'devil':
                self.bad_result(resource)
                self.person.add_condition('exhausted')
            elif resource == 'death':
                self.bad_result(resource)
                self.person.add_condition('exhausted')
                person.drop_all_resources()
            else:
                self.randomed = im.Scale(resource.image, 300, 450)
                if resource.nature == 'good':
                    if self.job:
                        success = resource.value > self.difficulty
                    else:
                        success = resource.value >= self.difficulty

                    if success:
                        self.text = encolor_text("Success", 5)
                        if self.job:
                            self.person.increase_productivity()
                        else:
                            self.result = 1
                        if resource in self.person.active_resources:
                            self.person.use_resource(resource)
                    else:
                        self.text = '{person.name} had to try better'.format(person=self.person)
                        self.result = 0
                elif resource.nature == 'bad':
                    self.text = '%s. Something gone terribly wrong!'%encolor_text('Epic fail', 'red')
                    self.result = -1
                    if self.job:
                        self.person.reset_productivity()

        def bad_result(self, name):
            self.result = -1
            self.randomed = im.Scale('images/tarot/arcana_%s.jpg'%name, 300, 450)
            self.text = '%s. Something gone terribly wrong!'%encolor_text('Epic fail', 'red')
            if self.job:
                self.person.reset_productivity()

        def get_player_cards(self):
            person = self.person
            cards = TokensGame.get_defaults(person)
            cards.append('fool')
            cards.append('tower')
            if any([value.tensed for key, value in person.needs.items() if person.need_level(key) == 1]):
                cards.append('hangman')
            if any([value.tensed for key, value in person.needs.items() if person.need_level(key) == 2]):
                cards.append('devil')
            if any([value.tensed for key, value in person.needs.items() if person.need_level(key) == 3]):
                cards.append('death')
            return cards
        def set_result(self, value):
            self.result = value

                


screen sc_skillcheck_mini(skillcheck):
    window:
        text skillcheck.text
    frame:
        xalign 0.5
        yalign 0.3
        hbox:
            spacing 10
            if attr is not None:
                imagebutton:
                    idle im.Scale(skillcheck.resource.image, 300, 450)
                    action [Function(person.use_resource, attr), Return(skillcheck),
                        If(skillcheck.job, Function(person.increase_productivity)),
                        Function(skillcheck.set_result, 1)]
            else:
                image im.Grayscale(im.Scale('images/tarot/card_back.jpg', 300, 450))

            imagebutton:
                idle im.Scale('images/tarot/card_back.jpg', 300, 450)
                action Function(skillcheck.get_random_resource), Return(skillcheck)
            imagebutton:
                idle im.Scale('images/tarot/arcana_fool.jpg', 300, 450)
                action Return(skillcheck)

screen sc_show_card(img, x_align, y_align):
    image img:
        xalign x_align
        yalign y_align


label lbl_skillcheck_mini(person, attribute, difficulty):
    python:
        attr = person.get_resource(attribute, difficulty)
        skill = attributes_translation[attribute]
        attribute_needed = encolor_text(skill, difficulty)
        skill_name_colored = encolor_text(skill, getattr(person, attribute))
        resqual = effort_quality[difficulty]
        text = '{person.name} meets a challenging task. Need {attribute} to succeed'.format(
                person=person, attribute=attribute_needed)
    if difficulty > 0 and difficulty <= 5:
        python:
            check = SkillcheckGame(person, attribute, difficulty, text, attr, False)
            result = renpy.call_screen('sc_skillcheck_mini', check)
        if result.randomed is not None:
            show screen sc_show_card(result.randomed, 0.5, 0.3)
            '[result.text]'
        return result.result

    elif difficulty == 0:
        '[text]'
        return 1
    else:
        '[text]'
        return 0
label lbl_jobcheck(person, attribute):
    python:
        skill = attributes_translation[attribute]
        skill_name_colored = encolor_text(skill, getattr(person, attribute))
        resqual = effort_quality[person.focus()+1]
        job_description = person.job_description()
        focus = person.focus()
        focus_desc = encolor_text(focus_description[focus], focus)
        attr = person.get_resource(attribute, focus, True)
        if person.focus() < 5:
            if not person.productivity_raised:
                text = "{person.name} {job_description} with {focus} effort. {person.name} need {resqual} to rise productivity".format(
                        person=person, job_description=job_description, focus=focus_desc, resqual=resqual)
            elif person.productivity_raised:
                text = "{person.name} {job_description} with {focus} effort. There has been some progress.".format(
                        person=person, job_description=job_description, focus=focus_desc)
        else:
            text = "{person.name} {job_description} with {focus} effort. Perfect!".format(
                person=person, job_description=job_description, focus=focus_desc)
    if person.focus() < 5 and not person.productivity_raised:
        python:
            check = SkillcheckGame(person, attribute, focus, text, attr, True)
            result = renpy.call_screen('sc_skillcheck_mini', check)
        if result.randomed is not None:
            show screen sc_show_card(result.randomed, 0.5, 0.3)
            '[result.text]'
        return
    else:
        '[text]'
        return

label lbl_jobcheck_npc(person, attribute):
    python:
        productivity = person.job_productivity()
        productivity_str = encolor_text(success_rate[productivity], productivity)

        
        skill = attributes_translation[attribute]
        skill_name_colored = encolor_text(skill, getattr(person, attribute))
        resqual = effort_quality[productivity+1]
        job_description = person.job.description()
        energy = person.energy
        motivation = person.motivation()
        motivation_text = encolor_text(__("motivation"), motivation)
        real_productivity = person.real_productivity()
        real_prod_str = success_rate[real_productivity]
        focus = person.focus()
        focus_desc = encolor_text(focus_description[focus], focus)
        attr = person.get_resource(attribute, focus, True)
        if person.focus() < 5:
            if not person.productivity_raised:
                text = "{person.name} {job_description} with {focus} effort leading to {productivity}. {person.name} need {resqual} to rise productivity".format(
                        person=person, job_description=job_description, focus=focus_desc, resqual=resqual,
                        productivity=productivity_str)
            elif person.productivity_raised:
                text = "{person.name} {job_description} with {focus} effort leading to {productivity}. There has been some progress.".format(
                        person=person, productivity=productivity_str, job_description=job_description,
                        focus=focus_desc)
        else:
            text = "{person.name} {job_description} with {focus} effort limited by {motivation} and leading to {productivity} productivity".format(
                person=person, job_description=job_description, productivity=productivity_str,
                focus=focus_desc, motivation=motivation_text)
    '[text]'
    return

        

