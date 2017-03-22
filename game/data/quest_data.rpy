init python:
        
    quests_data = {
        'edge_main_quest':{'name': __("Get to Eternal Rome"), "reminder":True, 'description': __("The Edge of Mists is extremely inhospitable. Only hope for a better life, or even life at all is lies behind the high walls of Eternal Rome. Figure out a way to get inside.")}, 
        'slaver_quest':{'name': __("Slaver's quest"), 'description': __("Bring a slave")}, 
        
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
