init python:
    homeworlds_dict = {
        'prehistoric':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('prehistoric'),
            'descriptions': ['desc1', 'desc2']
        }
    }

    families_dict = {
        'orphan':{
            'name': __('orphan'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        }
    }

    educations_dict = {
        'urchin':{
            'name': __('urchin'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        }
    }

    occupations_dict = {
        'athlete':{
            'name': __('athlete'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills':{
                'athletics': ['training', ('expirience', 2)]
            } 
        }
    }

    cultures_dict = {
        'slavic':{
            'name': __('slavic'),
            'available_skin_colors': ['yellow_skin', 'white_skin', 'dark_skin']
        }
    }