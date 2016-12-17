init python:
    sex_actions_data = {
        'anal_fuck':{'name': __("Anal penetration"),
        'pay':{'stamina': 1}, 'attribute': 'agility',  
        'markers':{'target': ['anal_stimulation', ], 'actor': ['straight', 'ass_fetish', ], 'both': []},
        'required':{'actor':{'willing': True, 'stats':{'feelings': ['>=', 1]}, 'anatomy': ['penis'] },
            'target':{'anatomy': ['body']}}},

        'struggle':{'name': __("Struggle"),
        'pay':{'stamina': 1}, 'attribute': 'physique',  
        'markers':{'target': ['forcing'], 'actor': ['active', 'restraint'], 'both': ['roughness',]},
        'required':{'actor':{'stats':{'feelings': ['<', 1]}, 'anatomy': ['graspers']},
            'target':{'willing': True, 'anatomy': ['graspers']}}},

        'endure':{'name': __("Endure violation"),
        'pay':{'drive': 1}, 'attribute': 'spirit',  
        'markers':{'target': ['active'], 'actor': ['passive'], 'both': []},
        'required':{'actor':{'willing': False},
            'target':{'willing': True}}},

        'suffer_pain':{'name': __("Suffer pain"),
        'pay':{'drive': 1}, 'attribute': 'sensitivity',  
        'markers':{'target': ['active', 'sadism', ], 'actor': ['passive', 'masochism', ], 'both': ['roughness']},
        'required':{'actor':{'stats':{'feelings': ['<', 1]}},
            'target':{'willing': True}}}, 

        'suffer_shame':{'name': __("Suffer shame"),
        'pay':{'drive': 1}, 'attribute': 'sensitivity',  
        'markers':{'target': ['abuse', 'passive', 'nothing', ], 'actor': ['humiliation', 'active', 'nothing', ], 'both': ['nothing', 'nothing', 'nothing', ]},
        'required':{'actor':{'willing': True, 'stats':{'feelings': ['>=', 1]}, 'anatomy': ['penis'] },
            'target':{'willing': True,'stats':{'feelings': ['>=', 1]}, 'anatomy': ['body']}}},

        'kiss':{'name': __("Kiss"),
        'pay':{'drive': 1}, 'attribute': 'sensitivity',  
        'markers':{'target': [], 'actor': [], 'both': ['softness', 'orallove']},
        'required':{'actor':{'willing': True},
            'target':{'willing': True}}},

        'cunnilingus':{'name': __("Сunnilingus"),
        'pay':{'drive': 1}, 'attribute': 'sensitivity',  
        'markers':{'target': ['orallove', 'passive', 'straight'], 'actor': ['sucker', 'active'], 'both': ['softness']},
        'required':{'actor':{'willing': True},
            'target':{'anatomy': ['vagina']}}},

        'fellation':{'name': __("Fellation"),
        'pay':{'drive': 1}, 'attribute': 'sensitivity',  
        'markers':{'target': ['orallove', 'passive', 'straight'], 'actor': ['sucker', 'active'], 'both': ['softness']},
        'required':{'actor':{'willing': True},
            'target':{'anatomy': ['penis']}}},

        'rimming':{'name': __("Rimming"),
        'pay':{'drive': 1}, 'attribute': 'sensitivity',  
        'markers':{'target': ['orallove', 'passive', 'ttop'], 'actor': ['sucker', 'active', 'tbottom'], 'both': ['softness']},
        'required':{'actor':{'willing': True},
            'target':{'anatomy': ['body']}}},

        'fuck':{'name': __("Fuck"),
        'pay':{'stamina': 1}, 'attribute': 'agility',  
        'markers':{'target': [], 'actor': [], 'both': ['straight']},
        'required':{'actor':{'willing': True, 'stats':{'feelings': ['>=', 1]}, 'anatomy': ['penis'] },
            'target':{'anatomy': ['vagina']}}},


                
    }
