##############################################################################
# The Edge of Mists faction
#
# Factions menu

    
label lbl_edge_faction_livein:
    $ faction = player.factions[0]
    $ master = player.supervisor
    $ favor = encolor_text(show_favor[master.favor], master.favor)
    $ free = encolor_text('free', 5)
    $ f_1 = encolor_favor_text(1, master)
    $ f_2 = encolor_favor_text(2, master)
    $ f_3 = encolor_favor_text(3, master)
    $ f_4 = encolor_favor_text(4, master)
    $ f_5 = encolor_favor_text(5, master)   
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
            call screen sc_gang_info(faction)
        'Information':
            call lbl_edge_info_base           
        'Carry on' if core.can_skip_turn():
            call lbl_edge_turn
   
    jump lbl_edge_faction_livein
    return
    
label lbl_edge_faction_occupation:
    $ sk_cmb = target.skill('combat').show()
    $ sk_sex = target.skill('sex').show()
    $ sk_ath = target.skill('athletics').show()
    $ sk_hk = target.skill('housekeeping').show()
    $ sk_alc = target.skill('alchemy').show()
    $ sk_mng = target.skill('management').show()
    $ sk_crf = target.skill('craft').show()
    $ master.remove_favor_consumption('rest_favor')
    
    menu:
        'Rest ([f_1] favor cost)':
            $ target.schedule.add_action('job_idle')  
            $ master.add_favor_consumption(target, False, 'rest_favor', time=None, description="")
        
        'Servitor (no skill)':
            $ target.schedule.add_action('job_servitor', False)  
            
        'Guard ([sk_cmb])':
            'not yet'
            call lbl_edge_faction_occupation
                                    
        'Concubine ([sk_sex])':
            $ pass
            
        'Builder ([sk_ath])':
            $ title = __('Some manual labor (athletics).')
            $ skill_id = 'athletics'
            $ description = _('doing manual labor for the gang. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['approval'], 'beneficiar': master,}
            $ target.schedule.add_action('job_clanwork', False, special_values=special_values)  
            
        'Scullion ([sk_hk])':
            $ title = __('Some labor (housekeeping).')
            $ skill_id = 'housekeeping'
            $ description = _('providing household services for the gang. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['approval'], 'beneficiar': master,}
            $ target.schedule.add_action('job_clanwork', False, special_values=special_values)  
        
        'Nurse ([sk_alc])':
            $ title = __('Some labor (alchemy).')
            $ skill_id = 'alchemy'
            $ description = _('doing medical services for the gang. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['approval'], 'beneficiar': master,}
            $ target.schedule.add_action('job_clanwork', False, special_values=special_values)  
        
        'Overseer ([sk_mng])':
            $ title = __('Some labor (management).')
            $ skill_id = 'management'
            $ description = _('doing management services for the gang. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['approval'], 'beneficiar': master,}
            $ target.schedule.add_action('job_clanwork', False, special_values=special_values)  
        
        'Handyman ([sk_crf])':
            $ title = __('Some labor (craft).')
            $ skill_id = 'craft'
            $ description = _('doing craft services for the gang. Yelds ')
            $ special_values = {'description': description,  'skill': skill_id, 'difficulty' : 2, 'moral': ['lawful', 'timid'], 'tense': ['amusement', 'comfort'], 'statisfy': ['approval'], 'beneficiar': master,}
            $ target.schedule.add_action('job_clanwork', False, special_values=special_values)  
            
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



