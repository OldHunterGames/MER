init -1 python:
    sys.path.append(renpy.loader.transfn("Core/DuelEngine/scripts"))
    import random as rand

    from duel_engine import DuelAction
    
    def clinch_special(card):
        user = card.current_fighter
        battle_points = [value['maneuver'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    
    def clinch_remove(card):
        user = card.current_fighter
        battle_points = [value['maneuver'] for value in user.fight.points.values()]
        make_active(battle_points)
    
    def hit_n_run_special(card):
        user = card.current_fighter
        battle_points = [value['onslaught'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    
    def hit_n_run_remove(card):
        user = card.current_fighter
        battle_points = [value['onslaught'] for value in user.fight.points.values()]
        make_active(battle_points)
    
    def rage_special(card):
        user = card.current_fighter
        battle_points = [value['fortitude'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    
    def rage_remove(card):
        user = card.current_fighter
        battle_points = [value['fortitude'] for value in user.fight.points.values()]
        make_active(battle_points)


    def outsmart_special(card):
        user = card.current_fighter
        for action in user.fight.persistent_actions:
            action.remove()
        user.fight.persistent_actions = []
        
    def fallback_special(card):
        user = card.current_fighter
        if len(user.drop) < 1:
            return
        value = 0
        point_to_decrease = None
        for point in user.fight.points[user.side].values():
            if point.value > value:
                value = point.value
                point_to_decrease = point
        if point_to_decrease != None:
            point_to_decrease.value -= user.escalation
        if user.side == 'allies':
            card = subscreen_call('draw_from_drop', card, user=user, text='draw_card')
            user.draw_from_drop(card)
        else:
            max_ = 0
            card_to_get = None
            for card in user.drop:
                if card.power > max_:
                    card_to_get = card
                    max_ = card.power
            user.draw_from_drop(card_to_get)

    def deescalation_special(card):
        user = card.current_fighter
        escalation = user.escalation
        points = user.fight.points[user.side]
        for i in points.values():
            if i.value > escalation:
                i.value -= escalation
        user.escalation = 0
        card.escalation = 0

    def iniciative_special(card):
        user = card.current_fighter
        names = ['maneuver', 'onslaught', 'fortitude', 'excellence']
        multiplier_name = 'iniciative'
        for i in user.fight.points[user.side]:
            i.remove_multiplier('iniciative')
        if user.side == 'allies':
            slot = subscreen_call('sc_chose_slot', card, user=user, names=names)
            set_multiplier(card, slot, multiplier_name)
        else:
            points = slot_chosing(card, names)
            set_multiplier(card, points, multiplier_name)

    
    
    #special mechanincs
    def reckless(card):
        user = card.current_fighter
        fight = user.fight
        side = fight.get_enemy_side(user.side)
        if card.rarity != 'exceptional':
            card.power += 5
            slot = 'excellence'
        else:
            slot = card.slot
        fight.points[side][slot].value += card.power
        card.set_power(0)

    def advantage(card):
        user = card.current_fighter
        user.draw(2)

    def combo(card):
        user = card.current_fighter
        if len(user.draw_list()) < 1:
            return
        if user.side == 'allies':
            card = subscreen_call('draw_from_drop', card, user, 'use_card')
            user.use_from_drop(card)
        else:
            max_ = 0
            card_to_get = None
            for card in user.draw_list():
                if card.power > max_:
                    card_to_get = card
                    max_ = card.power
            user.use_from_drop(card_to_get)

    def amplifiction(card):
        user = card.current_fighter
        fight = user.fight
        points = fight.points[user.side][card.slot]
        points.add_multiplier('amplifiction')

    def amplify(card):
        user = card.current_fighter
        fight = user.fight
        points = fight.points[user.side][card.slot]
        points.value += points.value

    def sequence(card):
        try:
            if card.sequence:
                return
        except AttributeError:
            pass
        user = card.current_fighter
        hand = user.hand
        cards = [i for i in hand.get_all_cards() if i.tag == card.tag and card.tag is not None]   
        
        card.sequence = True
        for i in cards:
            i.sequence = False
            if not i.sequence:
                i.sequence = True
                i.use()
        for i in cards:
            i.sequence = False
        card.sequence = False


    def counterstrike(card):
        user = card.current_fighter
        names = ['onslaught', 'fortitude']
        if user.side == 'allies':
            slot = subscreen_call('sc_chose_slot', card, user=user, names=names)
            user.fight.points[user.side][slot].value += card.power
        else:
            points = slot_chosing(card, names)
            

    def footwork(card):
        user = card.current_fighter
        names = ['maneuver', 'fortitude']
        if user.side == 'allies':
            slot = subscreen_call('sc_chose_slot', card, user=user, names=names)
            user.fight.points[user.side][slot].value += card.power
        else:
            points = slot_chosing(card, names)
            points = user.fight.points[user.side][points]
            points.value += card.power

    def outflank(card):
        user = card.current_fighter
        names = ['maneuver', 'onslaught']
        if user.side == 'allies':
            slot = subscreen_call('sc_chose_slot', card, user=user, names=names)
            user.fight.points[user.side][slot].value += card.power
        else:
            points = slot_chosing(card, names)
            points = user.fight.points[user.side][points]
            points.value += card.power

    def versatile(card):
        user = card.current_fighter
        names = ['maneuver', 'onslaught', 'fortitude']
        if user.side == 'allies':
            slot = subscreen_call('sc_chose_slot', card, user=user, names=names)
            user.fight.points[user.side][slot].value += card.power
        else:
            points = slot_chosing(card, names)
            points = user.fight.points[user.side][points]
            points.value += card.power

    def pressing(card):
        user = card.current_fighter
        escalation = user.escalation
        points = user.fight.points[user.side]
        points_value = [i.value for k, i in points.items() if k != 'excellence']
        max_slot = max(points_value)
        max_point = points.values()[points_value.index(max_slot)]
        if escalation < max_slot:
            max_point.value -= escalation
        points['excellence'].value += escalation+2

    def tactical(card):
        user = card.current_fighter
        if user.side == 'allies':
            drop_list = subscreen_call('sc_chose_drop', card, user=user)
            for i in drop_list:
                user.drop_card(i)
        else:
            for i in range(2):
                card = None
                try:
                    card = rand.choice(user.hand.cards_list)
                except IndexError:
                    break
                if card is not None:
                    user.drop_card(card)
        user.draw(2)

    def fatigue(card):
        user = card.current_fighter
        fight = user.fight
        points = fight.points
        fighters = [fight.current_ally, fight.current_enemy]
        escalation = fighters[0].escalation
        if escalation > fighters[1].escalation:
            fighters.remove(fighters[1])
        elif escalation < fighters[1].escalation:
            fighters.remove(fighters[0])
        for i in fighters:
            value = 0
            point = None
            current_points = points[i.side]
            for n in current_points:
                if n.value > value:
                    value = n.value
                    point = n
            n -= i.escalation



    #power mods
    def buildup(card):
        user = card.current_fighter
        value = len([i for i in user.drop if i.power > 0])
        return value

    def aggravating(card):
        user = card.current_fighter
        points = fight.points[user.side][card.slot]
        value = 0
        for i in user.drop:
            if i.id == card.id:
                value += i.power
        return value


    special_mechanics = {
        'card_draw':[combo, advantage, tactical],
        'eval_early': [reckless],
        'eval_last': [sequence],
    }
    #utility functions
    def use_slot(card, slot):
        user = card.current_fighter
        points = user.fight.points[user.side][slot]
        points.value += card.power
    
    def slot_chosing(card, names):
        user = card.current_fighter
        active_points = []
        for i in names:
            if user.fight.points[user.side][i].active:
                active_points.append(i)
        try:
            choosed = active_points[0]
            multi = user.fight.points[user.side][choosed].multiplier()
        except IndexError:
            return rand.choice(names)
        if len(active_points) < 2:
            return choosed 
        for i in active_points:
            points = user.fight.points[user.side][i]
            if points.multiplier > multi:
                choosed = i
        return choosed

    def set_multiplier(card, slot, multiplier_name):
        user = card.current_fighter
        points = user.fight.points[user.side][slot]
        points.add_multiplier(multiplier_name)

    def make_inactive(battlepoints_list):
        for point in battlepoints_list:
            point.active = False
    
    def make_active(battlepoints_list):
        for point in battlepoints_list:
            point.active = True
    
    def subscreen_call(screen_name, *args, **kwargs):
        return renpy.call_in_new_context('utility_subscreen_glue', screen_name, *args, **kwargs)


    
    # available keys for actions
    # {id: name, rarity, power=0, use_weapon=False, mighty=False, slot=None, special_effect=None, unique=False, style=None}
    # slot is one of 'onslaught', 'maneuver', 'fortitude', 'excellence'
    # special_effect must be function which take 1 arg, excepted arg is DuelCombatant who used card
    # style is one of 'breter', 'juggernaut', 'shieldbearer', 'restler', 'beast'

screen draw_from_drop(card, user, text):
    modal True
    
    vbox:
        align(0.6, 0.7)
        text '%s:'%text
        for c in user.draw_list():
            textbutton c.name:
                action Return(c)

screen sc_chose_slot(card, user, names):
    modal True
    vbox:
        align(0.6, 0.7)
        for name in names:
            textbutton name:
                action Return(name)

init python:
    sc_chose_drop_dropped = []
    def make_empty(list_):
        copy = [i for i in list_]
        for i in copy:
            try:
                list_.remove(i)
            except ValueError:
                pass
screen sc_chose_drop(card, user):
    modal True
    $ drop_list = sc_chose_drop_dropped
    vbox:
        align(0.6, 0.7)
        text 'drop card'
        for i in user.hand:
            textbutton i.name:
                selected (i in drop_list)
                action [If(i in drop_list, true=RemoveFromSet(drop_list, i), false=AddToSet(drop_list, i)),
                        SensitiveIf(len(drop_list) < 2 or i in drop_list)]
        textbutton 'Done':
            action [SensitiveIf(len(drop_list) > 1), Return(drop_list), Function(make_empty, drop_list)]

screen sc_duel_blocker:
    python:
        img = im.MatrixColor('interface/bg_base.jpg', im.matrix.opacity(0.2))
    modal True
    image img

screen sc_placeholder(screen_name, card, *args, **kwargs):
    use duel_battle(card.current_fighter.fight)
    $ renpy.show_screen('sc_duel_blocker')
    $ renpy.show_screen(screen_name, card, *args, **kwargs)

label utility_subscreen_glue(screen_name, card, *args, **kwargs):
    $ value = renpy.call_screen('sc_placeholder', screen_name, card, *args, **kwargs)
    return value
