style hoverable_text is text:
    color '#fff'
    underline True
    hover_background '#fff'
style char_info_window is window:
    background Color((0, 0, 0, 255))

style gray_button is button:
    idle_background Frame(im.Grayscale('interface/bg_base.jpg'),0,0)
    hover_background Frame(im.Grayscale('interface/bg_base.jpg'),0,0)

screen sc_character_info_screen(person, return_l=False, communicate=False):
    python:
        if player.know_person(person):
            relations = player.relations(person)
        else:
            relations = None
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        hbox:
            frame:
                xsize 1000
                vbox:
                    
                    hbox:
                        if person.has_feature('dead'):
                            image im.Grayscale(im.Scale(person.avatar_path, 150, 150))
                        else:  
                            image im.Scale(person.avatar_path, 150, 150)
                        vbox:
                            if person.has_feature('dead'):
                                textbutton 'Eat':
                                    action Function(player.eat_corpse, person), If(return_l, Return(), false=Hide('sc_character_info_screen'))
                            textbutton 'Leave' action If(return_l, Return(),false=Hide('sc_character_info_screen'))
                    frame:
                        xmaximum 1000
                        text DescriptionMaker(person).description()
                    frame:
                        hbox:
                            vbox:
                                text encolor_text(__('Allure'), person.allure())
                                text encolor_text(__('Hardiness'), person.hardiness())
                                text encolor_text(__('Succulence'), person.succulence())
                                text encolor_text(__('Purity'), person.purity())
                                text encolor_text(__('Exotic'), person.exotic())
                                text encolor_text(__('Style'), person.style())
                                text encolor_text(__('Menace'), person.menace())
                            vbox:
                                $ skills = [None, __("able"), __("veteran"), __("expert")]
                                for i in ['physique', 'mind', 'spirit', 'agility']:
                                    python:
                                        skill = skills[person.skill(i)]
                                        txt = encolor_text(attributes_translation[i], getattr(person, i))
                                        if skill is not None:
                                            txt += '(%s)'%encolor_text(skill, person.skill(i)+2)
                                    text txt


            vbox:       
                if any([person.get_buffs()]) or person.bad_markers or person.good_markers:
                    frame:
                        vbox:
                            for i in person.get_buffs():
                                text encolor_text(i.name, i.color())
                            for i in person.bad_markers:
                                text encolor_text(bad_markers_translation[i], 'red')
                            for i in person.good_markers:
                                text encolor_text(good_markers_translation[i], 'green')
        

                
        frame:
            xsize 200
            ysize 350
            xalign 1.0
            yalign 1.0
            if person.player_controlled:
                imagebutton:  
                    idle im.Scale('images/tarot/card_deck.jpg', 200, 350)
                    action Show('sc_tokens', person=player)
            elif communicate:
                if player.energy > -1:
                    imagebutton:
                        idle im.Scale(person.get_token_image(), 200, 350)
                        hover im.MatrixColor(im.Scale(person.get_token_image(), 200, 350), im.matrix.brightness(0.05))
                        action Function(core.shift_relations, person) 
                else:
                    imagebutton:
                        idle im.Grayscale(im.Scale(person.get_token_image(), 200, 350))
                        hovered Show('sc_text_popup', text=__("Not enough energy"))
                        unhovered Hide('sc_text_popup')
                        action NullAction()

init python:
    active_determination = None

screen sc_tokens(person):
    $ tokens = person.inner_resources
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        hbox:
            box_wrap True
            for i in person.active_resources:
                image im.Scale(i.image, 150, 250)


        textbutton 'Leave' action Hide('sc_tokens'):
            xalign 0.5
            yalign 1.0
            xsize 200
       
screen sc_info_popup(person):
    python:
        if player.know_person(person):
            relations = player.relations(person)
        else:
            relations = None
    window:  
        xfill False
        xalign 0.5
        yalign 0.0
        vbox:
            xalign 0.5
            text person.full_name():
                size 25
            text person.age + ' ' + person.gender + ' ' + person.genus.name + ' ' + '(%s)'%person.kink
            text "{0} {1} {2}".format(*person.alignment.description())
            if person != player and relations is not None:
                text (relations.colored_stance() + 
                    '({0} {1} {2})'.format(*relations.description(True, False)))
            for i in person.visible_features():
                text i.name
            for i in person.equiped_items():
                text i.name()
              
screen sc_weapon_info(weapon):
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            spacing 5
            text weapon.stats()
            if weapon.description() is not None:
                text weapon.description()
            text 'price: ' + str(weapon.price)

screen sc_vitality_info(person):
    $ d, l = person.vitality_info()
    python:
        list_ = list(d.items())
        for i in l:
            list_.append(i)
    frame:
        xalign 0.5
        yalign 0.5
        hbox:
            spacing 10
            vbox:
                text 'Good'
                for k, v in list_:
                    if v > 0:
                        text encolor_text(k, v)
            vbox:
                text 'Bad'
                for k, v in list_:
                    if v < 0:
                        text encolor_text(k, 0)
            vbox:
                text 'Nonfactors'
                for k, v in list_:
                    if v == 0:
                        text encolor_text(k, 6)


screen sc_text_popup(text):
    frame:
        xalign 0.5
        yalign 0.5
        text text
