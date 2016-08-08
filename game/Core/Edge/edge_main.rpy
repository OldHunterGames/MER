##############################################################################
# The Edge of Mists main
#
# Main script for EOM core module

init -8 python:
    sys.path.append(renpy.loader.transfn("Core/Edge/scrypt"))
    from edge_engine import *
    pass

label lbl_edge_main:
    'The Mist gives you a way...'  
    python:
        edge = EdgeEngine()
        edge.locations = []
        core.set_world('edge')
        house = choice([__('Kamira'), __('Serpis'), __('Corvus'), __('Taurus')])
        player.schedule.add_action('accommodation_makeshift', False)
    
    call lbl_edge_manage
    return
    
label lbl_edge_manage:
    
    menu:        
        'House [house] Outpost':
            call lbl_edge_noloc
        'Shifting Mist':
            call lbl_edge_noloc
        'Information':
            call lbl_edge_info_base
        'Carry on':
            call lbl_edge_turn
    
    jump lbl_edge_manage
    return

label lbl_edge_info_base:
    python:
        target = player
        job = target.show_job()
        txt = "Работа: [job]"
        txt += "Условия сна: %s  |  %s       \n"%(target.accommodation, job)
        txt += "Провизия: %s, Вещества: %s \n"%(core.resource("provision"), core.resource("drugs"))
        consumption = target.get_food_consumption(True)
        txt += 'Жрет: %s(%s)'%(consumption[0], consumption[1])
    "[txt]"        
    call lbl_edge_manage
    return

label lbl_edge_turn:
    'New turn'
    call lbl_edge_manage
    return
    
label lbl_edge_noloc:
    'Carry on, there is noting to see here...'
    
    return
    
    
label lbl_info_new(target):
    python:
        alignment = target.alignment.description() 
        job = target.show_job()
        desu = target.description()
        # taboos = child.show_taboos()
        features = target.show_features()
        tokens = target.tokens
        focus = encolor_text(target.show_focus(), target.focus)
        rel = target.relations(player).description() if target!=player else None
        stance = target.stance(player).level if target!=player else None
        skills = target.show_skills()
        tendency = target.attitude_tendency()
        needs = target.get_needs()
        recalc_result_target = target
        vitality_info_target = target
        txt = "Настроение: " + encolor_text(target.show_mood(), target.mood) + '{a=lb_recalc_result_glue}?{/a}'
        if stance:
            txt += " | Поза: " + str(stance)
        txt += " | Здоровье: %s "%(target.vitality) + '{a=lbl_vitality_info}?{/a}' + '\n'
        txt += "Характер: %s, %s, %s\n"%(target.alignment.description())
        if rel:
            txt += "Отношение: %s, %s, %s\n"%(rel)
            txt += "Гармония: %s, %s\n"%(target.relations(player).harmony()[0], target.relations(player).harmony()[1])
        else:
            txt += "Деньги: %s, Провизия: %s, Вещества: %s \n"%(game.money, game.resource("provision"), game.resource("drugs"))
        txt += "Запреты: %s \n "%(target.restrictions)
        txt += "Условия сна: %s  |  %s       \n"%(target.accommodation, job)
        txt += "Фокус: %s\n"%(focus)
        txt += "Особенности: %s\n"%(features)
        txt += "Аттрибуты: %s\n"%(target.show_attributes())
        if tendency:
            txt += "Тенденция: %s\n"%(tendency)
        if skills:
            txt += "Навыки: %s\n"%(skills)
        if tokens:
            txt += "Токены: %s\n"%(tokens)
        txt += 'Потребности: '
        # for need in needs:
        #    txt += '%s: [%s, %s, %s], '%(need, needs[need].level, needs[need].satisfaction, needs[need].tension)
        # txt += '\n'
        txt += "Ангст: %s, Решимость: %s\n"%(target.anxiety, target.determination)
        consumption = target.get_food_consumption(True)
        txt += 'Жрет: %s(%s)'%(consumption[0], consumption[1])
    "[txt]"

    return
