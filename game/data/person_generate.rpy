########################################
##  Person generator data and functions
##

init python:
    
    data_appearence_list = {
        'male': {
            'junior': {
                #Common  
                '9': 'innocent_appearance', 
                '10': 'gentle_appearance', 
                '11': 'candid_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'wild_appearance', 
                '8': 'foxy_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'unremarkible_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'bold_appearance',  
                #SuperRare
                '4': 'flawless_appearance', 
                '17': 'flawless_appearance',      
                #UberRare                
                '3': 'unusual_appearance', 
                '18': 'sleasy_appearance',           
                }, 
            'adolescent': {
                #Common  
                '9': 'coarse_appearance', 
                '10': 'bold_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'innocent_appearance', 
                '8': 'candid_appearance', 
                '13': 'wild_appearance',    
                '14': 'flawless_appearance',  
                #Rare
                '5': 'gentle_appearance', 
                '6': 'foxy_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'unremarkible_appearance',      
                #UberRare                
                '3': 'sleasy_appearance', 
                '18': 'unremarkible_appearance',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'coarse_appearance', 
                '10': 'bold_appearance', 
                '11': 'bold_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'candid_appearance', 
                '8': 'wild_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'flawless_appearance', 
                '6': 'gentle_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'foxy_appearance',      
                #UberRare                
                '3': 'innocent_appearance', 
                '18': 'sleasy_appearance',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'coarse_appearance', 
                '10': 'bold_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'wild_appearance', 
                '8': 'candid_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'flawless_appearance', 
                '6': 'unremarkible_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'foxy_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'gentle_appearance',      
                #UberRare                
                '3': 'innocent_appearance', 
                '18': 'sleasy_appearance',                                                                                   
                },                 
        },
        
        'female': {
            'junior': {
                #Common  
                '9': 'innocent_appearance', 
                '10': 'gentle_appearance', 
                '11': 'foxy_appearance',                                                                                 
                '12': 'candid_appearance',  
                #Uncommon 
                '7': 'flawless_appearance', 
                '8': 'unremarkible_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'wild_appearance', 
                '6': 'unremarkible_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'coarse_appearance', 
                '17': 'unusual_appearance',      
                #UberRare                
                '3': 'bold_appearance', 
                '18': 'sleasy_appearance',           
                }, 
            'adolescent': {
                #Common  
                '9': 'flawless_appearance', 
                '10': 'gentle_appearance', 
                '11': 'candid_appearance',                                                                                 
                '12': 'foxy_appearance',  
                #Uncommon 
                '7': 'innocent_appearance', 
                '8': 'sleasy_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'wild_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'bold_appearance',      
                #UberRare                
                '3': 'unremarkible_appearance', 
                '18': 'unremarkible_appearance',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'sleasy_appearance', 
                '10': 'gentle_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'foxy_appearance', 
                '8': 'flawless_appearance', 
                '13': 'candid_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'innocent_appearance', 
                '15': 'wild_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'bold_appearance',      
                #UberRare                
                '3': 'unremarkible_appearance', 
                '18': 'unremarkible_appearance',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'unremarkible_appearance', 
                '10': 'unremarkible_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'coarse_appearance', 
                '8': 'gentle_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'foxy_appearance', 
                '6': 'flawless_appearance', 
                '15': 'unusual_appearance',   
                '16': 'candid_appearance',  
                #SuperRare
                '4': 'sleasy_appearance', 
                '17': 'innocent_appearance',      
                #UberRare                
                '3': 'bold_appearance', 
                '18': 'wild_appearance',                                                                                   
                },                 
        },        

        'shemale': {
            'junior': {
                #Common  
                '9': 'innocent_appearance', 
                '10': 'gentle_appearance', 
                '11': 'foxy_appearance',                                                                                 
                '12': 'candid_appearance',  
                #Uncommon 
                '7': 'flawless_appearance', 
                '8': 'unremarkible_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'wild_appearance', 
                '6': 'unremarkible_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'coarse_appearance', 
                '17': 'unusual_appearance',      
                #UberRare                
                '3': 'bold_appearance', 
                '18': 'sleasy_appearance',           
                }, 
            'adolescent': {
                #Common  
                '9': 'flawless_appearance', 
                '10': 'gentle_appearance', 
                '11': 'candid_appearance',                                                                                 
                '12': 'foxy_appearance',  
                #Uncommon 
                '7': 'innocent_appearance', 
                '8': 'sleasy_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'wild_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'bold_appearance',      
                #UberRare                
                '3': 'unremarkible_appearance', 
                '18': 'unremarkible_appearance',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'sleasy_appearance', 
                '10': 'gentle_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'foxy_appearance', 
                '8': 'flawless_appearance', 
                '13': 'candid_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'innocent_appearance', 
                '15': 'wild_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'bold_appearance',      
                #UberRare                
                '3': 'unremarkible_appearance', 
                '18': 'unremarkible_appearance',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'unremarkible_appearance', 
                '10': 'unremarkible_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'coarse_appearance', 
                '8': 'gentle_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'foxy_appearance', 
                '6': 'flawless_appearance', 
                '15': 'unusual_appearance',   
                '16': 'candid_appearance',  
                #SuperRare
                '4': 'sleasy_appearance', 
                '17': 'innocent_appearance',      
                #UberRare                
                '3': 'bold_appearance', 
                '18': 'wild_appearance',                                                                                   
                },                  
        },

        'sexless': {
            'junior': {
                #Common  
                '9': 'innocent_appearance', 
                '10': 'gentle_appearance', 
                '11': 'foxy_appearance',                                                                                 
                '12': 'candid_appearance',  
                #Uncommon 
                '7': 'flawless_appearance', 
                '8': 'unremarkible_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'wild_appearance', 
                '6': 'unremarkible_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'coarse_appearance', 
                '17': 'unusual_appearance',      
                #UberRare                
                '3': 'bold_appearance', 
                '18': 'sleasy_appearance',           
                }, 
            'adolescent': {
                #Common  
                '9': 'flawless_appearance', 
                '10': 'gentle_appearance', 
                '11': 'candid_appearance',                                                                                 
                '12': 'foxy_appearance',  
                #Uncommon 
                '7': 'innocent_appearance', 
                '8': 'sleasy_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'wild_appearance', 
                '15': 'unremarkible_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'bold_appearance',      
                #UberRare                
                '3': 'unremarkible_appearance', 
                '18': 'unremarkible_appearance',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'sleasy_appearance', 
                '10': 'gentle_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'foxy_appearance', 
                '8': 'flawless_appearance', 
                '13': 'candid_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'coarse_appearance', 
                '6': 'innocent_appearance', 
                '15': 'wild_appearance',   
                '16': 'unremarkible_appearance',  
                #SuperRare
                '4': 'unusual_appearance', 
                '17': 'bold_appearance',      
                #UberRare                
                '3': 'unremarkible_appearance', 
                '18': 'unremarkible_appearance',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'unremarkible_appearance', 
                '10': 'unremarkible_appearance', 
                '11': 'unremarkible_appearance',                                                                                 
                '12': 'unremarkible_appearance',  
                #Uncommon 
                '7': 'coarse_appearance', 
                '8': 'gentle_appearance', 
                '13': 'unremarkible_appearance',    
                '14': 'unremarkible_appearance',  
                #Rare
                '5': 'foxy_appearance', 
                '6': 'flawless_appearance', 
                '15': 'unusual_appearance',   
                '16': 'candid_appearance',  
                #SuperRare
                '4': 'sleasy_appearance', 
                '17': 'innocent_appearance',      
                #UberRare                
                '3': 'bold_appearance', 
                '18': 'wild_appearance',                                                                                   
                },        
        },
                        
    }
    
    data_voice_list = {
        'male': {
            'junior': {
                #Common  
                '9': 'voice_sweet', 
                '10': 'voice_clear', 
                '11': 'voice_soft',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_sweet', 
                '8': 'voice_stuttering', 
                '13': 'voice_soft',    
                '14': 'voice_clear',  
                #Rare
                '5': 'voice_high', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_charming', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_husky', 
                '18': 'voice_strong',           
                }, 
            'adolescent': {
                #Common  
                '9': 'voice_high', 
                '10': 'voice_deep', 
                '11': 'voice_deep',                                                                                 
                '12': 'voice_deep',  
                #Uncommon 
                '7': 'voice_sweet', 
                '8': 'voice_clear', 
                '13': 'voice_charming',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_soft', 
                '6': 'voice_high', 
                '15': 'voice_stuttering',   
                '16': 'voice_deep',  
                #SuperRare
                '4': 'voice_husky', 
                '17': 'voice_strong',      
                #UberRare                
                '3': 'voice_stuttering', 
                '18': 'voice_deep',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'voice_strong', 
                '10': 'voice_deep', 
                '11': 'voice_deep',                                                                                 
                '12': 'voice_deep',  
                #Uncommon 
                '7': 'voice_strong', 
                '8': 'voice_deep', 
                '13': 'voice_deep',    
                '14': 'voice_husky',  
                #Rare
                '5': 'voice_deep', 
                '6': 'voice_charming', 
                '15': 'voice_clear',   
                '16': 'voice_soft',  
                #SuperRare
                '4': 'voice_sweet', 
                '17': 'voice_high',      
                #UberRare                
                '3': 'voice_stuttering', 
                '18': 'voice_high',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'voice_husky', 
                '10': 'voice_stuttering', 
                '11': 'voice_deep',                                                                                 
                '12': 'voice_deep',  
                #Uncommon 
                '7': 'voice_stuttering', 
                '8': 'voice_husky', 
                '13': 'voice_deep',    
                '14': 'voice_deep',  
                #Rare
                '5': 'voice_strong', 
                '6': 'voice_soft', 
                '15': 'voice_sweet',   
                '16': 'voice_deep',  
                #SuperRare
                '4': 'voice_charming', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_high', 
                '18': 'voice_clear',                                                                                   
                },                 
        },
        
        'female': {
            'junior': {
                #Common  
                '9': 'voice_sweet', 
                '10': 'voice_clear', 
                '11': 'voice_soft',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_charming', 
                '8': 'voice_soft', 
                '13': 'voice_clear',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_high', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_stuttering', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_strong', 
                '18': 'voice_husky',           
                }, 
            'adolescent': {
                #Common  
                '9': 'voice_clear', 
                '10': 'voice_charming', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_clear', 
                '8': 'voice_sweet', 
                '13': 'voice_soft',    
                '14': 'voice_charming',  
                #Rare
                '5': 'voice_deep', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_strong', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_stuttering', 
                '18': 'voice_husky',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'voice_deep', 
                '10': 'voice_charming', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_deep', 
                '8': 'voice_charming', 
                '13': 'voice_soft',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_sweet', 
                '6': 'voice_strong', 
                '15': 'voice_soft',   
                '16': 'voice_deep',  
                #SuperRare
                '4': 'voice_husky', 
                '17': 'voice_stuttering',      
                #UberRare                
                '3': 'voice_husky', 
                '18': 'voice_stuttering',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'voice_deep', 
                '10': 'voice_husky', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_husky', 
                '8': 'voice_stuttering', 
                '13': 'voice_soft',    
                '14': 'voice_deep',  
                #Rare
                '5': 'voice_sweet', 
                '6': 'voice_soft', 
                '15': 'voice_deep',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_charming', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_clear', 
                '18': 'voice_strong',                                                                                   
                },                 
        },        

        'shemale': {
            'junior': {
                #Common  
                '9': 'voice_sweet', 
                '10': 'voice_clear', 
                '11': 'voice_soft',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_charming', 
                '8': 'voice_soft', 
                '13': 'voice_clear',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_high', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_stuttering', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_strong', 
                '18': 'voice_husky',           
                }, 
            'adolescent': {
                #Common  
                '9': 'voice_clear', 
                '10': 'voice_charming', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_clear', 
                '8': 'voice_sweet', 
                '13': 'voice_soft',    
                '14': 'voice_charming',  
                #Rare
                '5': 'voice_deep', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_strong', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_stuttering', 
                '18': 'voice_husky',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'voice_deep', 
                '10': 'voice_charming', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_deep', 
                '8': 'voice_charming', 
                '13': 'voice_soft',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_sweet', 
                '6': 'voice_strong', 
                '15': 'voice_soft',   
                '16': 'voice_deep',  
                #SuperRare
                '4': 'voice_husky', 
                '17': 'voice_stuttering',      
                #UberRare                
                '3': 'voice_husky', 
                '18': 'voice_stuttering',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'voice_deep', 
                '10': 'voice_husky', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_husky', 
                '8': 'voice_stuttering', 
                '13': 'voice_soft',    
                '14': 'voice_deep',  
                #Rare
                '5': 'voice_sweet', 
                '6': 'voice_soft', 
                '15': 'voice_deep',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_charming', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_clear', 
                '18': 'voice_strong',                                                                                   
                },                 
        },        
        
        'sexless': {
            'junior': {
                #Common  
                '9': 'voice_sweet', 
                '10': 'voice_clear', 
                '11': 'voice_soft',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_charming', 
                '8': 'voice_soft', 
                '13': 'voice_clear',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_high', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_stuttering', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_strong', 
                '18': 'voice_husky',           
                }, 
            'adolescent': {
                #Common  
                '9': 'voice_clear', 
                '10': 'voice_charming', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_clear', 
                '8': 'voice_sweet', 
                '13': 'voice_soft',    
                '14': 'voice_charming',  
                #Rare
                '5': 'voice_deep', 
                '6': 'voice_high', 
                '15': 'voice_high',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_strong', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_stuttering', 
                '18': 'voice_husky',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'voice_deep', 
                '10': 'voice_charming', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_deep', 
                '8': 'voice_charming', 
                '13': 'voice_soft',    
                '14': 'voice_high',  
                #Rare
                '5': 'voice_sweet', 
                '6': 'voice_strong', 
                '15': 'voice_soft',   
                '16': 'voice_deep',  
                #SuperRare
                '4': 'voice_husky', 
                '17': 'voice_stuttering',      
                #UberRare                
                '3': 'voice_husky', 
                '18': 'voice_stuttering',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'voice_deep', 
                '10': 'voice_husky', 
                '11': 'voice_high',                                                                                 
                '12': 'voice_high',  
                #Uncommon 
                '7': 'voice_husky', 
                '8': 'voice_stuttering', 
                '13': 'voice_soft',    
                '14': 'voice_deep',  
                #Rare
                '5': 'voice_sweet', 
                '6': 'voice_soft', 
                '15': 'voice_deep',   
                '16': 'voice_high',  
                #SuperRare
                '4': 'voice_charming', 
                '17': 'voice_deep',      
                #UberRare                
                '3': 'voice_clear', 
                '18': 'voice_strong',                                                                                   
                },                 
        },        
    }

    data_skin_list = {
        'male': {
            'junior': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_normal',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_normal', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_scars',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_pigmented',      
                #UberRare                
                '3': 'skin_freckled', 
                '18': 'skin_wrinkly',           
                }, 
            'adolescent': {
                #Common  
                '9': 'skin_normal', 
                '10': 'skin_normal', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_normal',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_silky', 
                '6': 'skin_clear', 
                '15': 'skin_normal',   
                '16': 'skin_scars',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_pigmented',      
                #UberRare                
                '3': 'skin_freckled', 
                '18': 'skin_wrinkly',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'skin_normal', 
                '10': 'skin_normal', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_scars', 
                '8': 'skin_normal', 
                '13': 'skin_normal',    
                '14': 'skin_freckled',  
                #Rare
                '5': 'skin_pigmented', 
                '6': 'skin_pocky', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_wrinkly', 
                '17': 'skin_pigmented',      
                #UberRare                
                '3': 'skin_clear', 
                '18': 'skin_silky',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'skin_wrinkly', 
                '10': 'skin_pigmented', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_normal', 
                '8': 'skin_normal', 
                '13': 'skin_normal',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_scars', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_pocky',  
                #SuperRare
                '4': 'skin_freckled', 
                '17': 'skin_freckled',      
                #UberRare                
                '3': 'skin_silky', 
                '18': 'skin_clear',                                                                                   
                },                 
        },
        
        'female': {
            'junior': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_clear',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_normal',    
                '14': 'skin_silky',  
                #Rare
                '5': 'skin_freckled', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_scars',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',           
                }, 
            'adolescent': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_clear', 
                '8': 'skin_silky', 
                '13': 'skin_normal',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_freckled', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_scars',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'skin_normal', 
                '10': 'skin_normal', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_freckled',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_wrinkly', 
                '6': 'skin_pigmented', 
                '15': 'skin_scars',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_wrinkly',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'skin_wrinkly', 
                '10': 'skin_pigmented', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_freckled', 
                '8': 'skin_pocky', 
                '13': 'skin_pigmented',    
                '14': 'skin_wrinkly',  
                #Rare
                '5': 'skin_scars', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_scars', 
                '17': 'skin_normal',      
                #UberRare                
                '3': 'skin_silky', 
                '18': 'skin_clear',                                                                                   
                },                 
        },        

        'shemale': {
            'junior': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_clear',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_normal',    
                '14': 'skin_silky',  
                #Rare
                '5': 'skin_freckled', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_scars',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',           
                }, 
            'adolescent': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_clear', 
                '8': 'skin_silky', 
                '13': 'skin_normal',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_freckled', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_scars',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'skin_normal', 
                '10': 'skin_normal', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_freckled',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_wrinkly', 
                '6': 'skin_pigmented', 
                '15': 'skin_scars',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_wrinkly',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'skin_wrinkly', 
                '10': 'skin_pigmented', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_freckled', 
                '8': 'skin_pocky', 
                '13': 'skin_pigmented',    
                '14': 'skin_wrinkly',  
                #Rare
                '5': 'skin_scars', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_scars', 
                '17': 'skin_normal',      
                #UberRare                
                '3': 'skin_silky', 
                '18': 'skin_clear',                                                                                   
                },                 
        },   
        
        'sexless': {
            'junior': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_clear',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_normal',    
                '14': 'skin_silky',  
                #Rare
                '5': 'skin_freckled', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_scars',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',           
                }, 
            'adolescent': {
                #Common  
                '9': 'skin_silky', 
                '10': 'skin_clear', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_clear', 
                '8': 'skin_silky', 
                '13': 'skin_normal',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_freckled', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_scars',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'skin_normal', 
                '10': 'skin_normal', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_silky', 
                '8': 'skin_clear', 
                '13': 'skin_freckled',    
                '14': 'skin_normal',  
                #Rare
                '5': 'skin_wrinkly', 
                '6': 'skin_pigmented', 
                '15': 'skin_scars',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_pocky', 
                '17': 'skin_wrinkly',      
                #UberRare                
                '3': 'skin_wrinkly', 
                '18': 'skin_pigmented',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'skin_wrinkly', 
                '10': 'skin_pigmented', 
                '11': 'skin_normal',                                                                                 
                '12': 'skin_normal',  
                #Uncommon 
                '7': 'skin_freckled', 
                '8': 'skin_pocky', 
                '13': 'skin_pigmented',    
                '14': 'skin_wrinkly',  
                #Rare
                '5': 'skin_scars', 
                '6': 'skin_normal', 
                '15': 'skin_normal',   
                '16': 'skin_normal',  
                #SuperRare
                '4': 'skin_scars', 
                '17': 'skin_normal',      
                #UberRare                
                '3': 'skin_silky', 
                '18': 'skin_clear',                                                                                   
                },                 
        },   
                        
    }

    data_hair_list = {
        'male': {
            'junior': {
                #Common  
                '9': 'hair_soft', 
                '10': 'hair_soft', 
                '11': 'hair_shiny',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_shiny', 
                '8': 'hair_soft', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_dry', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_greasy',           
                }, 
            'adolescent': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_shiny', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_greasy', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_coarse', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_normal', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_normal', 
                '18': 'hair_normal',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'hair_coarse', 
                '10': 'hair_greasy', 
                '11': 'hair_dry',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_shiny', 
                '8': 'hair_normal', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_normal', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_soft', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_soft', 
                '18': 'hair_normal',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'hair_greasy', 
                '10': 'hair_dry', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_coarse', 
                '8': 'hair_normal', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_normal', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_soft', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_shiny', 
                '18': 'hair_normal',                                                                                   
                },                 
        },
        
        'female': {
            'junior': {
                #Common  
                '9': 'hair_soft', 
                '10': 'hair_shiny', 
                '11': 'hair_soft',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_shiny', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_soft', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_greasy',           
                }, 
            'adolescent': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_shiny', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_greasy', 
                '13': 'hair_shiny',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_soft', 
                '6': 'hair_coarse', 
                '15': 'hair_shiny',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_normal', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_normal', 
                '18': 'hair_normal',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_greasy', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_shiny', 
                '8': 'hair_soft', 
                '13': 'hair_greasy',    
                '14': 'hair_dry',  
                #Rare
                '5': 'hair_shiny', 
                '6': 'hair_coarse', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_greasy',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_coarse',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'hair_greasy', 
                '10': 'hair_dry', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_coarse', 
                '8': 'hair_greasy', 
                '13': 'hair_dry',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_normal', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_soft', 
                '17': 'hair_soft',      
                #UberRare                
                '3': 'hair_shiny', 
                '18': 'hair_shiny',                                                                                   
                },                 
        },        

        'shemale': {
            'junior': {
                #Common  
                '9': 'hair_soft', 
                '10': 'hair_shiny', 
                '11': 'hair_soft',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_shiny', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_soft', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_greasy',           
                }, 
            'adolescent': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_shiny', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_greasy', 
                '13': 'hair_shiny',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_soft', 
                '6': 'hair_coarse', 
                '15': 'hair_shiny',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_normal', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_normal', 
                '18': 'hair_normal',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_greasy', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_shiny', 
                '8': 'hair_soft', 
                '13': 'hair_greasy',    
                '14': 'hair_dry',  
                #Rare
                '5': 'hair_shiny', 
                '6': 'hair_coarse', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_greasy',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_coarse',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'hair_greasy', 
                '10': 'hair_dry', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_coarse', 
                '8': 'hair_greasy', 
                '13': 'hair_dry',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_normal', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_soft', 
                '17': 'hair_soft',      
                #UberRare                
                '3': 'hair_shiny', 
                '18': 'hair_shiny',                                                                                   
                },                 
        },        

        'sexless': {
            'junior': {
                #Common  
                '9': 'hair_soft', 
                '10': 'hair_shiny', 
                '11': 'hair_soft',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_shiny', 
                '13': 'hair_normal',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_soft', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_greasy',           
                }, 
            'adolescent': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_shiny', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_soft', 
                '8': 'hair_greasy', 
                '13': 'hair_shiny',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_soft', 
                '6': 'hair_coarse', 
                '15': 'hair_shiny',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_normal', 
                '17': 'hair_normal',      
                #UberRare                
                '3': 'hair_normal', 
                '18': 'hair_normal',                                                                                    
                }, 
            'mature': {
                #Common  
                '9': 'hair_dry', 
                '10': 'hair_greasy', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_shiny', 
                '8': 'hair_soft', 
                '13': 'hair_greasy',    
                '14': 'hair_dry',  
                #Rare
                '5': 'hair_shiny', 
                '6': 'hair_coarse', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_dry', 
                '17': 'hair_greasy',      
                #UberRare                
                '3': 'hair_coarse', 
                '18': 'hair_coarse',                                                                                  
                }, 
            'elder': {
                #Common  
                '9': 'hair_greasy', 
                '10': 'hair_dry', 
                '11': 'hair_normal',                                                                                 
                '12': 'hair_normal',  
                #Uncommon 
                '7': 'hair_coarse', 
                '8': 'hair_greasy', 
                '13': 'hair_dry',    
                '14': 'hair_normal',  
                #Rare
                '5': 'hair_normal', 
                '6': 'hair_normal', 
                '15': 'hair_normal',   
                '16': 'hair_normal',  
                #SuperRare
                '4': 'hair_soft', 
                '17': 'hair_soft',      
                #UberRare                
                '3': 'hair_shiny', 
                '18': 'hair_shiny',                                                                                   
                },                 
        },        
                        
    }

    data_constitution_list = {
                #Common  
                '9': 'normal', 
                '10': 'normal', 
                '11': 'normal',                                                                                 
                '12': 'normal',  
                #Uncommon 
                '7': 'lean', 
                '8': 'brawny', 
                '13': 'athletic',    
                '14': 'normal',  
                #Rare
                '5': 'large', 
                '6': 'small', 
                '15': 'lean',   
                '16': 'brawny',  
                #SuperRare
                '4': 'clumsy', 
                '17': 'athletic',      
                #UberRare                
                '3': 'crooked', 
                '18': 'athletic',           
                }

    data_spirit_list = {
                #Common  
                '9': None, 
                '10': None, 
                '11': None,                                                                                 
                '12': None,  
                #Uncommon 
                '7': 'shy', 
                '8': None, 
                '13': None,    
                '14': 'brave',  
                #Rare
                '5': 'shy', 
                '6': None, 
                '15': None,   
                '16': 'brave',  
                #SuperRare
                '4': 'shy', 
                '17': 'brave',      
                #UberRare                
                '3': 'shy', 
                '18': 'brave',           
                }

    data_mind_list = {
                #Common  
                '9': None, 
                '10': None, 
                '11': None,                                                                                 
                '12': None,  
                #Uncommon 
                '7': 'smart', 
                '8': None, 
                '13': None,    
                '14': 'dumb',  
                #Rare
                '5': 'smart', 
                '6': None, 
                '15': None,   
                '16': 'dumb',  
                #SuperRare
                '4': 'smart', 
                '17': 'dumb',      
                #UberRare                
                '3': 'smart', 
                '18': 'dumb',           
                }
                                                                
    def add_random_feature_plain(person, list):
        
        #get gauss 3-18 range
        roll = str(randint(1, 6) + randint(1, 6) + randint(1, 6))
        if feature: 
            feature = list[roll]
            person.add_feature(feature)
        
        return
                        
    def add_random_feature_genderage(person, list):
        
        #get gauss 3-18 range
        roll = str(randint(1, 6) + randint(1, 6) + randint(1, 6))
        feature = list[person.gender][person.age][roll]
        person.add_feature(feature)
        
        return
        
    def add_features_common(person):
        add_random_feature_genderage(person, data_appearence_list)
        add_random_feature_genderage(person, data_voice_list)
        add_random_feature_genderage(person, data_hair_list)
        add_random_feature_genderage(person, data_skin_list)
        
        return
