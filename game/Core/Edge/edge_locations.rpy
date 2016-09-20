# Edge of Mists locations

label lbl_edge_missed_location:
    menu:
        'Explore all (job)' if len(edge.locations) < edge.loc_max:
            $ target.schedule.add_action('job_explore', 1)       
        'Go back':
            $pass
    call lbl_edge_manage
    return
    
label lbl_edge_outpost(location):
    menu:
        'Bukake-slut for food (full time)':
            $ special_values = {'skill': 'sex', 'beneficiar': player, 'slut_rate': 0,}
            menu:
                'More dicks you suck, more miserable you feel. Who you will feed upon?'
                'Gentle and clean humans':
                    $ special_values['slut_rate'] = 1
                'Clean humans':
                    $ special_values['slut_rate'] = 2
                'Humans':
                    $ special_values['slut_rate'] = 3
                'Humans and beastmans':
                    $ special_values['slut_rate'] = 4
                'All dicks you can find':
                    $ special_values['slut_rate'] = 5                  
                'No one':
                    jump lbl_edge_locations_menu
            $ target.schedule.add_action('job_bukake', special_values=special_values)  
        'Prostitute for money (full time)':
            $ description = ' fucks for a price. Yelds '
            $ special_values = {'description': description, 'resource_name': 'money', 'skill': 'sex', 'difficulty' : 1, 'moral': None, 'tense': ['wellness', 'comfort'], 'statisfy': ['prosperity', 'communication', 'eros'], 'beneficiar': player,}
            $ target.schedule.add_action('job_moneywork',special_values=special_values)         
        'Trade':
            call screen sc_universal_trade
        'Get out':
            return 
                
    call lbl_edge_outpost(location)
    return

label lbl_edge_shifting_mist(location=None):
    'Battle'
    python:
        class Monster(object):
            def __init__(self):
                self.physique = 0
                self.agility = 0
        ally1 = DuelCombatant(player)
        enemy_weapon = Weapon('twohand', 'subdual', quality=1)
        enemy_armor = Armor('heavy_armor', quality=1)
        enemy = gen_random_person('human')
        enemy.main_hand = enemy_weapon
        enemy.armor = enemy_armor
        enemy1 = DuelCombatant(Monster())

        
        fight = DuelEngine([ally1],[enemy1], None)
        fight.start()
    return

label lbl_edge_grim_battlefield(location):
    menu:
        'The tides of Mist brought here an old battlefield full of dead bodies and battered armaments. Territory is under control of [location.owner.name]. You can see a few scavergers here and there, they looking for usible munitions.'
        'Find out about [location.owner.name]':
            call screen sc_faction_info(location.owner)
        'Work for food (full time)':
            menu:
                'The [location.owner.name] offer to give you some food (3 provisions units) if you scavenge armaments for them for a decade.'
                'Agree':
                    $ special_values = {'skill': 'survival', 'beneficiar': location.owner,}
                    $ target.schedule.add_action('job_foodwork', 1, special_values=special_values)  
                    jump lbl_edge_manage
                'Decline':
                    $ pass
        'Pay a tool for scavenge (full time)':
            menu:
                'You must pay 100 banknotes to [location.owner.name] in order to scavenge their territory for usible munitions for a decade. All you can find and carry out is yours.'
                'Agree (100 banknotes)' if core.resources.money >= 100:
                    $ core.resources.money -= 100
                    $ description = ' scavenging munition on the gim battlefield. Yelds '
                    $ special_values = {'description': description, 'resource_name': 'munition', 'skill': 'survival', 'difficulty' : 1, 'moral': None, 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
                    $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
                    jump lbl_edge_manage
                'Decline':
                    $ pass
        'Ask to join the [location.owner.name] gang' if not core.has_any_faction(player):
            $ location.owner.add_member(player)
            jump lbl_edge_faction_livein
        'Get out':
            return 

    call lbl_edge_grim_battlefield(location) 
    return

label lbl_edge_squatted_slums(location):
    menu:
        'Slums squatted by [location.owner.name] gang are open to live in... for a price.'
        'Sign in':
            call lbl_edge_slums_livein
        'Get out':
            return         
    
    call lbl_edge_squatted_slums(location)
    return

label lbl_edge_dying_grove(location):
    $ special_values = {'place': 'grove', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu             
    return

label lbl_edge_hazy_marsh(location):
    $ special_values = {'place': 'marsh', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu        
    return
    
label lbl_edge_echoing_hills(location):
    $ special_values = {'place': 'hills', 'quality': location.cache}
    menu:
        'Look for hidden stash (job)':
            $ target.schedule.add_action('job_lookforstash', 1, special_values=special_values)  
            jump lbl_edge_schedule
        'Go back':
            $ pass            
        
    jump lbl_edge_locations_menu        
    return
