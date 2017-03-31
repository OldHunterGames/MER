# -*- coding: UTF-8 -*-
import random
from collections import defaultdict

import renpy.store as store
import renpy.exports as renpy


class SimpleFight(object):

    def __init__(self, allies_list, enemies_list):

        self.allies = [SimpleCombatant(i, self) for i in allies_list]
        self.enemies = [SimpleCombatant(i, self) for i in enemies_list]
        allies_average_skill = sum(
            [i.combat_level for i in self.allies]) / len(self.allies)
        enemies_average_skill = sum(
            [i.combat_level for i in self.enemies]) / len(self.enemies)
        difference = allies_average_skill - enemies_average_skill
        self.selected_ally = self.allies[0]
        self.escalation = 0
        self.fleed = False
        self._log = defaultdict(list)
        self.round = 1
        self.logged_round = 1
        self.ended = False
        if difference < 0:
            for i in self.allies:
                i.skill_difference = difference
            for i in self.enemies:
                i.skill_difference = abs(difference)
        else:
            for i in self.allies:
                i.skill_difference = difference
            for i in self.enemies:
                i.skill_difference = -difference

        for i in self.allies:
            i.type = 'player'
            i.set_enemies([i for i in self.enemies])
        for i in self.enemies:
            i.type = 'npc'
            i.set_enemies([i for i in self.allies])
        self.enemies_turn()
        renpy.call_in_new_context('lbl_simple_fight', self, allies_list)

    def select(self, ally):
        self.selected_ally = ally

    def clear_log(self):
        try:
            del self._log[abs(self.round - self.logged_round - 1)]
        except:
            pass

    def log(self, log):
        self._log[self.round].append(log)

    def get_log(self):
        return self._log

    def combatants(self):
        list_ = [i for i in self.allies]
        list_.extend(self.enemies)
        return list_

    def active_allies(self):
        return [i for i in self.allies if not i.inactive]

    def active_enemies(self):
        return [i for i in self.enemies if not i.inactive]

    def end_turn(self):
        disables = []
        protections = []
        attacks = []
        restores = []
        specials = []
        for i in self.combatants():
            try:
                type_ = i.active_maneuver.type
            except AttributeError:
                continue
            else:
                if type_ == 'protection':
                    protections.append(i.active_maneuver)
                elif type_ == 'attack':
                    attacks.append(i.active_maneuver)
                elif type_ == 'restore':
                    restores.append(i.active_maneuver)
                elif type_ == 'disable':
                    disables.append(i.active_maneuver)
                else:
                    specials.append(i.active_maneuver)

        for i in disables:
            i.activate()
        for i in protections:
            i.activate()
        for i in attacks:
            i.activate()
        for i in restores:
            i.activate()
        for i in specials:
            i.activate()
        self.round += 1
        if self.get_winner() is not None:
            self.ended = True
        self.enemies_turn()

    def enemies_turn(self):
        if abs(self.round - self.logged_round) >= 2:
            self.clear_log()
        self.refresh_enemies()
        for i in self.enemies:
            if i.inactive:
                continue
            try:
                maneuver = random.choice(i.maneuvers)
                if isinstance(maneuver, Tank) and any([isinstance(n.active_maneuver, Tank) for n in i.allies]):
                    i.maneuvers.remove(maneuver)
                    maneuver = random.choice(i.maneuvers)
            except IndexError:
                i.inactive = True
                continue
            else:
                i.active_maneuver = maneuver
                if maneuver.self_targeted:
                    maneuver.add_target(i)
                    continue
                if maneuver.type == 'protection':
                    targets = [i for i in self.active_enemies()]
                    vitalities = [i.vitality() for i in targets]

                elif maneuver.type == 'attack':
                    targets = [i for i in self.active_allies()]
                    vitalities = [i.vitality() for i in targets]

                elif maneuver.type == 'disable':
                    targets = [i for i in self.active_allies()]
                    attacks = [i.attack for i in targets]
                    while maneuver.can_target_more() and len(targets) > 0:
                        attack = min(attacks)
                        index = attacks.index(attack)
                        target = targets.pop(index)
                        attacks.pop(index)
                        maneuver.add_target(target)
                    continue

                elif maneuver.type == 'restore':
                    targets = [i for i in self.active_enemies()]
                    vitalities = [i.vitality() for i in targets]

                elif maneuver.type == 'special':
                    targets = [i for i in self.active_allies()]
                    while maneuver.can_target_more() and len(targets) > 0:
                        target = random.choice(targets)
                        targets.remove(target)
                        maneuver.add_target(target)

                while maneuver.can_target_more() and len(targets) > 0:
                    vitality = min(vitalities)
                    index = vitalities.index(vitality)
                    target = targets.pop(index)
                    vitalities.pop(index)
                    maneuver.add_target(target)
        for i in self.enemies:
            if i.active_maneuver is not None:
                i.active_maneuver.select()
        self.refresh_allies()

    def refresh_allies(self):
        for i in self.allies:
            i.enemies = self.active_enemies()
            i.allies = self.active_allies()
            i.clear()
            if i.target is not None:
                if i.target not in self.active_enemies():
                    try:
                        i.set_target(self.active_enemies()[0])
                    except IndexError:
                        self.ended = True

    def get_enemies(self):
        return [i.person for i in self.enemies]

    def refresh_enemies(self):
        for i in self.enemies:
            i.enemies = self.active_allies()
            i.allies = self.active_enemies()
            i.clear()

    def get_winner(self):
        if self.fleed:
            return 'fleed'
        if all([i.inactive for i in self.allies]):
            return 'enemies'
        elif all([i.inactive for i in self.enemies]):
            return 'allies'
        else:
            return None

    def get_loot(self):
        try:
            loot = self.loot
        except AttributeError:
            enemies = self.get_enemies()
            loot = []
            for i in enemies:
                for item in i.get_items('all'):
                    loot.append(i.remove_item(item, 'all'))
            self.loot = loot
        return loot

    def get_corpses(self):
        return [i for i in self.get_enemies() if i.has_feature('dead')]

    def end(self):
        self.loot = self.get_loot()
        self.corpses = self.get_corpses()
        self.captives = self.get_captives()

    def get_captives(self):
        return [i for i in self.get_enemies() if not i.has_feature('dead')]


