## Major house servitude quest


label lbl_edge_outpost:
    edge_recruiter 'You can apply to become a Major House bond servitor in the city, but you have only one try to do so. Choose wisely.'
    $ core.quest_tracker.add_quest(Quest(**quests_data['edge_bond_quest']))
    $ fate = None
    menu:
        'Are you interested?'
        "Tell me more":
            call lbl_edge_bond_options(None) 
        'Not today':
            pass
        'I want to be a free citisen':
            call lbl_edge_citisen_briefing

    return

label lbl_edge_hiring:
    edge_recruiter 'You can apply to become a Major House bond servitor in the city, but you have only one try to do so. Choose wisely.'
    menu:
        'Are you interested?'
        "Tell me more":
            call lbl_edge_bond_options(None) 
        'Not today':
            pass
        'I want to be a free citisen':
            call lbl_edge_citisen_briefing

    return


label lbl_edge_spc_bond_start(card):
    call lbl_edge_hiring

    return

label lbl_edge_spc_citisen_start(card):
    if 'citisen_briefing' in edge.options:
        call lbl_edge_libertine_exam(None)
    else:
        call lbl_edge_citisen_briefing

    return

label lbl_edge_bond_options(card):
    python:     
        options = CardsMaker()
        options.add_entry('bond_mistmarine', edge_option_cards)
        options.add_entry('bond_concubine', edge_option_cards)
        options.add_entry('bond_clerk', edge_option_cards)
        options.add_entry('bond_builder', edge_option_cards)
        options.add_entry('bond_servant', edge_option_cards)
        options.add_entry('bond_host', edge_option_cards)        
        options.add_entry('nevermind', edge_option_cards)  
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
    $ edge.options.append('citisen_briefing')
        
    return
    
label lbl_edge_libertine_exam(card):
    python:
        score = 0
        if 'got_gem' in edge.options:
            score += 1
        if 'got_banknotes' in edge.options:
            score += 1
        if 'got_garantor' in edge.options:
            score += 1
        check_gem = False
        check_notes = False
        for item in player.items:
            if item.id == 'sparkgem':
                check_gem = True
            if item.id == 'notes':
                check_notes = True

    if score > 2:
        $ fate = 'citisen'
        jump lbl_edge_fate

    edge_recruiter "What do you need?"


    menu:
        '[garantor.name] will bail for me!' if 'got_garantor' not in edge.options and garantor:
            $ edge.options.append('got_garantor')
            edge_recruiter "Good for you! Let's settle the formalities."
            
        'I have a sparkgem!' if 'got_gem' not in edge.options and check_gem:
            $ edge.options.append('got_gem')
            python:  
                for item in player.items:
                    if item.id == 'sparkgem':
                        player.remove_item(item)
                        break             
            edge_recruiter "Ouuu... shiny! I'll hold it for you."

        'I have banknotes here!' if 'got_banknotes' not in edge.options and check_notes:
            $ edge.options.append('got_banknotes')
            python:  
                for item in player.items:
                    if item.id == 'notes':
                        player.remove_item(item)
                        break     
            edge_recruiter "Seems legit! I'll hold it for you."


        'Remind me what I need to become a citisen?':
            if 'got_garantor' not in edge.options:
                edge_recruiter 'First and above all, you need a garantor - respected citisen of Eternal Rome who will vouch for you.'
            if 'got_banknotes' not in edge.options:
                edge_recruiter 'You need some money for a first decades. The bundle of banknotes of our Major House will suffice.'
            if 'got_gem' not in edge.options:
                edge_recruiter 'The Rite of Joining requires Sparks of Creation. Bring me a Spark infused gem.'      
            edge_recruiter "Then I will bring you to Eternal Rome."                

        'Newermind':
            return
    
    call lbl_edge_libertine_exam(None)
    return

label lbl_edge_mistmarine(card):
    $ fate = 'mistmarine'
    python:
        def generate_warrior(genus):
            ocpn = choice(['wild_hunter', 'wild_outcast', 'tribal_chief', 'lumberjack', 'assasin', 'knight', 'officer', 'spacemarine', 'mech_pilot', ])
            
            return gen_random_person(genus=genus, occupation=ocpn)
            
        allies = [player]
        for i in range(4):
            allies.append(generate_warrior('human'))
        enemies = []
        for i in range(5):
            enemies.append(generate_warrior('human'))        

    enemies[0] 'Test your might!!!' 
    $ fight = SimpleFight(allies, enemies)      
    if fight.get_winner() == 'allies':
        jump lbl_edge_fate
    else:
        '[player.name] perished in battle.'
        jump game_over
  
    return

label lbl_edge_sexy_exam(card):
    python:
        fate = 'concubine'
        options = CardsMaker(edge_seduce_jury)
        CardMenu(options.run()).show()                    

    hide card

    if result:
        'scuccess'    
        call lbl_edge_fuck_challenge(skill)
    else:
        'fail'
        call lbl_edge_outpost
    
    return

label lbl_edge_sexy_exam_might(card):
    $ result = core.skillcheck(player, 'physique', 3) 
    return

label lbl_edge_sexy_exam_grace(card):
    $ result = core.skillcheck(player, 'agility', 3) 
    return

label lbl_edge_sexy_exam_spirit(card):
    $ result = core.skillcheck(player, 'spirit', 3) 
    return

label lbl_edge_sexy_exam_mind(card):
    $ result = core.skillcheck(player, 'mind', 3) 
    return

label lbl_edge_fuck_challenge(skill):
    $ partner = edge_junker
    #$ partner2 = gen_random_person(genus='human', occupation='stripper', gender='female')
    #$ partner3 = gen_random_person(genus='human', occupation='stripper', gender='female')
    partner "Let's fuck already!"

    $ sex = SimpleSex((player, 'controlled'), (partner, 'wishful'))
    $ result = sex.get_results()
    if result[partner] > 2:
        partner "Oh, baby you soooo hot!"
        edge_recruiter "You hired, [player.name]. Let's settle the formalities"
        jump lbl_edge_fate
    else:
        partner "Meh..."
        edge_recruiter "Thank you. We will call you back. Next!"
    
    return

label lbl_edge_bond_clerk(card):
    $ fate = 'clerk'
    call lbl_edge_skill_exam('mind')

    return

label lbl_edge_bond_builder(card):
    $ fate = 'builder'
    call lbl_edge_skill_exam('physique')

    return

label lbl_edge_bond_servitor(card):
    $ fate = 'servitor'
    call lbl_edge_skill_exam('agility')

    return

label lbl_edge_bond_host(card):
    $ fate = 'host'
    call lbl_edge_skill_exam('spirit')

    return
            
label lbl_edge_skill_exam(skill):
    edge_recruiter 'I will test your skills'
    $ player.moral_action(target=edge_recruiter, activity='timid') 
    $ result = core.skillcheck(player, skill, 5)

    if result > 0:
        edge_recruiter 'You a worthy to serve our great House!'    
        jump lbl_edge_fate
    else:
        edge_recruiter 'No more chances for you!'
        
    return
