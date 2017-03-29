## Major house servitude quest

label lbl_edge_hiring:
    edge_recruiter 'You can apply to become a Major House bond servitor in the city, but you have only one try to do so. Choose wisely.'
    $ core.quest_tracker.add_quest(Quest(**quests_data['edge_bond_quest']))
    menu:
        'Are you interested?'
        "Tell me more":
            call lbl_edge_bond_options 
        'Not today':
            pass
        'I want to be a free citisen':
            call lbl_edge_citisen_briefing

        'Mistmarine':
            
            call lbl_edge_mistmarine
        'Concubine': 
            
            call lbl_edge_sexy_exam            
        'Clerk': 
            
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

    return

label lbl_edge_bond_options:
    python:     
        options = CardsMaker()
        options.add_entry('bond_mistmarine', edge_option_cards['bond_mistmarine'])
        options.add_entry('bond_concubine', edge_option_cards['bond_concubine'])
        options.add_entry('bond_clerk', edge_option_cards['bond_clerk'])
        options.add_entry('bond_builder', edge_option_cards['bond_builder'])
        options.add_entry('bond_servant', edge_option_cards['bond_servant'])
        options.add_entry('bond_host', edge_option_cards['bond_host'])        
        options.add_entry('nevermind', edge_option_cards['nevermind'])  
        CardMenu(options.run()).show()    

    hide card
    return

label lbl_edge_citisen_briefing:
    edge_recruiter "So... It's possible, but will cost you dearly. In order to become a [edge_sovereign.name] libertine you must prove yourself worthy."
    edge_recruiter "Firts of all you need a garantor - someone of [edge_sovereign.name], who will stand bail for you."
    edge_recruiter "Debt and poverty is not an option for a free person in Rome, so you must have some financial security in advance. Bundle of banknotes will do."    
    edge_recruiter "And above all, you need to pay a price for Ascension. One hundred Sparks of Creation. Having no phoenix you cannot bear Sparks in your soul, so get a sparkgem and fill it."  
    edge_recruiter "You also will have a right to get one, and only one slave with you in Ethernal Rome. It isn't neccesary but convinient."  
    edge_recruiter "Slums are teeming with thieves, so I can save a sparkgem and banknotes for you. Just bring them to me if you whant."     
    edge_recruiter "Questions?"
    player "No. I'll be back."
    $ core.quest_tracker.add_quest(Quest(**quests_data['edge_citisen_quest']))
        
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
    $ fate = 'mistmarine'
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
    $ fight = SimpleFight(allies, enemies)           

    jump game_over
    return

label lbl_edge_sexy_exam:
    $ fate = 'concubine'
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

label lbl_edge_bond_clerk:
    $ fate = 'clerk'
    call lbl_edge_skill_exam('mind')

    return

label lbl_edge_bond_clerk:
    $ fate = 'clerk'
    call lbl_edge_skill_exam('mind')

    return

label lbl_edge_bond_clerk:
    $ fate = 'clerk'
    call lbl_edge_skill_exam('mind')

    return

label lbl_edge_bond_clerk:
    $ fate = 'clerk'
    call lbl_edge_skill_exam('mind')

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
