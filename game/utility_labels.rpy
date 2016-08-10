init python:
    class InfoStorage(object):
            def __init__(self, diss_inf, satisfy_inf, determination, anxiety, target):
                self.diss_inf = diss_inf
                self.satisfy_inf = satisfy_inf
                self.determination = determination
                self.anxiety = anxiety
                self.target = target
label mood_recalc_result(diss_inf=None, satisfy_inf=None, determination=None, anxiety=None, recalc=False, target=None):
    python:
        info = None 
        if recalc and target != None:
            for i in recalc_result:
                if i.target == target:
                    recalc_result.remove(i)
                    break
            info = InfoStorage(diss_inf, satisfy_inf, determination, anxiety, target)
            recalc_result.append(info)
    return
label lb_recalc_result_glue():
    call screen sc_mood_recalculation_result(recalc_result_target)
    return
screen sc_mood_recalculation_result(target=None):
    python:
        for i in recalc_result:
            if i.target==target:
                info = i
        threshold = 5-target.sensitivity
    if info == None:
        vbox:
            xalign 0.0
            yalign 0.0
            text 'Для этого персонажа инфы нет'
        hbox:
            xalign 0.5
            yalign 0.5
            textbutton 'Покинуть экран' action Return()
    else:
        python:
            key = 5
            txt = []
            txt_bad = []
            while key > 0:
                for need in info.satisfy_inf[key]:
                    text = encolor_text('%s'%(need.name), key)
                    txt.append(text)
                key -= 1
            for i in info.determination:
                text = encolor_text(i, 1)
                txt.append(text)
            for need in info.diss_inf:
                text = encolor_text('%s(%s)'%(need.name, need.level), 0)
                txt_bad.append(text)
            for i in info.anxiety:
                text = encolor_text(i, 0)
                txt_bad.append(text)
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
        hbox:
            xalign 0.5
            yalign 0.5
            textbutton 'Покинуть экран' action Return()

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
        if threshold != None:
            txt += 'Требуется: %s\n'%(info_show_quality[threshold])
        txt += 'Лимитирующий фактор: %s(%s) \n'%(encolor_text(skill.name, skill.level+1), skill.level+1)
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


label lbl_vitality_info():
    python:
        txt_good = ""
        txt_bad = ""
        zero_factors = ""
        d, l = vitality_info_target.vitality_info()
        items = list(d.items())
        for i in l:
            items.append(i)
        for k, v in items:
            if v > 0:
                txt_good += encolor_text(k, v) + '\n'
            elif v < 0:
                txt_bad += encolor_text(k, 0) + '\n'
            else:
                zero_factors += encolor_text(k, 6) + '\n'
        txt_good += '---------- \n'
        txt_good += txt_bad
        txt_good += '---------- \n'
        txt_good += zero_factors
    '[txt_good]'
    return
