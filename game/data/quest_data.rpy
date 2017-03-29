init python:
        
    quests_data = {
        'edge_main_quest':{'name': __("Get to Eternal Rome"), "reminder":True, 'description': __("The Edge of Mists is extremely inhospitable. Only hope for a better life, or even life at all is lies behind the high walls of Eternal Rome. Figure out a way to get inside.")}, 
        'slaver_quest':{'name': __("Slaver's quest"), 'description': __("Bring a slave to a guild slaver.")}, 
        'edge_slave_quest':{'name': __("Rome: slave path"), 'description': __("The simplest way to get into Eternal Rome is to sell yourself into slavery. Your new master will take you there.")}, 
        'edge_bond_quest':{'name': __("Rome: bond path"), 'description': __("Major Houses hire valuable employees on terms slightly better than slavish. It's not a bad way to get into Eternal Rome and get a stable job, but you need to prove yourself  worthy to the recruiter of the Major House.")}, 
        'edge_citisen_quest':{'name': __("Rome: citisen path"), 'description': __("Only a select few begin their lives in Eternal Rome as full-fledged citizens. To receive this honorary status, it is necessary to show the recruiter of the Major House that by acting independently you will bring more benefit than doing bonded labor.")}, 


    }
    basic_quests = {
        'relations': {
            'delicate': {'name': __("Delicate"), 'description': __("bring5bars"), 'end_label': 'lbl_relations_quest_end', 'axis': 'fervor'},
            'passionate': {'name': __("Passionate"), 'description': __("bring5bars"), 'end_label': 'lbl_relations_quest_end', 'axis': 'fervor'},
            'formal': {'name': __("Formal"), 'description': __("bring5bars"), 'end_label': 'lbl_relations_quest_end', 'axis': 'distance'},
            'intimate': {'name': __("Intimate"), 'description': __("bring5bars"), 'end_label': 'lbl_relations_quest_end', 'axis': 'distance'},
            'admirer': {'name': __("Admirer"), 'description': __("bring5bars"), 'end_label': 'lbl_relations_quest_end', 'axis': 'congruence'},
            'hater': {'name': __("Hater"), 'description': __("bring5bars"), 'end_label': 'lbl_relations_quest_end', 'axis': 'congruence'},                        
        }
    }
