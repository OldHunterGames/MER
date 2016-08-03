# -*- coding: UTF-8 -*-
person_features = {
    # base
    'junior': {'slot': 'age', 'modifiers': {'physique': -1, 'spirit': -1, 'mind': -1, 'sensitivity': +1}, 'visible': True},
    'adolescent': {'slot': 'age', 'modifiers': {}, 'visible': True},
    'mature': {'slot': 'age', 'modifiers': {'spirit': +1}, 'visible': True},
    'elder': {'slot': 'age', 'modifiers': {'agility': -1, 'mind': +1}, 'visible': True},

    'sexless': {'slot': 'gender', 'modifiers': {}, 'visible': True},
    'male': {'slot': 'gender', 'modifiers': {'physique': +1, 'sensitivity': -1}, 'visible': True},
    'female': {'slot': 'gender', 'modifiers': {'physique': -1, 'sensitivity': +1}, 'visible': True},
    'shemale': {'slot': 'gender', 'modifiers': {}, 'visible': True},

    'brawny': {'slot': 'constitution', 'modifiers': {'agility': -1, 'physique': +1}, 'visible': True},
    'large': {'slot': 'constitution', 'modifiers': {'physique': +1}, 'visible': True},
    'athletic': {'slot': 'constitution', 'modifiers': {'agility': +1, 'physique': +1}, 'visible': True},
    'small': {'slot': 'constitution', 'modifiers': {'physique': -1}, 'visible': True},
    'lean': {'slot': 'constitution', 'modifiers': {'agility': +1, 'physique': -1}, 'visible': True},
    'crooked': {'slot': 'constitution', 'modifiers': {'agility': -1, 'physique': -1}, 'visible': True},
    'clumsy': {'slot': 'constitution', 'modifiers': {'agility': -1}, 'visible': True},

    'brave': {'slot': 'spirit_feat', 'modifiers': {'spirit': +1}, 'visible': True},
    'shy': {'slot': 'spirit_feat', 'modifiers': {'spirit': -1}, 'visible': True},
    'smart': {'slot': 'mind_feat', 'modifiers': {'mind': +1}, 'visible': True},
    'dumb': {'slot': 'mind_feat', 'modifiers': {'mind': -1}, 'visible': True},
    'sensitive': {'slot': 'sensitivity_feat', 'modifiers': {'sensitivity': +1}, 'visible': True},
    'cool': {'slot': 'sensitivity_feat', 'modifiers': {'sensitivity': -1}, 'visible': True},

    # anatomy
    'small_breast': {'slot': 'breast_size', 'visible': True},
    'normal_breast': {'slot': 'breast_size', 'visible': True},
    'large_breast': {'slot': 'breast_size', 'visible': True},

    'small_penis': {'slot': 'penis_size', 'visible': True},
    'normal_penis': {'slot': 'penis_size', 'visible': True},
    'large_penis': {'slot': 'penis_size', 'visible': True},

    'human_penis': {'slot': 'penis_type', 'visible': True},
    'canine_penis': {'slot': 'penis_type', 'visible': True},

    # needs
    'greedy': {'slot': 'prosperity_feat', 'modifiers': {'prosperity': +1}, 'visible': True},
    'generous': {'slot': 'prosperity_feat', 'modifiers': {'prosperity': -1}, 'visible': True},
    'gourmet': {'slot': 'nutrition_feat', 'modifiers': {'nutrition': +1}, 'visible': True},
    'moderate_eater': {'slot': 'nutrition_feat', 'modifiers': {'nutrition': -1}, 'visible': True},
    'low_pain_threshold': {'slot': 'wellness_feat', 'modifiers': {'wellness': +1}, 'visible': True},
    'high_pain_threshold': {'slot': 'wellness_feat', 'modifiers': {'wellness': -1}, 'visible': True},
    'sybarite': {'slot': 'comfort_feat', 'modifiers': {'comfort': +1}, 'visible': True},
    'ascetic': {'slot': 'comfort_feat', 'modifiers': {'comfort': -1}, 'visible': True},
    'energetic': {'slot': 'activity_feat', 'modifiers': {'activity': +1}, 'visible': True},
    'lazy': {'slot': 'activity_feat', 'modifiers': {'activity': -1}, 'visible': True},
    'extrovert': {'slot': 'communication_feat', 'modifiers': {'communication': +1}, 'visible': True},
    'introvert': {'slot': 'communication_feat', 'modifiers': {'communication': -1}, 'visible': True},
    'curious': {'slot': 'amusement_feat', 'modifiers': {'amusement': +1}, 'visible': True},
    'dull': {'slot': 'amusement_feat', 'modifiers': {'amusement': -1}, 'visible': True},
    'dominant': {'slot': 'authority_feat', 'modifiers': {'authority': +1}, 'visible': True},
    'submissive': {'slot': 'authority_feat', 'modifiers': {'authority': -1}, 'visible': True},
    'ambitious': {'slot': 'ambition_feat', 'modifiers': {'ambition': +1}, 'visible': True},
    'modest': {'slot': 'ambition_feat', 'modifiers': {'ambition': -1}, 'visible': True},
    'lewd': {'slot': 'eros_feat', 'modifiers': {'eros': +1}, 'visible': True},
    'frigid': {'slot': 'eros_feat', 'modifiers': {'eros': -1}, 'visible': True},

    # nutrition
    'slim': {'slot': 'shape', 'modifiers': {'nutrition': 1}, 'visible': True, 'value': 1},
    'emaciated': {'slot': 'shape', 'modifiers': {'nutrition': 2}, 'visible': True, 'value': 2},
    'chubby': {'slot': 'shape', 'modifiers': {'nutrition': -1}, 'visible': True, 'value': -1},
    'obese': {'slot': 'shape', 'modifiers': {'nutrition': -1}, 'visible': True, 'value': -1},
    'starving': {'slot': None, 'modifiers': {'physique': -1}, 'visible': True},
    'dyspnoea': {'visible': True},
    'diabetes': {'visible': False},

    'dead': {'visible': True},
}


