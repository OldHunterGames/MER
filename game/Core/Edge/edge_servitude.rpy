## Major house servitude quest

label lbl_edge_hiring:
    edge_recruiter 'You can apply to become a Major House servitor in the city, but you have only one try to do so. Choose wisely.'
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
        'Free citisen':
            call lbl_edge_libertine_briefing
        'Not today':
            pass

    return

label lbl_edge_libertine_briefing:
    edge_recruiter "So... It's possible, but will cost you dearly. In order to become a [edge_sovereign.name] libertine you must prove yourself worthy."
    edge_recruiter "Firts of all you need a garantor - someone of [edge_sovereign.name], who will stand bail for you."
    edge_recruiter "Debt and poverty is not an option for a free person in Rome, so you must have some financial security in advance. Bundle of banknotes will do."    
    edge_recruiter "And above all, you need to pay a price for Ascension. One hundred Sparks of Creation. Having no phoenix you cannot bear Sparks in your soul, so get a sparkgem and fill it."  
    edge_recruiter "You also will have a right to get one, and only one slave with you in Ethernal Rome. It isn't neccesary but convinient."  
    edge_recruiter "Slums are teeming with thieves, so I can save a sparkgem and banknotes for you. Just bring them to me if you whant."     
    edge_recruiter "Questions?"
    player "No. I'll be back."
        
    return
    
label lbl_edge_libertine_exam:
    if 'got_gem' in edge.options:
        jump lbl_edge_libertine_pass
        
    edge_recruiter "What do you need?"
    menu:
        '[garantor.name] will bail for me!' if 'got_garantor' not in edge.options and garantor:
            $ edge.options.append('got_garantor')
            edge_recruiter "Good for you! Let's settle the formalities."
            
        'I have a sparkgem!' if 'got_gem' not in edge.options:
            $ edge.options.append('got_gem')
            
        'I have banknotes here!' if 'got_banknotes' not in edge.options:
            $ edge.options.append('got_banknotes')
                        
        'Newermind':
            jump lbl_edge_places
    
    call lbl_edge_libertine_exam
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
    menu:
        'You need to impress House representatives. What to do?'
        'Show your body. (Might)':
            $ skill = 'physiqye'
        'Dance a stiptease. (Finesse)':
            $ skill = 'agility'
        'Play a doctor. (Wisdom)':
            $ skill = 'mind'
        'Demonstrate a character. (Spirit)':
            $ skill = 'spirit'                            
    python:
        result = core.skillcheck(player, skill, 2)        

    if result:
        'scuccess'    
        call lbl_edge_fuck_challenge(skill)
    else:
        'fail'
        call lbl_edge_outpost
    
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
    $ player.moral_action('timid', 'lawful', edge_recruiter) 
    $ result = core.skillcheck(player, skill, 5)
    
    player '[result]'

    if result:
        'scuccess'    
        jump lbl_edge_fate
    else:
        'fail'
        call lbl_edge_outpost
        
    return
