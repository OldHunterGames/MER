# MER main RenPy script

init -10 python:
    sys.path.append(renpy.loader.transfn("scripts"))
    sys.path.append(renpy.loader.transfn("scripts/person"))
    sys.path.append(renpy.loader.transfn("Core"))
    from mer_core import *
    from mer_item import *
    from mer_person import *
    from mer_stock import *
    from mer_metric import *      
    from mer_event import *
    from mer_metaperson import *
    
init python:
    outer_worlds = []
    renpy.block_rollback()
    register_actions()

# The game starts here.
label start:
    python:
        discovered_worlds = []
        core = MistsOfEternalRome()
        set_event_game_ref(core)
        player = gen_random_person('human')
        testperson = Person()
        testperson.add_item(gen_item('weapon', 'simple_axe'))
        player.add_item(gen_item('weapon', 'simple_axe'))
        player.add_item(gen_item('armor', 'bad_plate'))
        player.add_item(gen_item('weapon', 'simple_dagger'))
        core.set_player(player)
        core.protagonist.sparks = 250
        meter = Meter(core.protagonist)
        ap = player.ap
        player.set_resources_storage(core.resources)

    
    show expression "interface/bg_base.jpg" as bg
    call evn_init
    call lbl_edge_main
    
    return
    
label choose_action:
    "You have [core.protagonist.sparks] sparks left. You need to pay [core.protagonist.allowance] sparks this decade to a major House. Mood: [player.mood]. Actions left: [ap]"    
    $ loc_to_call = "choose_acton"
    $ world_to_go = None
    menu:
        "Visit discovered world" if discovered_worlds:
            python:
                items = [(i.name, i) for i in discovered_worlds if hasattr(i, 'name')]
                items.append(("Don't go anywhere", "choose_acton"))
                world_to_go = renpy.display_menu(items)
                if isinstance(world_to_go, str):
                    loc_to_call = world_to_go
                else:
                    loc_to_call = world_to_go.point_of_arrival
        "Discover new world" if outer_worlds:
            $ loc_to_call = core.discover_world(outer_worlds)
        "Relax":
            $ loc_to_call = "end_turn"
        "finish":
            jump end_turn
    jump choose_action

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
    
label end_turn:
    if 'dead' in player.features:
        'you dead = GAME OVER'
        $ renpy.full_restart
        
    $ core.new_turn()
    call new_turn
    return
    
label new_turn:
    call choose_action
    return
    
label game_over:
    "Game Over!"
    $ renpy.full_restart()

screen sc_choose_item(person, item_type, slot, storage=None):
    python:
        item_list = [item for item in person.items if item.type == item_type and not item.equiped]
    vbox:
        for i in item_list:
            textbutton i.name action [Function(person.equip_item, i, slot), Return()]
        textbutton 'disarm' action [Function(person.equip_item, None, slot), Return()]
init python:
    class TradeInput(InputValue):
        def __init__(self):
            self.txt = self.get_text()
        def get_text(self):
            return '1'
        def set_text(self, s):
            self.txt = s

init python:
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
        $ total_player = sum([int(value) for key, value in trade_player.items() if key != 'money'])*100+trade_player['money']
        $ total_trader = sum([int(value) for key, value in trade_trader.items() if key != 'money'])*100+trade_trader['money']
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

        
    
