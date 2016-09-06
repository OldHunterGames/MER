init python:
    exchange_rates = {
    'drugs': 100,
    'provision': 100,
    'fuel': 100,
    'munition': 100,
    'hardware': 100,
    'clothes': 100
    }
    class TradeInput(InputValue):
        def __init__(self):
            self.txt = self.get_text()
        def get_text(self):
            return '1'
        def set_text(self, s):
            self.txt = s
    res_input = None
    show_input = False
    input_who = None
    timer_on = False
    uv_trade_input = TradeInput()
    universal_trade_values = {'player': collections.defaultdict(int), 'trader': collections.defaultdict(int)}
    def universal_trade_values_refresh():
        return {'player': collections.defaultdict(int), 'trader': collections.defaultdict(int)}
    def trade_timer(res, dict_, who, value):
        if res != None and who != None and value != None:
            if who == 'player':
                dict_[who][res] = str(min(int(value.txt), getattr(core.resources, res)))
            else:
                dict_[who][res] = int(value.txt)
    def deal_trade(dict_):
        for key in core.resources.resources.keys():
            value = int(dict_['trader'][key]) - int(dict_['player'][key])
            value = getattr(core.resources , key) + value
            setattr(core.resources, key, value)
        value = int(dict_['trader']['money']) - int(dict_['player']['money'])
        value = getattr(core.resources , 'money') + value
        setattr(core.resources, 'money', value)

screen sc_universal_trade(player=core.player, trader=None):
    python:
        
        trade_player = universal_trade_values['player']
        trade_trader = universal_trade_values['trader']
    vbox:
        align(0.0, 0.0)
        for k, v in core.resources.resources.items():
            textbutton '[k]([v])':
                action [SetVariable('show_input', True), SetVariable('res_input', k), SetVariable('input_who', 'player'),
                        SensitiveIf(v>0)]
        textbutton 'money([core.resources.money])':
            action [SetVariable('show_input', True), SetVariable('res_input', 'money'), SetVariable('input_who', 'player'),
                        SensitiveIf(core.resources.money>0)]
    vbox:
        align(0.3, 0.0)
        for i in core.resources.resources.keys():
            $ player_res = trade_player[i]
            $ trader_res = trade_trader[i]
            text '[player_res]  [i]  [trader_res]'
        $ player_money = trade_player['money']
        $ trader_money = trade_trader['money']
        text '[player_money]  money  [trader_money]'
        $ total_player = sum([int(value*exchange_rates[key]) for key, value in trade_player.items() if key != 'money'])+trade_player['money']
        $ total_trader = sum([int(value*exchange_rates[key]) for key, value in trade_trader.items() if key != 'money'])+trade_trader['money']
        $ total_difference = total_trader - total_player
        python:
            if total_player > total_trader:
                should_equalize = 'trader'
            elif total_player < total_trader:
                should_equalize = 'player'
            else:
                should_equalize = None

        text '[total_player] total [total_trader]'
        text ' '
        textbutton 'deal' action[Function(deal_trade, universal_trade_values),
                             SetVariable('universal_trade_values', universal_trade_values_refresh()),
                             SensitiveIf(total_player>=total_trader)]
        textbutton 'leave' action[SetVariable('universal_trade_values', universal_trade_values_refresh()), Return()]
        if should_equalize == 'player':
            textbutton 'equalize with money':
                action[SensitiveIf(core.resources.money >= total_difference), SetDict(trade_player, 'money', total_difference)]
        elif should_equalize == 'trader':
            textbutton 'equalize with money':
                action SetDict(trade_trader, 'money', -total_difference)

    vbox:
        align(0.5, 0.0)
        for i in core.resources.resources.keys():
            textbutton str(i):
                action [SetVariable('show_input', True), SetVariable('res_input', i), SetVariable('input_who', 'trader')]
        textbutton 'money':
            action [SetVariable('show_input', True), SetVariable('res_input', 'money'), SetVariable('input_who', 'trader')]

    if show_input:
        vbox:
            align(0.5, 0.7)
            text '[res_input]'
            input value uv_trade_input
            textbutton 'confirm' action[SetVariable('show_input', False),
                                 Function(trade_timer, res_input, universal_trade_values, input_who, uv_trade_input)]
            if input_who == 'player':
                textbutton 'all in' action[Function(uv_trade_input.set_text, getattr(core.resources, res_input)),SetVariable('show_input', False),
                                     Function(trade_timer, res_input, universal_trade_values, input_who, uv_trade_input)]

        
    
