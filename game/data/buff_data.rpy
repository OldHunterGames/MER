init python:
    buffs_dict = {
        'overfeed': {
            'name': __('overfeed'),
            'modifiers': {'vitality': 4},
            'slot': 'food'
        },
        'underfeed': {
            'name': __('underfeed'),
            'modifiers': {'vitality': -1},
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
        }
    }