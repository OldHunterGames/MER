init python:
    jobs_data = {
    'edge_idle': {'name': __('Idle'), 'description': 'EROR'},
    'edge_manual': {'name': __('Manual labor'), 'description': __('doing manual labor in slums')},
    'edge_houseservice': {'name': __('Simple work'), 'description': __('providing household services in the slums')},
    'edge_range': {'name': __('Range the Edge'), 'description': 'EROR'},   
    'edge_beg': {'name': __('Beggar'), 'description': 'EROR'},
    'edge_bukake': {'name': __('Bukake slut'), 'description': 'EROR'},      
    
    'edge_repair': {'name': __('Repairings'), 'description': __('repairs various stuff for slum-dwellers')},
    'edge_entertain': {'name': __('Entertain patrons'), 'description': __('entertains the slum-dwellers')},
    'edge_alchemy': {'name': __('Brew booze'), 'description': __('brew booze for a slum-dwellers')},
    'edge_disassembly': {'name': __('Disassemble wrecks'), 'description': __('disassembles old machinery')},

    'edge_treasurehunt': {'name': __('Treasure hunt'), 'description': __('Descriptext')},
    }   
        
    effort_quality = [encolor_text(__('noting'), 0), 
                            encolor_text(__('a tiny effort'), 1),
                            encolor_text(__('some effort'), 2),
                            encolor_text(__('considerable effort'), 3),
                            encolor_text(__('significant effort'), 4),
                            encolor_text(__('epic effort'), 5),
                            encolor_text(__('impossible effort'), 6)]
                            
    yeld_table = [0, 5, 15, 30, 50, 75]
