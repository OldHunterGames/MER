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
        core.set_world(edge)
        edge.go_to_mist()
        player.set_accomodation('bad_sleep')
        player.set_job('idle')
        player.set_overtime('test1')
        spendings_text = __("Decade bill: ")
        def encolor_resource_text(value):
            new_value = edge.resources.calculate_consumption(value)
            return encolor_text(spending_rate[5-new_value], 5-new_value)
        def encolor_favor_text(value, person):
            new_value = person.calculate_favor(value)
            return encolor_text(favor_rate[new_value], 5-new_value)
        def show_consumption_level():
            consumption = edge.resources.can_tick()
            consumption_level = edge.resources.consumption_level()
            consumption_text = spendings_text + encolor_text(spending_rate[5-consumption_level], 5-consumption_level)
            return consumption_text
        
        
        ## Houses & Persons
        edge_sovereign = core.get_faction('serpis')
        
        slums_leader = gen_random_person(genus='human', age=None, gender=None, world=None, culture=None, family=None, education=None, occupation=None)
        slums_faction = edge.add_faction(slums_leader, __('Slums'), 'slums')
        player.relations(slums_faction)
        ocpn = choice(['outcast', 'pathfinder', 'hunter', 'explorer', 'biker', 'sniper', 'marksman', 'watchman', 'sapper',  'mercenary', 'sellsword', 'gladiator', 'thug', 'raider', 'soldier', 'pirate', 'officer', 'knight', 'assasin'])
        slums_champion = gen_random_person(genus='human', occupation=ocpn)
        slums_faction.add_member(slums_champion) 
        slums_faction.set_member_to_role(slums_champion, 'champion') 
        ocpn = choice(['entertainer'], )
        slums_entertainer = gen_random_person(genus='human', occupation=ocpn)
        slums_faction.add_member(slums_entertainer)
        slums_faction.set_member_to_role(slums_entertainer, 'entertainer') 
        ocpn = choice(['medic', ])
        slums_medic = gen_random_person(genus='human', occupation=ocpn)
        slums_faction.add_member(slums_medic)
        slums_faction.set_member_to_role(slums_medic, 'medic') 
        edge_slaver = gen_random_person(genus='human', occupation='merchant')
        slavers = core.get_faction('slavers_guild')
        slavers.add_member(edge_slaver)
        edge_recruiter = gen_random_person(genus='human', occupation='administrator')
        slavers.add_member(edge_recruiter)
        
        ## Exploration variatns
        edge_exploration = ['slaver', 'recruiter', 'bukake', 'dying_grove', 'hazy_marshes', 'echoing_hills', 'repair_job', 'scavenge', 'entertain_job', 'brewery', 'machinery']
        
               
    
    slums_leader 'Hi, I am a leader of the Slums'
    slums_champion "I'll watch for you"
    slums_entertainer 'If you need to relax, welcome to my pub.'
    slums_medic "I'll patch you if you'l get hurt... for a price!"
        

    call edge_init_events
    call lbl_edge_manage
    return
    
