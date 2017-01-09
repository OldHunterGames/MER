init python:
    skills_data = {
        'athletics': {'name': __('athletics'), 'attribute': 'physique'},
        'combat': {'name': __('combat'), 'attribute': 'agility'},
        'stealth': {'name': __('stealth'), 'attribute': 'agility'},
        'craft': {'name': __('craft'), 'attribute': 'agility'},

        'charisma': {'name': __('charisma'), 'attribute': 'spirit'},
        'concentration': {'name': __('concentration'), 'attribute': 'spirit'},

        'housekeeping': {'name': __('housekeeping'), 'attribute': 'mind'},
        'management': {'name': __('management'), 'attribute': 'mind'},
        'survival': {'name': __('survival'), 'attribute': 'mind'},
        'science': {'name': __('science'), 'attribute': 'mind'},
        'streetwise': {'name': __('streetwise'), 'attribute': 'mind'},
        'engineering': {'name': __('engineering'), 'attribute': 'mind'},


        'sex': {'name': __('sex'), 'attribute': 'sensitivity'},
        'sorcery': {'name': __('sorcery'), 'attribute': 'sensitivity'},
        'expression': {'name': __('expression'), 'attribute': 'sensitivity'}

    }
    
    skillcheck_quality = [encolor_text(__('Fail'), 0), 
                            encolor_text(__('Marginal'), 1),
                            encolor_text(__('Statisfactory'), 2),
                            encolor_text(__('Fine'), 3),
                            encolor_text(__('Great'), 4),
                            encolor_text(__('Awesome'), 5),
                            encolor_text(__('Impossible'), 6)]