class SimpleCombatant(object):

    def __init__(self, person, fight):

        self.fight = fight
        self.person = person
        self.type = None
        self.maneuvers = []
        self.selected_maneuver = None
        self.active_maneuver = None
        self.protections = []
        self._hp = self.max_hp()
        self._defence = self.max_defence()
        self._disabled = False
        self.enemies = []
        self.allies = []
        self._inactive = False
        self.incoming_damage_multipliers = []
        self.skill_difference = 0
        self.power_up = 0
        self._target = None
        self._combat_style = None
        if self.combat_style() == 'shieldbearer':
            self.defence += 5 * self.shield_quality()

    @property
    def hp(self):
        return self._hp

    def shield_quality(self):
        for i in self.weapons():
            if i.size == 'shield':
                return i.quality
        return 0

    @hp.setter
    def hp(self, value):
        self._hp = value
        if not self.person.has_buff('wound'):
            self.person.add_buff('wound', 1)

    @property
    def target(self):
        if self._target is None:
            try:
                target = self.enemies[0]
            except IndexError:
                target = None
            return target
        return self._target

    def combat_style(self):
        if self.person.main_hand is not None:
            if self.person.main_hand.size == 'offhand':
                return 'cutthroat'
            if (self.person.main_hand.id == 'bare_hands' and
                    self.person.other_hand.id == 'bare_hands'):
                print self.person.main_hand.id
                print self.person.main_hand.id
                return 'brawler'
        if any([i.size == 'shield' for i in self.weapons()]):
            return 'shieldbearer'
        if any([i.size == 'versatile' for i in self.weapons()]):
            return 'swashbuckler'
        if any([i.size == 'twohand' for i in self.weapons()]):
            return 'wrecker'
        return 'brawler'

    def get_damage_multiplier(self, source):
        if source.combat_style() == 'versatile':
            return 2
        if source.combat_style() == 'cutthroat':
            if self.weight() == 'mobile':
                return 3
        if source.combat_style() == 'wrecker':
            if self.combat_style() == 'shieldbearer' or self.weight() == 'heavy':
                return 3
        return 1

    def weight(self):
        if self.armor_rate is None:
            return 'mobile'
        elif self.armor_rate == 'heavy_armor':
            return 'heavy'
        return

    def set_target(self, target):
        if self.active_maneuver is not None:
            self.active_maneuver.add_target(target)
        self._target = target

    def maneuvers_list(self):
        list_ = [i(self) for i in RuledManeuver.__subclasses__()]
        list_.extend([i(self) for i in SimpleManeuver.__subclasses__()])
        return list_

    def get_meneuvers(self):
        self.maneuvers = []
        maneuvers = [i for i in self.maneuvers_list()
                     if i.can_be_applied(self)]
        number = self.max_maneuvers()
        while number > 0:
            maneuver = random.choice(maneuvers)
            self.maneuvers.append(maneuver)
            maneuvers.remove(maneuver)
            number -= 1

    def max_maneuvers(self):
        value = 3
        if self.skill_difference < 0:
            for i in range(0, abs(self.skill_difference)):
                if i % 2 == 0:
                    value -= 1
        elif self.skill_difference > 0:
            for i in range(0, abs(self.skill_difference)):
                if i % 2 != 0:
                    value += 1
        return value

    def knockdown(self):
        self._inactive = True

    @property
    def inactive(self):
        return self.hp < 1 or self._inactive

    @property
    def disabled(self):
        return self.inactive or self._disabled

    @disabled.setter
    def disabled(self, bool_):
        self._disabled = bool_

    @inactive.setter
    def inactive(self, bool_):
        self._inactive = bool_

    @property
    def physique(self):
        return self.person.physique

    @property
    def agility(self):
        return self.person.agility

    def set_enemies(self, enemies):
        self.enemies = enemies

    @property
    def name(self):
        return self.person.name

    @property
    def avatar(self):
        return self.person.avatar_path

    @property
    def combat_level(self):
        return self.person.skill('physique')

    def weapons(self):
        return self.person.weapons()

    def weapon_quality(self):
        value = 0
        for i in self.weapons():
            try:
                value += i.quality
            except AttributeError:
                pass
        return value

    @property
    def attack(self):
        return self.physique + self.weapon_quality() + self.power_up

    @property
    def armor_rate(self):
        try:
            rate = self.person.armor.armor_rate
            if rate == 'unarmored':
                rate = None
        except AttributeError:
            rate = None
        return rate

    def max_defence(self):
        armor = self.person.armor
        try:
            quality = armor.quality
        except AttributeError:
            return self.person.agility * 5
        else:
            if armor.armor_rate == 'light_armor':
                return (self.person.agility + quality * 2) * 3
            elif armor.armor_rate == 'heavy_armor':
                return quality * 10
        return self.person.agility * 5

    @property
    def defence(self):
        return self._defence

    @defence.setter
    def defence(self, value):
        self._defence = max(0, min(self.max_defence(), value))

    def max_hp(self):
        return self.physique * 3

    def select_maneuver(self, maneuver):
        maneuver.clear()
        self.selected_maneuver = maneuver
        maneuver.select()

    def activate_maneuver(self, maneuver):
        self.select_maneuver(maneuver)
        self.active_maneuver = self.selected_maneuver
        self.selected_maneuver = None
        if self.target is not None:
            self.active_maneuver.add_target(self.target)

    def damage(self, value, source, ignore_armor=False):

        value += self.fight.escalation
        for i in self.incoming_damage_multipliers:
            value *= i
        value = int(value)
        value *= self.get_damage_multiplier(source)
        for i in self.protections:
            value = i.protect(value, source, self)
        if value > 0:
            self.fight.log("{name} damaged for {value}, source:{source}".format(
                name=self.name.encode('utf-8'), value=value, source=source.name.encode('utf-8')))
        if ignore_armor:
            self.hp -= value
            return
        if self.defence < value:
            self.defence = 0
            value -= self.defence
            self.hp -= value
            if self.hp <= 0:
                if source.combat_style() != 'brawler':
                    if not self.person.player_controlled:
                        self.person.die()
        else:
            self.defence -= value

    def vitality(self):
        return self.defence + self.hp

    def clear(self):
        if self.active_maneuver is not None:
            self.active_maneuver.clear()
        self.active_maneuver = None
        self.selected_maneuver = None
        self._disabled = False
        self.incoming_damage_multipliers = []
        self.protections = []
        self.get_meneuvers()


