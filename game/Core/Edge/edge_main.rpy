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
        edge.loc_max = 2 + player.agility
        core.set_world('edge')
        house = choice([__('Kamira'), __('Serpis'), __('Corvus'), __('Taurus')])
        player.schedule.add_action('accommodation_makeshift', False)
        player.schedule.add_action('overtime_nap', False)  
        player.schedule.add_action('job_idle', False)  
        player.ration['amount'] = "unlimited"  
        player.ration['food_type'] = "forage" 
        core.resources.add_consumption('player_food', 'provision', player.get_food_consumption, None)
        
    call edge_init_events
    call lbl_edge_manage
    return
    
label lbl_edge_manage:
    $ target = player
    
    menu:        
        'Locations':
            call lbl_edge_locations_menu  
        'Schedule':
            call lbl_edge_schedule
        'Information':
            call lbl_edge_info_base
        'Carry on':
            call lbl_edge_turn
    
    jump lbl_edge_manage
    return

label lbl_edge_schedule:
    $ schedule_major = edge_denotation[target.job]
    $ schedule_minor = edge_denotation[target.overtime]
    
    menu:
        "Occupation: [schedule_major]":
            call lbl_edge_shedule_job
        "Overtime: [schedule_minor]":
            call lbl_edge_shedule_overtime
        "Socialisation: [shedule_socialisation]" if False:
            call lbl_universal_interaction from _call_lbl_universal_interaction
            
        'Назад':
            jump lbl_edge_manage   
    
    jump lbl_edge_schedule
    return

label lbl_edge_locations_menu:
    menu:
        'House [house] Outpost':
            call screen sc_universal_trade
        'Shifting Mist':
            call lbl_edge_noloc
        'Grim battlefield' if 'grim battlefield' in edge.locations:
            call lbl_edge_noloc
        'Crimson pit' if 'crimson pit' in edge.locations:
            call lbl_edge_noloc
        'Junk yard' if 'junk yard' in edge.locations:
            call lbl_edge_noloc
        'Ruined factory' if 'ruined factory' in edge.locations:
            call lbl_edge_noloc
        'Dying grove' if 'dying grove' in edge.locations:
            call lbl_edge_noloc
        'Hazy marsh' if 'hazy marsh' in edge.locations:
            call lbl_edge_noloc
        'Echoing hills' if 'echong hills' in edge.locations:
            call lbl_edge_noloc
        'Outworld ruines' if 'outworld ruines' in edge.locations:
            call lbl_edge_noloc
        'Raiders encampment' if 'raiders encampment' in edge.locations:
            call lbl_edge_noloc
        'House [house] charity mission' if 'charity mission' in edge.locations:
            call lbl_edge_noloc
        'Done':
            call lbl_edge_manage
            
    call lbl_edge_locations_menu    
    return

label lbl_edge_shedule_job:
    menu:
        'Idle':
            $ player.schedule.add_action('job_idle', False)  
        'Explore viscinity' if len(edge.locations) < edge.loc_max:
            $ player.schedule.add_action('job_explore', 1)               
        'Scavenge munition (battlefield)' if 'grim battlefield' in edge.locations:
            $ player.schedule.add_action('job_scmunition', 1)  
        'Extract demonblood (pit)' if 'crimson pit' in edge.locations:
            $ player.schedule.add_action('job_dbexctraction', 1)  
        'Scavenge tools & scrap (junkyard)' if 'junk yard' in edge.locations:
            $ player.schedule.add_action('job_scjunc', 1)              
        'Disassemble machinery (factory)' if 'ruined factory' in edge.locations:
            $ player.schedule.add_action('job_disassemble', 1)     
        'Nevermind':
            $ pass
    
    jump lbl_edge_schedule
    return

label lbl_edge_shedule_overtime:
    menu:
        'Rest':
            $ player.schedule.add_action('overtime_nap', False)          
        'Scout new location' if len(edge.locations) < edge.loc_max:
            $ player.schedule.add_action('overtime_scout', 1)    
        'Nevermind':
            $ pass
    
    jump lbl_edge_schedule
    return

label lbl_edge_info_base:
    python:
        target = player
        job = target.show_job()
        txt = "Работа: [job]"
        txt += "Accommodation: %s  |  %s       \n"%(target.accommodation, job)
        txt += "Fuel: %s, Hardware: %s, Munition: %s \n"%(core.resources.fuel, core.resources.hardware, core.resources.munition)
        consumption = target.get_food_consumption(True)
        txt += 'Ration: %s(%s)'%(consumption[0], consumption[1])
    "[txt]"        
    call lbl_edge_manage
    return

label lbl_edge_turn:
    'New turn'
    $ core.new_turn()
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
