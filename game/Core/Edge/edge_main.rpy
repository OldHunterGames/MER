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
    def canibalism_unlocker(person):
        person.allow('feed', 'canibalism')

    def canibalism_locker(person):
        if len(person.get_corpses()) < 1:
            person.disallow('feed', 'canibalism')

label lbl_edge_main:    
    'The Mist gives you a way...'  
    python:
        core.set_world(edge)
        edge.go_to_mist()
        player.set_accommodation('makeshift')
        player.set_job('idle')
        player.set_overtime('rest')
        player.set_feed('forage')
        player.add_corpse.add_callback(canibalism_unlocker)
        player.remove_corpse.add_callback(canibalism_locker)
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
        edge_sovereign.add_member(edge_recruiter)
        
        ## Exploration variatns
        #edge_exploration = ['slaver', 'recruiter', 'bukake', 'dying_grove', 'hazy_marshes', 'echoing_hills', 'repair_job', 'scavenge', 'entertain_job', 'brewery', 'machinery']
        #edge.explorations = edge_exploration
               
    
    slums_leader 'Hi, I am a leader of the Slums'
    $ player.relations(slums_leader)
    slums_champion "I'll watch for you"
    $ player.relations(slums_champion)
    slums_entertainer 'If you need to relax, welcome to my pub.'
    $ player.relations(slums_entertainer)
    slums_medic "I'll patch you if you'l get hurt... for a price!"
    $ player.relations(slums_medic)    

    call edge_init_events
    call lbl_edge_manage
    return
    
label lbl_edge_manage:
    show expression "interface/bg_base.jpg" as bg
    show screen sc_player_hud
    python:
        target = player
        money = player.money
        bill = player.decade_bill
        enrgy_txt = encolor_text('energy', player.energy)
           
    menu:

#        'Нарастить энергию':
#            $ player.gain_energy() 
#        'Test your MIGHT':
#            $ core.skillcheck(player, 'physique', 3)
#        'Divination ([enrgy_txt])' if player.energy >= 0:
#            $ TokensGame(player)      
        'Opportunities':
            if player.energy >= 0:
                call lbl_edge_opportunities 
            else:
                'No energy'
        'Places':
            call lbl_edge_places
        'Faction' if edge.faction_mode:
            $ pass
    
    jump lbl_edge_manage
    return

label lbl_edge_places:
    menu:
        'Marketplace':
            menu:
                'Trader':
                    python:
                        knife = create_item('knife', 'weapon')
                        slums_leader.add_item(knife)
                    call screen sc_trade(slums_leader) 
                'Back':
                    pass
        'House [edge_sovereign.name] outpost':
            call lbl_edge_outpost
        'Hazy marsh' if edge.is_stash_found('hazy_marsh'):
            $ stash = edge.get_stash('hazy_marsh')
            call screen sc_manage_stash(stash)   
        'Echoing hills' if edge.is_stash_found('echoing_hills'):
            $ stash = edge.get_stash('echoing_hills')
            call screen sc_manage_stash(stash) 
        'Dying grove' if edge.is_stash_found('dying_grove'):
            $ stash = edge.get_stash('dying_grove')
            call screen sc_manage_stash(stash)              
        'Done':
            jump lbl_edge_manage
    
    call lbl_edge_places    
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
