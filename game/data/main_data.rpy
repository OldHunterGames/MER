init python:

    house_names = {'kamira': __('Kamira'),
                 'serpis': __('Serpis'), 
                 'corvus': __('Corvus'),
                 'taurus':  __('Taurus')}
    
    spending_rate = [__('unaffordable'), __('expensive'), __('substantial'), __('minor'), __('negligible'), __('free')]
    favor_rate = [__('disregarded'), __('minor'), __('notable'), __('substantial'), __('pressing'), __('outrageous')]
    success_rate = [__('failure'), __('minimum'), __('adequate'), __('good'), __('great'), __('excellent')]

    food_quality_dict = {-1: __("disgusting "),
                         0: __('forage '),
                         1: __('adequate '),
                         2: __('gustable '),
                         3: __('tasty '),
                         4: __('delicious '),
    }

    food_amount_dict = {0: __('starving'),
                        1: __('underfeed'),
                        2: __(''),
                        3: __('overfeed')
    }
    
    show_resource = [
        __('no resources'), 
        __('a few resources'), 
        __('some resources'), 
        __('considerable resources'), 
        __('plenty of resources'), 
        __('all resources you can handle'), 
        ]
    
    show_favor = [
        __('no favor'), 
        __('a few favor'), 
        __('some favor'), 
        __('considerable favor'), 
        __('great favor'), 
        __('total trust'), 
        ]    
        
    #Houses
    major_names = {
    'vatican': __('Holy Vatican'), 
    'serpis': __('House Serpis'), 
    'pardus': __('House Pardus'), 
    'kamira': __('House Kamira'), 
    'corvus': __('House Corvus'),             
    }
    
    #Relations
    relations_name = {
        -1: {
            'neutral': __('insolent'),
            'hostile': __('agressive'),
            'friendly': __('nagging'),
            'slave': __('rebellious'),      
            'master': __('cruel'),                                          
        }, 
        0: {
            'neutral': __('prudent'),
            'hostile': __('cautious'),
            'friendly': __('fellow'),
            'slave': __('forced'),      
            'master': __('oppressive'),                                          
        }, 
        1: {
            'neutral': __('cooperative'),
            'hostile': __('frightful'),
            'friendly': __('friend'),
            'slave': __('accustomed'),      
            'master': __('rightful'),                                          
        },
        ## По умолчанию, реально даём название в зависимости от типа преданности 
        2: {
            'neutral': __('thrustworthy'),
            'hostile': __('humble'),
            'friendly': __('charmed'),
            'slave': __('wishing'),      
            'master': __('patron'),                                          
        },                         
    }
