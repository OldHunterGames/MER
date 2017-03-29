init python:
    maneuvers_data = {
        'swift_strike': {'name': __('Swift strike'), 'description': __('Double damage vs dodge. \n Target:')},  
        'direct_strike': {'name': __('Direct strike'), 'description': __('Double damage vs attacking enemy. \n Target:')},  
        'heavy_strike': {'name': __('Heavy strike'), 'description': __('Double damage vs block. \n Target:')},  
        'wide_strike': {'name': __('Wide strike'), 'description': __('Targets all enemies. Gives power up to those who have managed to defend')},  
        'dodge': {'name': __('Dodge'), 'description': __('Dodge all attacks exept "Swift strike". Get power up if "Heavy strike" is dodged.')},  
        'block': {'name': __('Block'), 'description': __('Block all attacks exept "Heavy strike". Get power up if "Swift strike" is bloked.')},  
        'shield_up': {'name': __('Shield up'), 'description': __('Deflect all attacks. Get some deffence (receive the greater the greater the lack of). Give power up to each opponent whom attack is deflected.')},  
        'backstab': {'name': __('Backstab'), 'description': __('Ignores protection. Double damage to HP.')},  
        'parry': {'name': __('Parry'), 'description': __('Deflect one attack, and if attack is deflected givs a power up.')},  
        'power_strike': {'name': __('Power strike'), 'description': __('Triple damage.')},  
        'grapple': {'name': __('Grapple'), 'description': __('Opponent skips his action.')},  
        'pin_down': {'name': __('Pin Down'), 'description': __('Win the fight.')},  
        'flee': {'name': __('Flee'), 'description': __('Get out from the fight.')},  
        'outflank': {'name': __('Outflank'), 'description': __('Deflect first enemy attack. If no damage recived get power up.')},  
        'tank': {'name': __('Tank'), 'description': __('Half damage this round. All attacks aimed at you and only you (even "wide strikes").')},  
    }

    combat_styles_translation = {
    'brawler': __("brawler"),
    'cutthroat': __("cutthroat"),
    'swashbuckler': __("swashbuclker"),
    'shieldbearer': __("shieldbearer"),
    'wrecker': __("wrecker"),
    }

    combat_weight = {
        'heavy': __("heavy"),
        'mobile': __('mobile')
    }