class Maneuver(object):

    def __init__(self, person):
        self.targets_available = None
        self.targets = []
        self.person = person
        self._can_target_more = True
        self.self_targeted = False

    @property
    def name(self):
        try:
            name = store.maneuvers_data[self.id]['name']
        except KeyError:
            name = self.id
        return name

    @property
    def description(self):
        try:
            desc = store.maneuvers_data[self.id]['description']
        except KeyError:
            desc = 'No description'
        return desc

    def clear(self):
        self.targets = []
        self._can_target_more = True

    def can_target_more(self):
        try:
            can_target = self.targets_available > len(self.targets)
        except TypeError:
            can_target = False
        return can_target and self._can_target_more and not self.self_targeted

    def can_be_applied(self, person):
        #
        raise Exception("Not implemented")

    def activate(self):
        if self.person.disabled:
            return
        if self.self_targeted:
            self.targets = []
            self.targets.append(self.person)
        for i in self.targets:
            self._activate(i)

    def _activate(self, target):
        raise Exception('Not implemented')

    def select(self):
        raise Exception('Not implemented')

    def ready(self):
        raise Exception("Not implemented")

    def add_target(self, target):
        if not self.can_target_more():
            try:
                self.targets.pop(0)
            except IndexError:
                pass
            self.targets.append(target)
            return
        if target not in self.targets:
            self.targets.append(target)

    def protect(self, value, source, who):
        if value < 1:
            return value
        if self.person.disabled:
            return value
        start = value
        new = self._protect(value, source)
        self.person.fight.log('{name} protected {start} damage, result: {new}'.format(
            name=who.name.encode('utf-8'), start=start, new=new))
        return new

    def _protect(self, target):
        raise Exception("Not implemented")


