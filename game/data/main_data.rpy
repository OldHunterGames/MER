init python:

    house_names = {'kamira': __('Kamira'),
                 'serpis': __('Serpis'), 
                 'corvus': __('Corvus'),
                 'taurus':  __('Taurus')}
    
    spending_rate = [__('unaffordable'), __('expensive'), __('substantial'), __('minor'), __('negligible'), __('free')]
    favor_rate = [__('disregarded'), __('minor'), __('notable'), __('substantial'), __('pressing'), __('outrageous')]

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