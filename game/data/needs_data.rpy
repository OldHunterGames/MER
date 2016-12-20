## Needs data

init python:

    needs = {
        ## basic needs that all character have. "relief" intensity fixed at 1, "general" at 2, "purporse" at 3
        "relief": {'name': __('Relief')}, 
        "general": {'name': __('General')}, 
        'purpose': {'name': __('Purpose')},  
        
        ## Genreal needs
        "nutrition": {'name': __('nutrition')}, 
        "wellness": {'name': __('wellness')},
        "comfort": {'name': __('comfort')},
        "activity": {'name': __('activity')},
        "communication": {'name': __('communication')}, 
        "amusement": {'name': __('amusement')}, 
        "prosperity": {'name': __('prosperity')}, 
        "authority": {'name': __('authority')}, 
        "ambition": {'name': __('ambition')}, 
        "eros": {'name': __('eros')},
               
        ## Alugnment-based needs 
        "order": {'name': __('order')}, 
        "independence": {'name': __('independence')}, 
        "approval": {'name': __('approval')}, 
        "thrill": {'name': __('thrill')}, 
        "altruism": {'name': __('altruism')}, 
        "power": {'name': __('power')}
        }