class SimpleManeuver(Maneuver):

    def can_be_applied(self, person):

        return True

    def select(self):
        pass

    def ready(self):
        return not self.can_target_more()


class RuledManeuver(Maneuver):

    def can_be_applied(self, person):
        raise Exception("Not implemented")

    def select(self):
        pass

    def ready(self):
        return not self.can_target_more()


class SwiftStrike(SimpleManeuver):

    def __init__(self, person):

        super(SwiftStrike, self).__init__(person)
        self.targets_available = 1
        self.id = 'swift_strike'
        self.type = 'attack'

    def _activate(self, target):
        if target.active_maneuver is not None:
            if isinstance(target.active_maneuver, Dodge):
                target.damage(self.person.attack * 2, self.person)
                return
        target.damage(self.person.attack, self.person)


class DirectStrike(SimpleManeuver):

    def __init__(self, person):

        super(DirectStrike, self).__init__(person)
        self.targets_available = 1
        self.id = 'direct_strike'
        self.type = 'attack'

    def _activate(self, target):
        if target.active_maneuver is not None:
            if target.active_maneuver.type == 'attack':
                target.damage(self.person.attack * 2, self.person)
                return
        target.damage(self.person.attack, self.person)


class HeavyStrike(SimpleManeuver):

    def __init__(self, person):
        super(HeavyStrike, self).__init__(person)
        self.targets_available = 1
        self.id = 'heavy_strike'
        self.type = 'attack'

    def _activate(self, target):
        if target.active_maneuver is not None:
            if isinstance(target.active_maneuver, Block):
                target.damage(self.person.attack * 2, self.person)
                return
        target.damage(self.person.attack, self.person)


class WideStrike(SimpleManeuver):

    def __init__(self, person):
        super(WideStrike, self).__init__(person)
        self.targets_available = len(self.person.enemies)
        self.id = 'wide_strike'
        self.type = 'attack'

    def _activate(self, target):
        target.damage(self.person.attack, self.person)

    def select(self):
        for i in self.person.enemies:
            self.add_target(i)

    def can_be_applied(self, person):
        if person.type == 'npc':
            if len(person.enemies) > 1:
                return person.combat_style() == 'wrecker'
            return False
        return person.combat_style() == 'wrecker'


class Dodge(SimpleManeuver):

    def __init__(self, person):
        super(Dodge, self).__init__(person)
        self.targets_available = 1
        self.self_targeted = True
        self.type = 'protection'
        self.id = 'dodge'

    def _activate(self, target):
        target.protections.append(self)

    def _protect(self, value, source):
        if isinstance(source.active_maneuver, SwiftStrike):
            return value
        elif isinstance(source.active_maneuver, HeavyStrike):
            self.person.power_up += 1
        return 0


class Block(SimpleManeuver):

    def __init__(self, person):

        super(Block, self).__init__(person)
        self.targets_available = 1
        self.type = 'protection'
        self.id = 'block'
        self.self_targeted = True

    def _activate(self, target):
        target.protections.append(self)

    def _protect(self, value, source):
        if isinstance(source.active_maneuver, HeavyStrike):
            return value
        elif isinstance(source.active_maneuver, SwiftStrike) or isinstance(source.active_maneuver, WideStrike):
            self.person.power_up += 1
        return 0