label lbl_edge_manage:
    show expression "interface/bg_base.jpg" as bg
    show screen sc_player_hud
    python:
        target = player
        food_info = player.ration_status()
        consumption = edge.resources.can_tick()
        consumption_text = ''
        money = player.money
        bill = player.decade_bill
        enrgy_txt = encolor_text('energy', player.energy)
        if bill == 0:
            bill_txt = ''
        else:
            bill_txt = "Decade bill is %s brs." % (bill) 
            
        if player.job == 'edge_idle': 
            job = encolor_text(player.job, 0)
        else:
            job = encolor_text(player.job, 4)
            
        if not core.can_skip_turn():
            consumption_text += ". You can't skip turn - not enough brs."
    menu:
        "Nutrition: [food_info] \nYou have [money] brs. [bill_txt]"
        "[consumption_text]"
        
        'Take a chance ([enrgy_txt])' if player.energy >= 0:
            $ TokensGame(player)        
        'Тест навыка':
            $ result = core.skillcheck(player, 'athletics', 4) 
        'Opportunities ([enrgy_txt])' if player.energy >= 0:
            call lbl_edge_opportunities     
        'House [edge_sovereign.name] outpost':
            call lbl_edge_outpost
        'Marketplace':
            call lbl_edge_slums_marketplace
        'Dwellings':
            call lbl_edge_slums_accomodation            
        'Eatery':
            call lbl_edge_slums_ration
        'Services':
            call lbl_edge_slums_services
        'Jobs' if not edge.faction_mode:
            call lbl_edge_slums_jobs
        'Stashes' if edge.any_stash_found():
            call lbl_edge_stashes    
        'People':
            pass

        'Faction' if edge.faction_mode:
            $ pass
        #'Locations':
        #    call lbl_edge_locations_menu  
        #'Information':
        #    call lbl_edge_info_base
        #'Equipment':
        #    call screen sc_person_equipment(player)
        #'Deck':
        #    call screen deck_creator
    
    jump lbl_edge_manage
    return

label lbl_edge_slums_marketplace:
    python:
        resources = encolor_text(show_resource[edge.resources.value], edge.resources.value)
        free = encolor_text('free', 5)
        cost_1 = encolor_resource_text(1)
        cost_2 = encolor_resource_text(2)
        cost_3 = encolor_resource_text(3)
        cost_4 = encolor_resource_text(4)
        cost_5 = encolor_resource_text(5) 
    
    menu:
        'Here you can barter some resources for food and equipment. \nYou have [resources].'
        'Buy food' if edge.resources.value > 0:
            menu:
                'Whole roasted girl ([cost_1])':
                    player 'Munch-munch. Toasty!'
                    $ edge.resources.spend(1)  
                    $ player.eat(3,3)
                'Back':
                    $ pass
                
        'Buy weapon' if edge.resources.value > 0:
            menu:
                'knife ([cost_2])' if edge.resources.value >= 2:
                    player "Nice knife!"
                    python:
                        edge.resources.spend(2)
                        player.add_item(create_weapon(id='knife'))
                'Back':
                    pass
                        
                    
        'Buy equipement' if edge.resources.value > 0:
            pass
            
        'Sell weapons':
            call screen edge_sell_screen(player, 'weapon')
                
        'Get out':
            call lbl_edge_manage
    
    call lbl_edge_slums_marketplace
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
        txt += target.food_info()
    "[txt]"

    return

label lbl_all_gangs:
    python:
        menu_list = [(gang.name, gang) for gang in edge.gang_list]
        menu_list.append(('Leave', 'leave'))
        choice = renpy.display_menu(menu_list)
    if choice == 'leave':
        return
    else:
        call screen sc_gang_info(choice)
    call lbl_all_gangs

label lbl_edge_outpost:
    menu:
        'Slaver' if 'slaver' in edge.options:
            call lbl_edge_slavery
        'Recruiter' if 'recruiter' in edge.options:
            call lbl_edge_hiring            
        'Get out':
            call lbl_edge_manage
        
    call lbl_edge_outpost
    return

label lbl_edge_stashes:
    python:
        stashes = edge.active_stashes()
        stashes = [(edge_locations[i], i) for i in stashes]
        stashes.append((__("leave"), 'leave'))
        stash = renpy.display_menu(stashes)
        if not stash == 'leave':
            stash = edge.get_stash(stash)
    if stash == 'leave':
        return
    call screen sc_manage_stash(stash)
    jump lbl_edge_stashes

label lbl_edge_turn:
    $ edge.new_turn()
    if edge.faction_mode:
        call lbl_edge_faction_livein
    if edge.slums_mode:
        call lbl_edge_manage
    else:
        call lbl_edge_manage        
    return





############## ARCHIVE ########################

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
    
label lbl_edge_noloc:
    'Carry on, there is noting to see here...'
    
    return
    

