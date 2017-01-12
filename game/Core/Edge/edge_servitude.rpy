## Major house servitude quest

label lbl_edge_hiring:
    'You can apply to become a Major House servitor in the city, but you have only one try to do so. Choose wisely.'
    menu:
        'What kind of job to choose?'
        'Mistmarine':
            $ fate = 'mistmarine'
            call lbl_edge_mistmarine
        'Concubine': 
            $ fate = 'concubine'
            call lbl_edge_sexy_exam            
        'Clerk': 
            $ fate = 'clerk'
            call lbl_edge_skill_exam('mind')
        'Builder': 
            $ fate = 'builder'
            call lbl_edge_skill_exam('physique')   
        'Servant': 
            $ fate = 'servant'
            call lbl_edge_skill_exam('agility')
        'Host': 
            $ fate = 'host'
            call lbl_edge_skill_exam('spirit')                                                            
        'Not today':
            pass

    return

label lbl_edge_mistmarine:
    python:
        def generate_warrior(genus):
            ocpn = choice(['outcast', 'pathfinder', 'hunter', 'explorer', 'biker', 'sniper', 'marksman', 'watchman', 'sapper',  'mercenary', 'sellsword', 'gladiator', 'thug', 'raider', 'soldier', 'pirate', 'officer', 'knight', 'assasin'])
            
            return gen_random_person(genus=genus, occupation=ocpn)
            
        allies = [player]
        for i in range(4):
            allies.append(generate_warrior('human'))
        enemies = []
        for i in range(5):
            enemies.append(generate_warrior('human'))        

    enemies[0] 'Test your might!!!'        
    call lbl_simple_fight(allies, enemies)

    jump game_over
    return

label lbl_edge_sexy_exam:
    'Skillcheck [skill]'
    python:
        moral = target.check_moral(['timid', 'lawful'], player)
        result = core.threshold_skillcheck(player, skill, difficulty = 0, tense_needs=['authority', 'independence'], satisfy_needs=['eros', 'order'], beneficiar=player, morality=moral, success_threshold = 1, special_motivators=[])        

    if result[0]:
        'scuccess'    
        call lbl_edge_fuck_challenge(skill)
    else:
        'fail'
        call lbl_edge_outpost(location)
    
    return

label lbl_edge_fuck_challenge(skill):
    $ partner = gen_random_person(genus='human', occupation='slut', gender='female')
    #$ partner2 = gen_random_person(genus='human', occupation='slut', gender='female')
    #$ partner3 = gen_random_person(genus='human', occupation='slut', gender='female')
    partner 'Hi there!'
    $ sex = SexEngine((player, True), [(partner, True)])
    
    call screen sc_sexengine_main(sex)
    
    return

label lbl_edge_skill_exam(skill):
    edge_recruiter 'I will test your skills'
    $ actor.moral_action('timid', 'lawful') 
    $ result = core.skillcheck(player, skill, 5)
    
    player '[result]'

    if result[0]:
        'scuccess'    
        jump lbl_edge_fate
    else:
        'fail'
        call lbl_edge_outpost(location)
        
    return
