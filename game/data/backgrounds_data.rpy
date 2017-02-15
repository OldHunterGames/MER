init python:
        
    ## HOMEWORLDS 
    
    homeworlds_dict = {
        'wild':{
            'available_technical_levels': [0],
            'available_prestige_levels': [0],
            'name': __('wild'),
            'features': ['ignorant'], 
            'descriptions': [__('wild world 1'), __('wild world 2'), __('wild world 3'), ]
        },
        'prehistoric':{
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'name': __('prehistoric'),
            'features': ['ignorant'],             
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
            'features': ['educated'],             
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
            'features': ['educated'],                
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
            'features': ['educated'],                
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
            'skills': {'housekeeping': ['training']},                    
            'technical_level': 1,
            'prestige_level': 1
        },
        'serf':{
            'name': __('serf'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'skills': {'housekeeping': ['training']},                    
            'technical_level': 1,
            'prestige_level': 1
        },
        'low':{
            'name': __('low-class'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'skills': {'housekeeping': ['training']},            
            'technical_level': 1,
            'prestige_level': 1
        },   
        'middle':{
            'name': __('middle-class'),
            'available_technical_levels': [1, 2],
            'available_prestige_levels': [1, 2],
            'skills': {'housekeeping': ['training']},        
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
        },
        'natural':{
            'name': __('natural'),
            'available_technical_levels': [1],
            'available_prestige_levels': [1],
            'technical_level': 1,
            'prestige_level': 1,          
        },
        'forced_labor':{
            'name': __('forced labor'),
            'available_technical_levels': [2, 3],
            'available_prestige_levels': [1],
            'technical_level': 2,
            'prestige_level': 1,           
        },
        'apprentice':{
            'name': __('apprentice'),
            'available_technical_levels': [2, 3],
            'available_prestige_levels': [2, 3],
            'technical_level': 2,
            'prestige_level': 2,         
        },
        'domestic':{
            'name': __('domestic'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [1, 2, 3, 4],
            'technical_level': 2,
            'prestige_level': 2,           
        },
        'educated':{
            'name': __('educated'),
            'available_technical_levels': [3, 4, 5],
            'available_prestige_levels': [3, 4],
            'technical_level': 3,
            'prestige_level': 3,          
        },
        'martial':{
            'name': __('martial'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [2, 3, 4, 5],
            'technical_level': 2,
            'prestige_level': 2,           
        },
         'aristocratic':{
            'name': __('aristocratic'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [4, 5],
            'technical_level': 2,
            'prestige_level': 5,            
        },
           'artistic':{
            'name': __('artistic'),
            'available_technical_levels': [2, 3, 4, 5],
            'available_prestige_levels': [2, 3, 4],
            'technical_level': 2,
            'prestige_level': 2,          
        },     
    }
    
    
    ## OCCUOPATIONS 
    
    occupations_dict = {
        'athlete':{
            'name': __('athlete'),
            'technical_level': 1,
            'prestige_level': 1,        
        },
        'daytaler':{
            'name': __('daytaler'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'lumberjack':{
            'name': __('lumberjack'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'miner':{
            'name': __('miner'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'mason':{
            'name': __('mason'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'porter':{
            'name': __('porter'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'rower':{
            'name': __('rower'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'peasant':{
            'name': __('peasant'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'mercenary':{
            'name': __('mercenary'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'sellsword':{
            'name': __('sellsword'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'gladiator':{
            'name': __('gladiator'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'thug':{
            'name': __('thug'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'raider':{
            'name': __('raider'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'soldier':{
            'name': __('soldier'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'pirate':{
            'name': __('pirate'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'officer':{
            'name': __('officer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'knight':{
            'name': __('knight'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'assasin':{
            'name': __('assasin'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'thief':{
            'name': __('thief'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'scout':{
            'name': __('scout'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'spy':{
            'name': __('spy'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'smith':{
            'name': __('smith'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'carpenter':{
            'name': __('carpenter'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'engraver':{
            'name': __('engraver'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'cartwright':{
            'name': __('cartwright'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'cobbler':{
            'name': __('cobbler'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'tanner':{
            'name': __('tanner'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'potter':{
            'name': __('potter'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'plumber':{
            'name': __('plumber'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'sculptor':{
            'name': __('sculptor'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'glassmaker':{
            'name': __('glassmaker'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'artisan':{
            'name': __('artisan'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'jewler':{
            'name': __('jewler'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'tinker':{
            'name': __('tinker'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'rethor':{
            'name': __('rethor'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'lawyer':{
            'name': __('lawyer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'lobbist':{
            'name': __('lobbist'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'phylosopher':{
            'name': __('phylosopher'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'salesman':{
            'name': __('salesman'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'emissary':{
            'name': __('emissary'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'entrepreneur':{
            'name': __('entrepreneur'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'entertainer':{
            'name': __('entertainer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'escort':{
            'name': __('escort'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'storyteller':{
            'name': __('storyteller'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'bonvivan':{
            'name': __('bonvivan'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'impostor':{
            'name': __('impostor'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'preacher':{
            'name': __('preacher'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'actor':{
            'name': __('actor'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'psychic':{
            'name': __('psychic'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'monk':{
            'name': __('monk'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'yogi':{
            'name': __('yogi'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'hermit':{
            'name': __('hermit'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'ascet':{
            'name': __('ascet'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'manager':{
            'name': __('manager'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'merchant':{
            'name': __('merchant'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'accountant':{
            'name': __('accountant'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'clerk':{
            'name': __('clerk'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'scribe':{
            'name': __('scribe'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'administrator':{
            'name': __('administrator'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'quartermaster':{
            'name': __('quartermaster'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'auditor':{
            'name': __('auditor'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'secretary':{
            'name': __('secretary'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'teacher':{
            'name': __('teacher'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'director':{
            'name': __('director'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'outcast':{
            'name': __('outcast'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'pathfinder':{
            'name': __('pathfinder'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'hunter':{
            'name': __('hunter'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'guide':{
            'name': __('guide'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'explorer':{
            'name': __('explorer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'shaman':{
            'name': __('shaman'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'alchemic':{
            'name': __('alchemic'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'medic':{
            'name': __('medic'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'herbalist':{
            'name': __('herbalist'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'pharmacist':{
            'name': __('pharmacist'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'apotecary':{
            'name': __('apotecary'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'chemist':{
            'name': __('chemist'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'surgeon':{
            'name': __('surgeon'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'anatomist':{
            'name': __('anatomist'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'geneticist':{
            'name': __('geneticist'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'pusher':{
            'name': __('pusher'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'biker':{
            'name': __('biker'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'hippie':{
            'name': __('hippie'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'investigator':{
            'name': __('investigator'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'detective':{
            'name': __('detective'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'pimp':{
            'name': __('pimp'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'academic':{
            'name': __('academic'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'scientist':{
            'name': __('scientist'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'researcher':{
            'name': __('researcher'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'bookworm':{
            'name': __('bookworm'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'scholar':{
            'name': __('scholar'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'inventor':{
            'name': __('inventor'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'mechanist':{
            'name': __('mechanist'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'engineer':{
            'name': __('engineer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'architect':{
            'name': __('architect'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'sapper':{
            'name': __('sapper'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'sysadmin':{
            'name': __('sysadmin'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'coder':{
            'name': __('coder'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'webmaster':{
            'name': __('webmaster'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'hacker':{
            'name': __('hacker'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'hooker':{
            'name': __('hooker'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'pornoactor':{
            'name': __('pornoactor'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'webcamwhore':{
            'name': __('webcamwhore'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'paramour':{
            'name': __('paramour'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'slut':{
            'name': __('slut'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'concubine':{
            'name': __('concubine'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'kunoichi':{
            'name': __('kunoichi'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'stripper':{
            'name': __('stripper'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'housewife':{
            'name': __('housewife'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'laundress':{
            'name': __('laundress'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'cook':{
            'name': __('cook'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'butler':{
            'name': __('butler'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'servant':{
            'name': __('servant'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'maid':{
            'name': __('maid'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'chief':{
            'name': __('chief'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'sniper':{
            'name': __('sniper'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'marksman':{
            'name': __('marksman'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'cannoneer':{
            'name': __('cannoneer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'watchman':{
            'name': __('watchman'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'artist':{
            'name': __('artist'),
            'technical_level': 1,
            'prestige_level': 1,
        },      
        'dancer':{
            'name': __('dancer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'gypsy':{
            'name': __('gypsy'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'faquir':{
            'name': __('faquir'),
            'technical_level': 1,
            'prestige_level': 1,
        },        
        'musician':{
            'name': __('musician'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'singer':{
            'name': __('singer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'bard':{
            'name': __('bard'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'sorcerer':{
            'name': __('sorcerer'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'enchanter':{
            'name': __('enchanter'),
            'technical_level': 1,
            'prestige_level': 1,
        },
        'mystic':{
            'name': __('mystic'),
            'technical_level': 1,
            'prestige_level': 1,
        },    
        'fortuneteller':{
            'name': __('fortuneteller'),
            'technical_level': 1,
            'prestige_level': 1,
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
    background_equipment = {'lumberjack': {'main_hand': 'strudy_axe', 'other_hand': None, 'armor': None},
        'miner': {'main_hand': 'pickaxe', 'other_hand': None, 'armor': None},
        'daytaler': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'rower': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'peasant': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'mason': {'main_hand': 'crowbar', 'other_hand': None, 'armor': None},
        'porter': {'main_hand': 'crowbar', 'other_hand': None, 'armor': None},
        'mercenary': {'main_hand': 'letal_weapon', 'other_hand': 'dagger', 'armor': 'soft_armor'},
        'sellsword': {'main_hand': 'sword', 'other_hand': 'shield', 'armor': 'hard_armor'},
        'gladiator': {'main_hand': 'sword', 'other_hand': 'shield', 'armor': 'soft_armor'},
        'thug': {'main_hand': 'club', 'other_hand': None, 'armor': 'soft_armor'},
        'raider': {'main_hand': 'sword', 'other_hand': 'dagger', 'armor': 'soft_armor'},
        'soldier': {'main_hand': 'letal_weapon', 'other_hand': None, 'armor': 'hard_armor'},
        'pirate': {'main_hand': 'sword', 'other_hand': None, 'armor': None},
        'officer': {'main_hand': 'sdw', 'other_hand': None, 'armor': None},
        'knight': {'main_hand': 'sword', 'other_hand': 'shield', 'armor': 'hard_armor'},
        'assasin': {'main_hand': 'dagger', 'other_hand': None, 'armor': 'soft_armor'},
        'thief': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'scout': {'main_hand': 'dagger', 'other_hand': None, 'armor': 'soft_armor'},
        'spy': {'main_hand': 'dagger', 'other_hand': None, 'armor': None},
        'smith': {'main_hand': 'maul', 'other_hand': None, 'armor': None},
        'carpenter': {'main_hand': 'hand_axe', 'other_hand': None, 'armor': None},
        'cobbler': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'tanner': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'artisan': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'monk': {'main_hand': 'quarterstaff', 'other_hand': None, 'armor': None},
        'quartermaster': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'outcast': {'main_hand': 'quarterstaff', 'other_hand': None, 'armor': None},
        'pathfinder': {'main_hand': 'dagger', 'other_hand': None, 'armor': 'soft_armor'},
        'hunter': {'main_hand': 'hunting_weapon', 'other_hand': None, 'armor': None},
        'guide': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'explorer': {'main_hand': 'dagger', 'other_hand': None, 'armor': None},
        'medic': {'main_hand': 'lancet', 'other_hand': None, 'armor': None},
        'herbalist': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'surgeon': {'main_hand': 'lancet', 'other_hand': None, 'armor': None},
        'anatomist': {'main_hand': 'lancet', 'other_hand': None, 'armor': None},
        'biker': {'main_hand': 'crowbar', 'other_hand': None, 'armor': 'leather_coat'},
        'pimp': {'main_hand': 'knuckles', 'other_hand': None, 'armor': None},
        'mechanist': {'main_hand': 'crowbar', 'other_hand': None, 'armor': None},
        'sapper': {'main_hand': 'dagger', 'other_hand': None, 'armor': None},
        'cook': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'chief': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'sniper': {'main_hand': 'long_weapon', 'other_hand': None, 'armor': None},
        'marksman': {'main_hand': 'long_weapon', 'other_hand': None, 'armor': None},
        'canoneer': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'watchman': {'main_hand': 'knife', 'other_hand': None, 'armor': None},
        'bard': {'main_hand': 'dagger', 'other_hand': None, 'armor': None},
        'mystic': {'main_hand': 'dagger', 'other_hand': None, 'armor': None},
    }
