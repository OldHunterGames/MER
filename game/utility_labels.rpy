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
