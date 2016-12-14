init python:
    sex_actions_data = {
        'anal_penetration':{
            'name': __("Anal penetration"),
            'pay':
                {
                    'stamina': 1
                },
            'markers':{
                'target': [],
                'actor': [],
                'both': []
            },
            'type': 'twoway',
            'required':{
                'actor':{
                    'willing': True,
                    'stats':{
                        'feelings': ['>=', 1]
                    },
                    'anatomy': ['penis']

                },
                'target':{
                    'anatomy': ['anus']
                }
            }
        }
    }