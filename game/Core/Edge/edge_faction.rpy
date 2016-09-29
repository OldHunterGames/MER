##############################################################################
# The Edge of Mists faction
#
# Factions menu

    
label lbl_edge_faction_livein:
    $ faction = player.factions[0]
    $ master = player.supervisor
    $ favor = encolor_text(show_favor[master.favor], master.favor)
    $ free = encolor_text('free', 5)
    $ f_1 = encolor_resource_text(1)
    $ f_2 = encolor_resource_text(2)
    $ f_3 = encolor_resource_text(3)
    $ f_4 = encolor_resource_text(4)
    $ f_5 = encolor_resource_text(5)    
    $ consumption_level = master.get_favor_consumption()
    $ show_consumption = encolor_text(favor_rate[consumption_level], 5-consumption_level) 
    if core.can_skip_turn():
        $ addtext = ''
    else:
        $ addtext = 'Reduce your demands or get more favor with faction leader to be able to move on.'
       
    menu:        
        "You have [favor] with a faction leader. Your demands are [show_consumption]. [addtext]"
        'Occupation':
            call lbl_edge_faction_occupation  
        'Accomodation':
            call lbl_edge_faction_accomodation            
        'Ration':
            call lbl_edge_faction_ration
        'Services':
            call lbl
        'Earnings share':
            call lbl_edge_faction_share
        'Equipement':
           call lbl   
        'Clanmates':
            call screen sc_faction_info(master)
        'Information':
            call lbl_edge_info_base           
        'Carry on' if core.can_skip_turn():
            call lbl_edge_turn
   
    jump lbl_edge_faction_livein
    return
    
label lbl_edge_faction_occupation:
    $ sk_cmb = target.skill('combat').show()
    $ sk_sex = target.skill('sex').show()
    $ sk_ath = target.skill('survival').show()
    $ sk_hk = target.skill('housekeeping').show()
    $ sk_alc = target.skill('alchemy').show()
    $ sk_mng = target.skill('management').show()
    $ sk_crf = target.skill('craft').show()
    
    menu:
        'Rest ([f_1] favor cost)':
            $ target.schedule.add_action('job_idle')  
            $ master.add_favor_consumption(target, 1, 'accomodation_favor', time=None, description="")
        
        'Servitor (no skill)':
            $ target.schedule.add_action('job_servitor')  
            
        'Guard ([sk_cmb])':
            $ pass
                                    
        'Concubine ([sk_sex])':
            $ title = __('Some labor (sex).')
            $ skill_id = 'survival'
            $ description = _('doing sexual services at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
            
        'Builder ([sk_ath])':
            $ title = __('Some manual labor (athletics).')
            $ skill_id = 'survival'
            $ description = _('doing manual labor at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
            
        'Scullion ([sk_hk])':
            $ title = __('Some labor (housekeeping).')
            $ skill_id = 'survival'
            $ description = _('providing household services at the slums. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['prosperity'], 'beneficiar': player,}
            $ target.schedule.add_action('job_simplework', 1, special_values=special_values)  
        
        'Nurse ([sk_alc])':
            $ pass
        
        'Overseer ([sk_mng])':
            $ pass
        
        'Handyman ([sk_crf])':
            $ pass
            
    call lbl_edge_faction_livein  
    return 
    
label lbl_edge_faction_accomodation:

    menu:
        'Tiny mat in common room ([free])':
            $ target.schedule.add_action('accommodation_mat', single=False) 
            $ cost = 0
        'Cot & bkanket ([f_1])':
            $ target.schedule.add_action('accommodation_cot', single=False) 
            $ cost = 1
        'Apartments ([f_2])':
            $ target.schedule.add_action('accommodation_appartment', single=False) 
            $ cost = 3            
            
    $ master.add_favor_consumption(target, cost, 'accomodation_favor', time=None, description="")
    # call lbl_edge_faction_livein
    return
    
label lbl_edge_faction_ration:
    menu:
        'Junkfood lunch ([f_1])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'ammount': 1, 'taste': 0}) 
            $ cost = 1           
        'Junkfood 3 time meals ([f_2])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'ammount': 2, 'taste': 0}) 
            $ cost = 2           
        'Cooked lunch ([f_2])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'ammount': 1, 'taste': 2}) 
            $ cost = 2   
        'All junkfood you can eat ([f_3])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'ammount': 3, 'taste': 0}) 
            $ cost = 3           
        'Cooked 3 time meals ([f_3])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'ammount': 2, 'taste': 2}) 
            $ cost = 3   
        'Whole roasted girl ([f_4])':
            $ target.schedule.add_action('feed_catering', single=False, special_values={'ammount': 3, 'taste': 3}) 
            $ cost = 4               
        'Who does not work shall not eat ([free])':
            $ cost = 0
            $ target.schedule.remove_action('feed_catering')
            
    $ master.add_favor_consumption(target, cost, 'nutrition_favor', time=None, description="")
    # call lbl_edge_faction_livein
    return
    
label lbl_edge_faction_share:

    menu:
        'No share ([free])':
            $ target.schedule.add_action('income_share', single=False) 
            $ income = 0
            
    $ master.add_favor_consumption(target, income, 'share_favor', time=None, description="")    
    return



