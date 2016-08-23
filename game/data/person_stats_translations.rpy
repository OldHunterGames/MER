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