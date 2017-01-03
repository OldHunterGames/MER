init python:
    relations_translation = {'fervor': {-1: __("delicate"), 0: __("plain"), 1: __("passionate")},
        'distance': {-1: __("intimate"), 0: __("close"), 1: __("formal")},
        'congruence': {-1: __("contradictor"), 0: __("associate"), 1: __("supporter")}}

    stance_translation = {'master': [__('cruel'), __('opressive'), __('rightful'), __('benevolent')],
            'slave': [__('rebellious'), __('forced'), __('accustomed'), __('willing')],
            'neutral': [__('hostile'), __('distrustful'), __('favorable'), __('friendly')]}
    stance_types_translation = {'master': __('master'),
        'slave': __('slave'),
        'neutral': __('neutral')}
    alignments_translation = {'orderliness': {-1: __("Chaotic"), 0: __("Conformal"), 1: __("Lawful")},
        'activity': {-1: __("Timid"), 0: __("Reasonable"), 1: __("Ardent")},
        'morality': {-1: __("Evil"), 0: __("Selfish"), 1: __("Good")}}

    mood_translation = {-1: '!!!CRUSHED!!!', 0: 'Gloomy', 1: 'Tense',
        2: 'Content', 3: 'Serene', 4: 'Jouful', 5: 'Enthusiastic'}

    attributes_translation = {
        'physique': __('physique'),
        'agility': __('agility'),
        'mind': __('mind'),
        'spirit': __('spirit'),
        'sensitivity': __('sensitivity'),
        'anxiety': __('anxiety'),
        'determination': __('determination'),
        'mood': __('mood'),
        'vitality': __('vitality'),
        'motivation': __('motivation')
    }