style hoverable_text is text:
    color '#fff'
    underline True
    hover_background '#fff'
style char_info_window is window:
    background Color((0, 0, 0, 255))

screen sc_character_info_screen(person, return_l=False):
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        hbox:
            frame:
                vbox:
                    
                    hbox:  
                        image im.Scale(person.avatar_path, 150, 150)
                        textbutton 'Leave' action If(return_l, Return(),false=Hide('sc_character_info_screen'))
                    hbox:
                        spacing 10
                        vbox:
                            for i in person.visible_features():
                                text i.name
                        vbox:
                            for i in person.equiped_items():
                                textbutton i.name:
                                    text_style 'hoverable_text'
                                    style 'hoverable_text'
                                    action NullAction()
                                    hovered Show('sc_weapon_info', weapon=i)
                                    unhovered Hide('sc_weapon_info')
            hbox:
                xalign 0.32
                frame:
                    
                    vbox:
                        text person.full_name():
                            size 25
                        text person.age + ' ' + person.gender + ' ' + person.genus.name + ' ' + '(%s)'%person.kink
                        hbox:
                            text "{0} {1} {2} ".format(*person.alignment.description())
                            textbutton "({mood})".format(mood=encolor_text(person.show_mood(), person.mood)):
                                style 'hoverable_text'
                                text_style 'hoverable_text'
                                hovered Show('sc_mood_info', person=person)
                                unhovered Hide('sc_mood_info')
                                action NullAction()
                        if person != core.player:
                            text (person.stance(player).show_type() + ' ' +
                                '{0} {1} {2}'.format(*person.relations(player).description()))
                        textbutton 'Vitality: %s'%person.vitality:
                            style 'hoverable_text'
                            text_style 'hoverable_text'
                            hovered Show('sc_vitality_info', person=person)
                            unhovered Hide('sc_vitality_info')
                            action NullAction()
                frame:
                    vbox:
                        text '{b}Skills{/b}'
                        for i in person.get_all_skills():
                            if i != person.focused_skill:
                                textbutton encolor_text(i.name, i.level) + '(%s)'%i.level:
                                    style 'hoverable_text'
                                    text_style 'hoverable_text'
                                    hovered Show('sc_skill_info', skill=i)
                                    unhovered Hide('sc_skill_info')
                                    action NullAction()
                        if person.focused_skill is not None:
                            $ i = person.focused_skill
                            text '{b}Focus:{/b}'
                            textbutton encolor_text(i.name, i.level) + '(%s)'%i.level:
                                style 'hoverable_text'
                                text_style 'hoverable_text'
                                hovered Show('sc_skill_info', skill=i)
                                unhovered Hide('sc_skill_info')
                                action NullAction()

screen sc_skill_info(skill):
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            for i in skill.description:
                text i
        

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
                text i.name

screen sc_mood_info(person):
    python:
        threshold = 5-person.sensitivity
        try:
            info = person.mood_memory
        except AttributeError:
            info = None
    if info is None:
        frame:
            xalign 0.5
            yalign 0.5
            text 'Для этого персонажа инфы нет'
    else:
        python:
            key = 5
            txt = []
            txt_bad = []
            while key > 0:
                for need in info['satisfy_inf'][key]:
                    text = encolor_text('%s'%(need.name), key)
                    txt.append(text)
                key -= 1
            for i in info['determination']:
                text = encolor_text(i, 1)
                txt.append(text)
            for need in info['diss_inf']:
                text = encolor_text('%s(%s)'%(need.name, need.level), 0)
                txt_bad.append(text)
            for i in info['anxiety']:
                text = encolor_text(i, 0)
                txt_bad.append(text)
        frame:
            xalign 0.5
            yalign 0.5
            hbox:
                if len(txt) < 1 and len(txt_bad) < 1:
                    text 'No mood modifiers for this turn'
                else:
                    vbox:
                        xalign 0.0
                        yalign 0.0
                        for i in txt:
                            text [i]

                    vbox:
                        xalign 0.3
                        yalign 0.0
                        for i in txt_bad:
                            text [i]
                    vbox:
                        xalign 0.6
                        yalign 0.0
                        text 'Порог: [threshold]'

screen sc_weapon_info(weapon):
    frame:
        xalign 0.5
        yalign 0.5
        text weapon.description

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

