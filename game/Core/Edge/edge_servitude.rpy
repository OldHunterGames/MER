## Major house servitude quest

label lbl_edge_hiring:
    'You can apply to become a Major House servitor in the city, but you have only one try to do so. Choose wisely.'
    menu:
        'What kind of job to choose?'
        'Mistmarine': 
            call lbl_edge_mistmarine
            
        'Concubine': 
            call lbl_edge_sexy_exam('charisma') 
        'Stripper': 
            call lbl_edge_sexy_exam('expression') 
        'Sexy maid': 
            call lbl_edge_sexy_exam('housekeeping') 
        'Sexy secretary': 
            call lbl_edge_sexy_exam('management')
        'Sexy nurse': 
            call lbl_edge_sexy_exam('alchemy')
            
        'Scholar': 
            call lbl_edge_skill_exam('scholarship')
        'Artisan': 
            call lbl_edge_skill_exam('craft')   
        'Repairperson': 
            call lbl_edge_skill_exam('mechanics')
        'System integrator': 
            call lbl_edge_skill_exam('electronics')                                                            
        'Not today':
            call lbl_edge_outpost(location)

    return

label lbl_edge_mistmarine:
    'FIGHT'
    python:
        def generate_warrior(genus):
            ocpn = choice(['mercenary', 'sellsword', 'gladiator', 'thug', 'raider', 'soldier', 'pirate', 'officer', 'knight', 'assasin'])
            
            return gen_random_person(genus=gns, occupation=ocpn)
            
        allies = [player]
        for i in range(3):
            allies.append(generate_warrior(human))
        enemies = []
        for i in range(4):
            enemies.append(generate_warrior(human))        
        
    call lbl_simple_fight(allies, enemies)

    jump game_over
    return

label lbl_edge_sexy_check(skill):
    'PLACEHOLDER'
    call lbl_edge_outpost(location)
    return

label lbl_edge_sexy_check(skill):
    'PLACEHOLDER'
    call lbl_edge_outpost(location)
    return
