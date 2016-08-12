init python:
    sys.path.append(renpy.loader.transfn("Core/DuelEngine/scripts"))
    from duel_engine import DuelAction
    def make_inactive(battlepoints_list):
        for point in battlepoints_list:
            point.active = False
    def clinch_special(user):
        battle_points = [value['maneuver'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    def hit_n_run_special(user):
        battle_points = [value['onslaught'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    def rage_special(user):
        battle_points = [value['fortitude'] for value in user.fight.points.values()]
        make_inactive(battle_points)
    def outsmart_special(user):
        for value in user.fight.points.values():
            for i in value.values():
                i.active = True
    def fallback_special(user):
        value = 0
        point_to_decrease = None
        for point in user.fight.points[user.side].values():
            if point.value > value:
                value = point.value
                point_to_decrease = point
        if point_to_decrease != None:
            point_to_decrease.value -= user.escalation
        card = renpy.call_screen('draw_From_drop', user)
        user.draw_from_drop(card)

    clinch = DuelAction('clinch', 'clinch', 'common', 0, special_effect=clinch_special)
    hit_n_run = DuelAction('hit_n_run', 'hit-n-run', 'common', 0, special_effect=hit_n_run_special)
    rage = DuelAction('rage', 'rage', 'common', 0, special_effect=rage_special)
    outsmart = DuelAction('outsmart', 'outsmart', 'common', 0, special_effect=outsmart_special)
    fallback = DuelAction('fallback', 'fallback', 'common', 0, special_effect=fallback_special)
    test1 = DuelAction('test1', 'test', 'common', 2, slot='onslaught')
    actions_lib = [test1, clinch, hit_n_run, rage, outsmart, fallback]