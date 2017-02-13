label lbl_skillcheck_info(result, stats, skill, used, threshold=None, difficulty=0):
    python:
        if result < 0:
            result = 0
        info_show_quality = [encolor_text('провально', 0), 
                            encolor_text('слабенько', 1),
                            encolor_text('удовлетворительно', 2),
                            encolor_text('хорошо', 3),
                            encolor_text('отлично', 4),
                            encolor_text('идеально', 5),
                            encolor_text('Impossible', 6)]
        txt = 'Сложность: %s\n'%(difficulty)
        txt += 'Результат: %s\n'%(info_show_quality[result])
        if threshold is not None:
            txt += 'Требуется: %s\n'%(info_show_quality[threshold])
        txt += 'Лимитирующий фактор: %s(%s) \n'%(encolor_text(skill.name, skill.level), skill.level)
        txt += '+++++++ \n'
        unused = []
        for key in stats.keys():
            if key != 'level':
                if key in used:
                    txt += '%s \n'%(encolor_text(key, stats[key]))
                else:
                    unused.append('%s'%(encolor_text(key, stats[key])))
        txt += '---------- \n'
        for text in unused:
            txt += '%s \n'%(text)
        if stats['motivation'] <= 0:
            txt = 'Проверка провалена из-за низкой мотивации'
    '[txt]'
    return


init python:
    class SlaverQuest(object):
        allure = 4
        
        def __init__(self, performer):
            self.performer = performer

        @property
        def description(self):
            data = quests_data.get('slaver_quest')
            no_desc = 'No description'
            if data is not None:
                return data.get('description', no_desc)
            else:
                return no_desc

        @property
        def name(self):
            data = quests_data.get('slaver_quest')
            name = 'Unnamed'
            if data is not None:
                return data.get('name', name)
            else:
                return name

        def check(self):
            for i in self.performer.slaves:
                if i.allure() >= self.allure:
                    return True
            return False

        def finish(self):
            finished = renpy.call_in_new_context('lbl_slaver_quest_end', self)
            return finished

        def get_available_slaves(self):
            return [i for i in self.performer.slaves if i.allure() >= self.allure]


label lbl_slaver_quest_end(quest):
    $ result = renpy.call_screen('sc_slave_picker', slaver=quest.performer, slaves_list=quest.get_available_slaves())
    if result:
        $ quest.performer.activate_resource_by_name('star')
        menu:
            'Choose reward'
            'Assignations':
                $ pass
            'Nutrition bars':
                $ quest.performer.add_money(10)
            'Protection':
                $ pass
            "Don't take reward":
                $ quest.performer.set_token('contribution')
                return True
        $ quest.performer.set_token('convention')
        return True
    else:
        return False

screen sc_slave_picker(slaver, slaves_list):
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
                for i in slaves_list:
                        vbox:
                            spacing 2
                            
                            imagebutton:
                                idle im.Scale(i.avatar_path, 100, 100)
                                action Function(slaver.remove_slave, i), Return(True)
                                hovered Show('sc_info_popup', person=i)
                                unhovered Hide('sc_info_popup')
                            text i.name[0:8]
    on 'hide':
        action Hide('sc_info_popup')
    textbutton "Leave":
        action Return(False)


