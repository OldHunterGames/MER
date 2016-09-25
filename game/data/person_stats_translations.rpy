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
    alignments_translation = {'orderliness': {-1: __("chaotic"), 0: __("conformal"), 1: __("lawful")},
        'activity': {-1: __("timid"), 0: __("reasonable"), 1: __("ardent")},
        'morality': {-1: __("evil"), 0: __("selfish"), 1: __("good")}}

    food_quality_dict = {-1: __("disgusting "),
                         0: __('forage '),
                         1: __('adequate '),
                         2: __('gustable '),
                         3: __('tasty '),
                         4: __('delicious '),
    }

    food_amount_dict = {0: __('starving'),
                        1: __('underfeed'),
                        2: __(''),
                        3: __('overfeed')
    }