init python:
        
    ## HOMEWORLDS 
    
    homeworlds_dict = {
        'wild':{
            'available_technical_levels': [0],
            'available_prestige_levels': [0],
            'name': __('wild'),
            'descriptions': [__('wild world 1'), __('wild world 2'), __('wild world 3'), ]
        },
        'prehistoric':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('prehistoric'),
            'descriptions': [__('prehistoric world 1'), __('prehistoric world 2'), __('prehistoric world 3'), ]
        },
        'lowtec':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('lowtec'),
            'descriptions': [__('lowtec world 1'), __('lowtec world 2'), __('lowtec world 3'), ]
        },
        'fantasy':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('fantasy'),
            'descriptions': [__('fantasy world 1'), __('fantasy world 2'), __('fantasy world 3'), ]
        },
        'imperial':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('imperial'),
            'descriptions': [__('imperial world 1'), __('imperial world 2'), __('imperial world 3'), ]
        },
        'steampunk':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('steampunk'),
            'descriptions': [__('steampunk world 1'), __('steampunk world 2'), __('steampunk world 3'), ]
        },
        'modern':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('modern'),
            'descriptions': [__('modern world 1'), __('modern world 2'), __('modern world 3'), ]
        },
        'cyberpunk':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('cyberpunk'),
            'descriptions': [__('cyberpunk world 1'), __('cyberpunk world 2'), __('cyberpunk world 3'), ]
        },        
        'utopia':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('utopia'),
            'descriptions': [__('utopia world 1'), __('utopia world 2'), __('utopia world 3'), ]
        },
        'dystopia':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('dystopia'),
            'descriptions': [__('dystopia world 1'), __('dystopia world 2'), __('dystopia world 3'), ]
        },
        'spaceopera':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('spaceopera'),
            'descriptions': [__('spaceopera world 1'), __('spaceopera world 2'), __('spaceopera world 3'), ]
        },
    }
    
    
    ## FAMILIES 
    
    families_dict = {
        'unknown':{
            'name': __('unknown'),
            'available_technical_levels': [0],
            'available_prestige_levels': [0],
            'technical_level': 0,
            'prestige_level': 0
        },
        'orphan':{
            'name': __('orphan'),
            'available_technical_levels': [1, 2, 3, 4, 5],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },
        'commune':{
            'name': __('commune'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },    
        'slave':{
            'name': __('slave'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },
        'serf':{
            'name': __('serf'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },
        'low':{
            'name': __('low-class'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },   
        'middle':{
            'name': __('middle-class'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },
        'high':{
            'name': __('high-class'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },
        'noble':{
            'name': __('noble'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'technical_level': 1,
            'prestige_level': 1
        },           
    }
    
    
    ## EDUCATIONS 
    
    educations_dict = {
        'carefree':{
            'name': __('carefree'),
            'available_technical_levels': [0],
            'available_prestige_levels': [0],
            'technical_level': 0,
            'prestige_level': 0,
        },
        'urchin':{
            'name': __('urchin'),
            'available_technical_levels': [1, 2, 3],
            'available_prestige_levels': [2],
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': [('expirience', 1)],
            'athletics': [('expirience', 2)],
            'stealth': [('expirience', 3)],
            'streetwise': ['training', ('expirience', 4)],
            },
        },
        'natural':{
            'name': __('natural'),
            'available_technical_levels': [1],
            'available_prestige_levels': [1],
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': [('expirience', 1)],
            'stealth': ['training', ('expirience', 2)],
            'survival': ['training', ('expirience', 3)],
            },            
        },
        'forced_labor':{
            'name': __('forced labor'),
            'available_technical_levels': [2, 3],
            'available_prestige_levels': [1],
            'technical_level': 2,
            'prestige_level': 1,
            'skills': {
            'athletics': ['training', ('expirience', 1)],
            },            
        },
        'apprentice':{
            'name': __('apprentice'),
            'available_technical_levels': [2, 3],
            'available_prestige_levels': [2, 3],
            'technical_level': 2,
            'prestige_level': 2,
            'skills': {
            'craft': ['training', ('expirience', 1)],
            },            
        },
        'domestic':{
            'name': __('domestic'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [1, 2, 3, 4],
            'technical_level': 2,
            'prestige_level': 2,
            'skills': {
            'housekeeping': ['training', ('expirience', 1)],
            },            
        },
        'educated':{
            'name': __('educated'),
            'available_technical_levels': [3, 4, 5],
            'available_prestige_levels': [3, 4],
            'technical_level': 3,
            'prestige_level': 3,
            'skills': {
            'scholarship': ['training',],
            'alchemy': ['training'],
            'concentration': ['training',],
            'expression': ['training'],
            'management': ['training'],            
            },            
        },
        'martial':{
            'name': __('martial'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [2, 3, 4, 5],
            'technical_level': 2,
            'prestige_level': 2,
            'skills': {
            'athletics': ['training',],
            'combat': ['training',],
            'observation': ['training',],
            },            
        },
         'aristocratic':{
            'name': __('aristocratic'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [4, 5],
            'technical_level': 2,
            'prestige_level': 5,
            'skills': {
            'charisma': ['training', ('expirience', 2)],
            'management': ['training'],
            'expression': ['training', ('expirience', 1)],         
            'scholarship': ['training'],
            },            
        },
           'artistic':{
            'name': __('artistic'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [2, 3, 4],
            'technical_level': 2,
            'prestige_level': 2,
            'skills': {
            'sex': ['training',],
            'charisma': ['training', ('expirience', 1)],            
            'expression': ['training', ('expirience', 2)],
            },            
        },     
    }
    
    
    ## OCCUOPATIONS 
    
    occupations_dict = {
        'athlete':{
            'name': __('athlete'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'daytaler':{
            'name': __('daytaler'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'lumberjack':{
            'name': __('lumberjack'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'miner':{
            'name': __('miner'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'mason':{
            'name': __('mason'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'porter':{
            'name': __('porter'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'rower':{
            'name': __('rower'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'peasant':{
            'name': __('peasant'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'athletics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'mercenary':{
            'name': __('mercenary'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'sellsword':{
            'name': __('sellsword'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'gladiator':{
            'name': __('gladiator'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'thug':{
            'name': __('thug'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'raider':{
            'name': __('raider'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'soldier':{
            'name': __('soldier'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'pirate':{
            'name': __('pirate'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'officer':{
            'name': __('officer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'knight':{
            'name': __('knight'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'combat': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'assasin':{
            'name': __('assasin'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'stealth': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'thief':{
            'name': __('thief'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'stealth': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'scout':{
            'name': __('scout'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'stealth': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'spy':{
            'name': __('spy'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'stealth': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'smith':{
            'name': __('smith'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'carpenter':{
            'name': __('carpenter'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'engraver':{
            'name': __('engraver'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'cartwright':{
            'name': __('cartwright'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'cobbler':{
            'name': __('cobbler'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'tanner':{
            'name': __('tanner'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'potter':{
            'name': __('potter'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'plumber':{
            'name': __('plumber'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'sculptor':{
            'name': __('sculptor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'glassmaker':{
            'name': __('glassmaker'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'artisan':{
            'name': __('artisan'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'jewler':{
            'name': __('jewler'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'tinker':{
            'name': __('tinker'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'craft': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'athlete':{
            'name': __('athlete'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'rethor':{
            'name': __('rethor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'lawyer':{
            'name': __('lawyer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'lobbist':{
            'name': __('lobbist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'phylosopher':{
            'name': __('phylosopher'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'salesman':{
            'name': __('salesman'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'emissary':{
            'name': __('emissary'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'entrepreneur':{
            'name': __('entrepreneur'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'entertainer':{
            'name': __('entertainer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'escort':{
            'name': __('escort'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'storyteller':{
            'name': __('storyteller'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'bonvivan':{
            'name': __('bonvivan'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'impostor':{
            'name': __('impostor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'preacher':{
            'name': __('preacher'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'actor':{
            'name': __('actor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'charisma': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'psychic':{
            'name': __('psychic'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'concentration': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'monk':{
            'name': __('monk'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'concentration': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'yogi':{
            'name': __('yogi'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'concentration': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'hermit':{
            'name': __('hermit'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'concentration': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'ascetic':{
            'name': __('ascetic'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'concentration': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'manager':{
            'name': __('manager'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'merchant':{
            'name': __('merchant'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'accountant':{
            'name': __('accountant'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'clerk':{
            'name': __('clerk'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'scribe':{
            'name': __('scribe'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'administrator':{
            'name': __('administrator'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'quartermaster':{
            'name': __('quartermaster'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'auditor':{
            'name': __('auditor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'secretary':{
            'name': __('secretary'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'teacher':{
            'name': __('teacher'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'director':{
            'name': __('director'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'management': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'outcast':{
            'name': __('outcast'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'survival': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'pathfinder':{
            'name': __('pathfinder'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'survival': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'hunter':{
            'name': __('hunter'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'survival': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'guide':{
            'name': __('guide'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'survival': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'explorer':{
            'name': __('explorer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'survival': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'shaman':{
            'name': __('shaman'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'alchemy':{
            'name': __('alchemy'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'medic':{
            'name': __('medic'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'herbalist':{
            'name': __('herbalist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'pharmacist':{
            'name': __('pharmacist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'apotecary':{
            'name': __('apotecary'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'chemist':{
            'name': __('chemist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'surgeon':{
            'name': __('surgeon'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'anatomist':{
            'name': __('anatomist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'geneticist':{
            'name': __('geneticist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'alchemy': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'pusher':{
            'name': __('pusher'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'biker':{
            'name': __('biker'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'hippie':{
            'name': __('hippie'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'investigator':{
            'name': __('investigator'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'detective':{
            'name': __('detective'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'pimp':{
            'name': __('pimp'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'academic':{
            'name': __('academic'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'scientist':{
            'name': __('scientist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'researcher':{
            'name': __('researcher'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'bookworm':{
            'name': __('bookworm'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'scholar':{
            'name': __('scholar'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'streetwise': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'inventor':{
            'name': __('inventor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'mechanist':{
            'name': __('mechanist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'engineer':{
            'name': __('engineer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'architect':{
            'name': __('architect'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'sapper':{
            'name': __('sapper'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'sysadmin':{
            'name': __('sysadmin'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'coder':{
            'name': __('coder'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'webmaster':{
            'name': __('webmaster'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'hacker':{
            'name': __('hacker'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'mechanics': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'hooker':{
            'name': __('hooker'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },
        'pornoactor':{
            'name': __('pornoactor'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },    
        'webcamwhore':{
            'name': __('webcamwhore'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },
        'paramour':{
            'name': __('paramour'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },
        'slut':{
            'name': __('slut'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },    
        'concubine':{
            'name': __('concubine'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },
        'kunoichi':{
            'name': __('kunoichi'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },
        'stripper':{
            'name': __('stripper'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sex': ['profession'],
            'housekeeping': ['training', ('expirience', 1)]
            },
        },      
        'housewife':{
            'name': __('housewife'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'laundress':{
            'name': __('laundress'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'cook':{
            'name': __('cook'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'butler':{
            'name': __('butler'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'servant':{
            'name': __('servant'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'maid':{
            'name': __('maid'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'chief':{
            'name': __('chief'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'housekeeping': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'sniper':{
            'name': __('sniper'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'observation': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'marksman':{
            'name': __('marksman'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'observation': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'cannoneer':{
            'name': __('cannoneer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'observation': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'watchman':{
            'name': __('watchman'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'observation': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'artist':{
            'name': __('artist'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },      
        'dancer':{
            'name': __('dancer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'gypsy':{
            'name': __('gypsy'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'faquir':{
            'name': __('faquir'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },        
        'musician':{
            'name': __('musician'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'singer':{
            'name': __('singer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'bard':{
            'name': __('bard'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'expression': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'sorcerer':{
            'name': __('sorcerer'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sorcery': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'enchanter':{
            'name': __('enchanter'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sorcery': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
        'mystic':{
            'name': __('mystic'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sorcery': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },    
        'fortuneteller':{
            'name': __('fortuneteller'),
            'technical_level': 1,
            'prestige_level': 1,
            'skills': {
            'sorcery': ['profession'],
            'sex': ['training', ('expirience', 1)]
            },
        },
    }
    
    
    ## CULTURES 
    
    cultures_dict = {
        'slavic':{
            'name': __('slavic'),
            'available_skin_colors': ['white_skin']
        },
        'soviet':{
            'name': __('soviet'),
            'available_skin_colors': ['white_skin']
        },
        'european':{
            'name': __('european'),
            'available_skin_colors': ['white_skin']
        },
        'american':{
            'name': __('american'),
            'available_skin_colors': ['white_skin', 'dark_skin']
        },
        'fantasy':{
            'name': __('fantasy'),
            'available_skin_colors': ['white_skin']
        },
        'nordic':{
            'name': __('nordic'),
            'available_skin_colors': ['white_skin']
        },
        'oriental':{
            'name': __('oriental'),
            'available_skin_colors': ['yellow_skin']
        },
        'papua':{
            'name': __('papua'),
            'available_skin_colors': ['dark_skin']
        },
        'tribal':{
            'name': __('tribal'),
            'available_skin_colors': ['yellow_skin', 'white_skin', 'dark_skin']
        },
        'arabic':{
            'name': __('arabic'),
            'available_skin_colors': ['white_skin', 'dark_skin']
        },
    }

	## EQUIPMENT
	background_equipment = {'lumberjack': {'weapon': 'strudy_axe', 'offhand': None, 'armor': None},
		'miner': {'weapon': 'pickaxe', 'offhand': None, 'armor': None},
		'daytaler': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'rower': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'peasant': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'mason': {'weapon': 'crowbar', 'offhand': None, 'armor': None},
		'porter': {'weapon': 'crowbar', 'offhand': None, 'armor': None},
		'mercenary': {'weapon': 'letal_weapon', 'offhand': 'dagger', 'armor': 'soft_armor'},
		'sellsword': {'weapon': 'sword', 'offhand': 'shield', 'armor': 'hard_armor'},
		'gladiator': {'weapon': 'sword', 'offhand': 'shield', 'armor': 'soft_armor'},
		'thug': {'weapon': 'club', 'offhand': None, 'armor': 'soft_armor'},
		'raider': {'weapon': 'sword', 'offhand': 'dagger', 'armor': 'soft_armor'},
		'soldier': {'weapon': 'letal_weapon', 'offhand': None, 'armor': 'hard_armor'},
		'pirate': {'weapon': 'sword', 'offhand': None, 'armor': None},
		'officer': {'weapon': 'sdw', 'offhand': None, 'armor': None},
		'knight': {'weapon': 'sword', 'offhand': 'shield', 'armor': 'hard_armor'},
		'assasin': {'weapon': 'dagger', 'offhand': None, 'armor': 'soft_armor'},
		'thief': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'scout': {'weapon': 'dagger', 'offhand': None, 'armor': 'soft_armor'},
		'spy': {'weapon': 'dagger', 'offhand': None, 'armor': None},
		'smith': {'weapon': 'maul', 'offhand': None, 'armor': None},
		'carpenter': {'weapon': 'hand_axe', 'offhand': None, 'armor': None},
		'cobbler': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'tanner': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'artisan': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'monk': {'weapon': 'quarterstaff', 'offhand': None, 'armor': None},
		'quartermaster': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'outcast': {'weapon': 'quarterstaff', 'offhand': None, 'armor': None},
		'pathfinder': {'weapon': 'dagger', 'offhand': None, 'armor': 'soft_armor'},
		'hunter': {'weapon': 'hunting_weapon', 'offhand': None, 'armor': None},
		'guide': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'explorer': {'weapon': 'dagger', 'offhand': None, 'armor': None},
		'medic': {'weapon': 'lancet', 'offhand': None, 'armor': None},
		'herbalist': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'surgeon': {'weapon': 'lancet', 'offhand': None, 'armor': None},
		'anatomist': {'weapon': 'lancet', 'offhand': None, 'armor': None},
		'biker': {'weapon': 'crowbar', 'offhand': None, 'armor': 'leather_coat'},
		'pimp': {'weapon': 'knuckles', 'offhand': None, 'armor': None},
		'mechanist': {'weapon': 'crowbar', 'offhand': None, 'armor': None},
		'sapper': {'weapon': 'dagger', 'offhand': None, 'armor': None},
		'cook': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'chief': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'sniper': {'weapon': 'long_weapon', 'offhand': None, 'armor': None},
		'marksman': {'weapon': 'long_weapon', 'offhand': None, 'armor': None},
		'canoneer': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'watchman': {'weapon': 'knife', 'offhand': None, 'armor': None},
		'bard': {'weapon': 'dagger', 'offhand': None, 'armor': None},
		'mystic': {'weapon': 'dagger', 'offhand': None, 'armor': None},
	}
