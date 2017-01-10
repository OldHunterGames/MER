init python:
    buffs_dict = {
        'overfeed': {
            'name': __('overfeed'),
            'modifiers': {'energy': 4},
            'slot': 'food'
        },
        'underfeed': {
            'name': __('underfeed'),
            'modifiers': {'energy': -1},
            'slot': 'food'
        },
        'bad_sleep': {
            'name': __('bad sleep'),
            'modifiers': {'vitality': -1},
            'slot': 'sleep'
        },
        'beauty_sleep': {
            'name': __('beauty sleep'),
            'modifiers': {'vitality': 2},
            'slot': 'sleep'
        },
        'wound': {
            'name': __('wound'),
            'modifiers': {'vitality': -1, 'wellness': -1},
        },
        'exhausted':{
            'name': __("exhausted"),
            'modifiers': {'energy': -1}
        },
        'rested':{
            'name': __('rested'),
            'modifiers': {'energy': 1}
        },
        'pain':{
            'name': __("pain"),
            'modifiers': {'energy': -1}
        },
        'drugs':{
            'name': __("drugs"),
            'modifiers': {'energy': 1}
        },
        'discomfort':{
            'name': __('discomfort'),
            'modifiers': {'energy': -1}
        },
        'bliss':{
            'name': __('bliss'),
            'modifiers': {'energy': 1}
        },
        'deprivation':{
            'name': __("deprivation"),
            'modifiers': {'energy': -1}
        },
        'adrenaline':{
            'name': __('adrenaline'),
            'modifiers': {'energy': 1}
        },
        'lust':{
            'name': __('lust'),
            'modifiers': {'energy': -1}
        },
        'orgasm':{
            'name': __('orgasm'),
            'modifiers': {'energy': 1}
        },
        'epic_luck':{
            'name': __('epic luck'),
            'modifiers': {'mood': 1}
        }
    }