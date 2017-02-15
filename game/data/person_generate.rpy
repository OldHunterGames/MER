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
    
    def add_random_feature_genderage(person, list):
        
        #get gauss 3-18 range
        roll = str(randint(1, 6) + randint(1, 6) + randint(1, 6))
        feature = list[person.gender][person.age][roll]
        person.add_feature(feature)
        
        return