class Parry(SimpleManeuver):

    def __init__(self, person):

        super(Parry, self).__init__(person)
        self.targets_available = 1
        self.self_targeted = True
        self.type = 'protection'
        self.id = 'parry'

    def _activate(self, target):
        self.protected = [i for i in self.targets]
        target.protections.append(self)

    def _protect(self, value, source):
        if value > 0:
            for i in self.protected:
                i.protections.remove(self)
                self.person.power_up += 1
            return 0
        return value

    def can_be_applied(self, person):
        if person.type == 'player':
            return person.combat_style() == 'swashbuckler'
        else:
            if len(person.enemies) > 1:
                return False
        return person.combat_style() == 'swashbuckler'


class ShielUp(RuledManeuver):

    def __init__(self, person):

        super(ShielUp, self).__init__(person)
        self.targets_available = 1
        self.type = 'protection'
        self.id = 'shield_up'

    def _activate(self, target):
        target.protections.append(self)
        self.p_target = target

    def _protect(self, value, source):
        if self.p_target == self.person:
            target = self.person
            if target.armor_rate is None:
                heal = target.agility * 3
            elif target.armor_rate == 'light_armor':
                heal = target.agility * 2
            else:
                heal = target.physique * 2
            target.defence = min(target.max_defence(), target.defence + heal)
            self.person.fight.escalation += 1
        if value > 0:
            self.p_target.protections.remove(self)
            return 0
        return value

    def can_be_applied(self, person):
        shield = person.combat_style() == 'shieldbearer'
        if person.type == 'npc':
            if person.defence < 1:
                return shield
            else:
                return False
        return shield


class Backstab(RuledManeuver):

    def __init__(self, person):

        super(Backstab, self).__init__(person)
        self.targets_available = 1
        self.type = 'attack'
        self.id = 'backstab'

    def _activate(self, target):
        target.damage(self.person.attack * 2, self.person, True)

    def can_be_applied(self, person):
        return person.combat_style() == 'cutthroat'


class PinDown(RuledManeuver):

    def __init__(self, person):

        super(PinDown, self).__init__(person)
        self.targets_available = 1
        self.type = 'special'
        self.id = 'pin_down'

    def _activate(self, target):
        target.knockdown()

    def can_be_applied(self, person):
        if len(person.enemies) < 1:
            return False
        enemy = person.enemies[0]
        amount = len(person.enemies) < 2
        physique = enemy.physique < person.physique
        weapon = len(person.enemies[0].weapons()) < 1
        armor = enemy.armor_rate is None
        style = person.combat_style() == 'brawler'
        return amount and physique and weapon and style and armor


class Tank(RuledManeuver):

    def __init__(self, person):
        super(Tank, self).__init__(person)
        self.targets_available = 1
        self.self_targeted = True
        self.type = 'protection'
        self.id = 'tank'

    def _activate(self, target):
        for i in self.person.allies:
            if (not isinstance(i.active_maneuver, Tank) and
                    not any(isinstance(n, Tank) for n in i.protections)):
                i.protections.append(self)

    def _protect(self, value, source):
        value /= 2
        value = int(value)
        self.person.damage(value, source)
        return 0

    def can_be_applied(self, person):
        if person.type == 'player':
            return person.weight() == 'heavy'

        allies = len(person.allies) > 1
        enemies = len(person.enemies) > 1
        defence = all([person.defence >= i.defence for i in person.allies])
        return allies and enemies and defence and person.weight() == 'heavy'


class Outflank(RuledManeuver):

    def __init__(self, person):
        super(Outflank, self).__init__(person)
        self.targets_available = 1
        self.self_targeted = True
        self.type = 'special'
        self.id = 'outflank'

    def select(self):
        self.hp = self.person.hp
        self.defence = self.person.defence
        self.person.protections.append(self)

    def _protect(self, value, source):
        if value > 0:
            self.person.protections.remove(self)
            return 0
        return value

    def _activate(self, target):
        if self.hp > target.hp or self.defence > target.defence:
            return
        else:
            self.person.power_up += 1

    def can_be_applied(self, person):
        if person.type == 'npc':
            if len(person.enemies) > 1:
                return False
        return person.weight() == 'mobile'
