##############################################################################
# The Edge of Mists main
#
# Main script for EOM core module

init -8 python:
    sys.path.append(renpy.loader.transfn("Core/Edge/scrypt"))
    from edge_engine import *
    from edge_camp import *
    edge = EdgeEngine()
    pass

label lbl_edge_main:
    'The Mist gives you a way...'  
    python:
        camp = EdgeCamp()
        edge.locations = []
        trade_loc = EdgeLocation('outpost', True)
        trade_loc.gen_owner(choice(great_houses))
        mist_loc = EdgeLocation('shifting_mist', True)
        edge.locations.append(trade_loc)
        edge.locations.append(mist_loc)
        edge.loc_max = 7
        core.set_world('edge')
        edge.house = choice(house_names.values())
        player.schedule.add_action(camp.accommodation, False)
        player.schedule.add_action('overtime_nap', False)  
        player.schedule.add_action('job_idle', False)  
        player.ration['amount'] = "unlimited"  
        player.ration['food_type'] = "forage" 
        core.resources.add_consumption('player_food', 'provision', player.get_food_consumption, None)
    call edge_init_events
    call lbl_edge_manage
    return
    
label lbl_edge_manage:
    $ consumption_provision = core.resources.consumption('provision')
    $ consumption_fuel = core.resources.consumption('fuel')
    $ consumption_drugs = core.resources.consumption('drugs')
    $ target = player
    
    menu:        
        "Banknotes: [core.resources.money]  \nFood: [core.resources.provision] (-[consumption_provision]) | Fuel: [core.resources.fuel] (-[consumption_fuel]) | Drugs: [core.resources.drugs] (-[consumption_drugs])  \nHardware: [core.resources.hardware] |
     Munition: [core.resources.munition] | 
     "
        'Locations':
            call lbl_edge_locations_menu  
        'Craft':
            call lbl_edge_craft
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
        'Done':
            jump lbl_edge_manage   
    
    jump lbl_edge_schedule
    return

label lbl_edge_locations_menu:
    $ edge.make_locations_menu()
            
    call lbl_edge_locations_menu    
    return

label lbl_edge_shedule_job:
    menu:
        'Idle':
            $ target.schedule.add_action('job_idle', False)  
        'Explore viscinity' if len(edge.locations) < edge.loc_max:
            $ target.schedule.add_action('job_explore', 1)               
        'Look for hidden stashes' if edge.has_location('hazy_marsh') or edge.has_location('echoing_hills') or edge.has_location('dying_grove'):
            jump lbl_edge_locations_menu
        'Scavenge munition' if edge.has_location('grim_battlefield'):
            $ target.schedule.add_action('job_scmunition', 1)  
        'Extract demonblood' if edge.has_location('crimson_pit'):
            $ target.schedule.add_action('job_dbexctraction', 1)  
        'Scavenge tools & scrap' if edge.has_location('junk_yard'):
            $ target.schedule.add_action('job_scjunc', 1)              
        'Disassemble machinery' if edge.has_location('ruined_factory'):
            $ target.schedule.add_action('job_disassemble', 1)     
        'Nevermind':
            $ pass
    
    jump lbl_edge_schedule
    return

label lbl_edge_shedule_overtime:
    menu:
        'Rest':
            $ target.schedule.add_action('overtime_nap', False)          
        'Scout new location' if len(edge.locations) < edge.loc_max:
            $ target.schedule.add_action('overtime_scout', 1)    
        'Found a camp (outworld ruines)' if 'outworld ruines' in edge.locations and not camp.founded:
            $ target.schedule.add_action('overtime_foundcamp', 1)  
        'Nevermind':
            $ pass
    
    jump lbl_edge_schedule
    return

label lbl_edge_craft:
    menu:
        'Camp improvements' if camp.founded:    
            call lbl_edge_craft_camp
        'Basic stuff':
            call lbl_edge_craft_basic
        'Advanced stuff' if 'workbench' not in camp.improvements:
            call lbl_edge_craft_workbench
        'Done':
            jump lbl_edge_manage
            
    jump lbl_edge_craft
    return

label lbl_edge_craft_camp:
    menu:
        'Stove (3 hardware)' if core.resources.hardware >= 3 and 'stove' not in camp.improvements:
            $ core.resources.hardware -= 3
            $ camp.improvements.append('stove')
            'You get a stove. Camp will consume 1 fuel/decade to increase comfort. Corpses can be processed to provision now, for a fuel cost.'
        'Done':
            jump lbl_edge_craft        
    
    jump lbl_edge_craft_camp
    return

label lbl_edge_info_base:
    python:
        job  = edge_denotation[target.job]
        overtime = edge_denotation[target.overtime]        
        focus = encolor_text(target.show_focus(), target.focus)
        consumption = target.get_food_consumption(True)
        recalc_result_target=target
        vitality_info_target = target
        txt = "Mood: " + encolor_text(target.show_mood(), target.mood) + ' {a=lb_recalc_result_glue}[?]{/a}'
        txt += " | Vitality: %s "%(target.vitality) + '{a=lbl_vitality_info}[?]{/a}'
        txt += ' | Ration: %s (%s)'%(consumption[0], consumption[1])
        txt += "\nOccupation: %s | Overtime: %s"% (job, overtime)
        txt += " | Accommodation: %s  \n"%target.accommodation
        txt += "Skill focus: %s\n"%(focus)
        txt += "Atributes: %s\n"%(target.show_attributes())     
        txt += "Features: %s\n"%(target.show_features())
        

    "[txt]"        
    call lbl_edge_manage
    return

label lbl_edge_turn:
    'New turn. Extra resources lost, try to find a safe stash to hold your resources!'
    $ edge.locations_tick()
    $ core.new_turn()
    $ resources.to_zero()
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