screen sc_person_equipment(person):
    vbox:
        text 'Weapon:'
        for i in person.inventory.weapon_slots():
            python:
                sc_equipment_desc = person.inventory.carried_weapons[i]
                if sc_equipment_desc != None:
                    sc_equipment_desc = i + ': ' + sc_equipment_desc.description
                else:
                    sc_equipment_desc = i
            textbutton sc_equipment_desc:
                action [Show('sc_equip_item', person=person, slot=i),
                        SensitiveIf(person.inventory.is_slot_active(i))]
        text 'Armor:'
        for i in person.inventory.armor_slots():
            python:
                sc_equipment_desc = person.inventory.carried_armor[i]
                if sc_equipment_desc != None:
                    sc_equipment_desc = i + ': ' + sc_equipment_desc.description
                else:
                    sc_equipment_desc = i
            textbutton sc_equipment_desc:
                action [Show('sc_equip_item', person=person, slot=i),
                        SensitiveIf(person.inventory.is_slot_active(i))]
        text ' '
        textbutton 'leave':
            action Hide('sc_person_equipment'), Hide('sc_equip_item'), Return()

screen sc_equip_item(person, slot):
    vbox:
        align(0.0, 0.7)
        text slot + ':'
        for i in person.inventory.available_for_slot(slot):
            textbutton i.description:
                action Function(person.inventory.equip_on_slot, slot, i)
        textbutton 'unequip':
            action Function(person.inventory.equip_on_slot, slot, None)
        textbutton 'leave':
            action Hide('sc_equip_item')

screen sc_prefight_equip(person):
    vbox:
        python:
            if person.main_hand == None:
                prefight_text1 = "main hand"
            else:
                prefight_text1 = "main hand: %s"%person.main_hand.description
            if person.other_hand == None:
                prefight_text2 = 'other hand'
            else:
                prefight_text2 = 'other hand: %s'%person.other_hand.description
        textbutton prefight_text1:
            action [Show('sc_equip_weapon', person=person, hand='main_hand'),
                SensitiveIf(any([weapon for weapon in person.inventory.carried_weapons.values() if weapon != None]) or person.main_hand != None)]
        textbutton prefight_text2:
            action [Show('sc_equip_weapon', person=person, hand='other_hand'),
                SensitiveIf(any([weapon for weapon in person.inventory.carried_weapons.values() if weapon != None]) or person.other_hand != None)]
        textbutton 'Done' action Return()

screen sc_equip_weapon(person, hand):
    vbox:
        align(0.3, 0.3)
        for weapon in person.inventory.carried_weapons.values():
            if weapon != None:
                textbutton weapon.description:
                    action Function(person.equip_weapon, weapon, hand), Hide('sc_equip_weapon')
        textbutton 'unequip' action Function(person.disarm_weapon, hand), Hide('sc_equip_weapon')

screen sc_make_deck(person):
        vbox:
            xalign 0.0
            text 'current deck:'
            for card in person.deck.cards_list:
                textbutton card.name:
                    hovered Show('sc_card_description', card=card)
                    unhovered Hide('sc_card_description')
                    action Function(person.deck.remove_card, card)
        vbox:
            xalign 0.3
            text 'available:'
            for card in person.cards_list:
                if card not in person.deck.cards_list:
                    textbutton card.name:
                        hovered Show('sc_card_description', card=card)
                        unhovered Hide('sc_card_description')
                        action Function(person.deck.add_card, card)
        textbutton 'done':
            xalign 0.6
            action Return()



screen sc_card_description(card):
    text card.show():
        align(0.5, 0.5)


screen sc_faction_info(faction):
    frame:
        hbox:
            vbox:
                text 'Faction: ' + faction.name
                text ' '
                text 'Leaded:'
                text faction.owner.name
                text ' ' 
                text 'faction alignment:'
                text 'morality: ' + faction.owner.alignment.show_morality()
                text 'activity: ' + faction.owner.alignment.show_activity()
                text 'orderliness: ' + faction.owner.alignment.show_orderliness()
                text ' '
                text 'Relations: '
                text 'fervor: ' + player.relations(faction).show_fervor()
                text 'distance: ' + player.relations(faction).show_distance()
                text 'congruence: ' + player.relations(faction).show_congruence()
                text ' '
                text 'Stance:'
                text 'type: ' + str(player.stance(faction).show_type())
                text 'level: ' + str(player.stance(faction).show_stance())
                text ' '
                text 'Harmony: ' + str(player.relations(faction).harmony()[0])
                $ axis = player.relations(faction).show_harmony_axis()
                if len(axis[0]) > 0:
                    text 'harmonized_axis: ' + str(axis[0])
                if len(axis[1]) > 0:
                    text 'bad harmony: ' + str(axis[1])
                text ' '
                textbutton 'leave':
                    action Return()