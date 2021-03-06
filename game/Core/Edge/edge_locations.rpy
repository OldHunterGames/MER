# Edge of Mists locations

label lbl_edge_missed_location:
    menu:
        'Explore all (job)' if len(edge.locations) < edge.loc_max:
            $ target.schedule.add_action('job_explore', 1)       
        'Go back':
            $pass
    call lbl_edge_manage
    return

label lbl_edge_utility1(location, title, dif, achive, pay, skill_id):
    menu:
        '[title]'
        'Find out about [location.owner.name]':
            call screen sc_faction_info(location.owner)
        'Work for food (full time)':
            menu:
                'The [location.owner.name] offer to give you some food if you {b}scavenge{/b} armaments for them for a decade. It is [dif] task, but you must achieve [achive] in order to get your reward.'
                'Agree':
                    $ special_values = {'skill': skill_id, 'moral': ['lawful', 'timid'], 'beneficiar': location.owner, 'difficulty': 1}
                    $ special_values['fail_text'] = _('scavenging munition on the grim battlefield for a local gang, but fails to deliver. No food recived.')                    
                    $ special_values['succes_text'] = _('succesfully scavenging munition on the grim battlefield for a local gang. Recived some food')
                    $ target.schedule.add_action('job_foodwork', 1, special_values=special_values)  
                    jump lbl_edge_manage
                'Decline':
                    $ pass
        'Pay a tool for scavenge (full time)':
            menu:
                'You must [pay] to [location.owner.name] in order to scavenge their territory for usible munitions for a decade. All you can find and carry out is yours.'
                'Agree' if edge.resources.can_spend(1):
                    $ edge.resources.spend(1)
                    $ description = _('scavenging munition on the gim battlefield. Yelds ')
                    $ special_values = {'description': description,  'resource_name': 'munition', 'skill': skill_id, 'difficulty' : 1, 'moral': None, 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
                    $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
                    jump lbl_edge_manage
                'Decline':
                    $ pass
        'Ask to join the [location.owner.name] gang' if not core.has_any_faction(player):
            call lbl_edge_gang_signin(location) 
            
        'Get out':
            return 

    call lbl_edge_grim_battlefield(location) 
    return

label lbl_edge_grim_battlefield(location):
    $ dif = encolor_text('straightforward', 1)
    $ achive = encolor_text('adequate results', 2)
    $ pay = encolor_text('pay', 1)
    $ title = ('The tides of Mist brought here an old battlefield full of dead bodies and battered armaments.'
                'Territory is under control of {location.owner.name}.'
                'You can see a few scavergers here and there, they looking for usible munitions.').format(location=location)
    $ skill_id = 'survival'
    call lbl_edge_utility1(location, title, dif, achive, pay, skill_id)
    return

label lbl_edge_crimson_pit(location):
    $ dif = encolor_text('straightforward', 1)
    $ achive = encolor_text('adequate results', 2)
    $ pay = encolor_text('pay', 1)
    $ title = ('Dense smoke and the smell of burned tar guides you to a enormous scorched pit.'
            'You can see a pool of glossy crimson liquid on its bottom, the infamous "Demon Blood", fuel of Eternal Rome.'
            'Place is guarded by {location.owner.name} while tired workers mine the substance.').format(location=location)
    $ skill_id = 'athletics'
    call lbl_edge_utility1(location, title, dif, achive, pay, skill_id)
    return

label lbl_edge_junk_yard(location):
    $ dif = encolor_text('straightforward', 1)
    $ achive = encolor_text('adequate results', 2)
    $ pay = encolor_text('pay', 1)
    $ title = 'Junk yard. Owned by {location.owner.name}.'.format(location=location)
    $ skill_id = 'survival'
    call lbl_edge_utility1(location, title, dif, achive, pay, skill_id)
    return

label lbl_edge_ruined_factory(location):
    $ dif = encolor_text('straightforward', 1)
    $ achive = encolor_text('adequate results', 2)
    $ pay = encolor_text('pay', 1)
    $ title = 'Ruinded factory. Owned by {location.owner.name}.'.format(location=location)
    $ skill_id = 'mechanics'
    call lbl_edge_utility1(location, title, dif, achive, pay, skill_id)
    return

label lbl_edge_dying_grove(location):
    $ special_values = {'place': 'grove', 'quality': location.richness}
    call lbl_edge_unocuppied(location)
    return

label lbl_edge_hazy_marsh(location):
    $ special_values = {'place': 'marsh', 'quality': location.richness}
    call lbl_edge_unocuppied(location)
    return
    
label lbl_edge_echoing_hills(location):
    $ special_values = {'place': 'hills', 'quality': location.richness}
    call lbl_edge_unocuppied(location)    
    return
    
label lbl_edge_unocuppied(location):
    menu:
        'Stash your resorces' if edge.resources.can_spend(1) and not location.has_player_stash:
            # $ location.stash = edge.resources.value
            $ location.make_stash()
            call lbl_edge_unocuppied(location)
            
        "Retrive your stash" if location.has_player_stash:
            $ location.player_stash = False
            $ location.empty_stash()
            call lbl_edge_unocuppied(location)
            
        "Look for someone's stash (job)":
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_manage
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu             
    return
    
label lbl_edge_gang_signin(location):
    python:
        location.owner.add_member(player)
        edge.faction_mode = True
        player.set_supervisor(location.owner.owner)
        target.schedule.add_action('accommodation_mat', single=False) 
        player.supervisor.add_favor_consumption(target, 0, 'accomodation_favor', time=None, description="")
        player.supervisor.add_favor_consumption(target, 0, 'nutrition_favor', time=None, description="")
        
    jump lbl_edge_faction_livein    
    return

