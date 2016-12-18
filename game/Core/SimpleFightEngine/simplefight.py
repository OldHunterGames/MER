# -*- coding: UTF-8 -*-
import random

import renpy.store as store
import renpy.exports as renpy


class SimpleFight(object):


    def __init__(self, allies_list, enemies_list):

        self.allies = [SimpleCombatant(i, self) for i in allies_list]
        self.enemies = [SimpleCombatant(i, self) for i in enemies_list]
        allies_average_skill = sum([i.combat_level for i in self.allies])/len(self.allies)
        enemies_average_skill = sum([i.combat_level for i in self.enemies])/len(self.enemies)
        difference = allies_average_skill - enemies_average_skill
        self.target = self.enemies[0]
        self.escalation = 0
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

    def set_target(self, target):
        self.target = target
    
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
        if self.target is not None:
            if self.target not in self.active_enemies():
                self.target = self.active_enemies()[0]
        self.enemies_turn()

    def enemies_turn(self):
        self.refresh_enemies()
        for i in self.enemies:
            if i.inactive:
                continue
            try:
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
        self.refresh_allies()

    def refresh_allies(self):
        for i in self.allies:
            i.enemies = self.active_enemies()
            i.clear()

    def refresh_enemies(self):
        for i in self.enemies:
            i.enemies = self.active_allies()
            i.clear()

    def get_winner(self):
        if all([i.inactive for i in self.allies]):
            return 'enemies'
        elif all([i.inactive for i in self.enemies]):
            return 'allies'
        else:
            return None

            


class SimpleCombatant(object):


    def __init__(self, person, fight):
        
        self.fight = fight
        self.person = person
        self.type = None
        self.maneuvers = []
        self.selected_maneuver = None
        self.active_maneuver = None
        self.protections = []
        self.hp = self.max_hp()
        self._defence = self.max_defence()
        self._disabled = False
        self.enemies = []
        self._inactive = False
        self.incoming_damage_multipliers = []
        self.skill_difference = 0

    def maneuvers_list(self):
        list_ = [i(self) for i in RuledManeuver.__subclasses__()]
        list_.extend([i(self) for i in SimpleManeuver.__subclasses__()])
        return list_

    def get_meneuvers(self):
        self.maneuvers = []
        maneuvers = [i for i in self.maneuvers_list() if i.can_be_applied(self)]
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
                if i%2 == 0:
                    value -= 1
        elif self.skill_difference > 0:
            for i in range(0, abs(self.skill_difference)):
                if i%2 != 0:
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
        return self.person.skill('combat').level

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
        return self.physique + self.weapon_quality()

    @property
    def armor_rate(self):
        try:
            rate = self.person.armor.armor_rate
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
                return (self.person.agility + quality*2) * 3
            elif armor.armor_rate == 'heavy_armor':
                return quality * 10

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

    def damage(self, value):
        value += self.fight.escalation
        for i in self.incoming_damage_multipliers:
            value *= i
        value = int(value)
        for i in self.protections:
            value = i.protect(value)
        if self.defence < value:
            self.defence = 0
            value -= self.defence
            self.hp -= value
        else:
            self.defence -= value

    def vitality(self):
        return self.defence + self.hp

    def clear(self):
        self.active_maneuver = None
        self.selected_maneuver = None
        self._disabled = False
        self.incoming_damage_multipliers = []
        self.get_meneuvers()
        


class Maneuver(object):


    def __init__(self, person):
        self.targets_available = None
        self.targets = []
        self.person = person
        self._can_target_more = True
        self.self_targeted = False

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
        self.clear()
        self.person.active_maneuver = None

    def _activate(self, target):
        raise Exception('Not implemented')

    def select(self):
        raise Exception('Not implemented')

    def ready(self):
        raise Exception("Not implemented")

    def add_target(self, target):
        if not self.can_target_more():
            return
        if target not in self.targets:
            self.targets.append(target)

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

class Hit(SimpleManeuver):


    def __init__(self, person):

        super(Hit, self).__init__(person)
        self.targets_available = 1
        self.name = 'Hit'
        self.type = 'attack'

    def _activate(self, target):
        target.damage(self.person.attack)

class Cleave(SimpleManeuver):


    def __init__(self, person):

        super(Cleave, self).__init__(person)
        self.targets_available = self.person.physique
        self.name = 'Cleave'
        self.type = 'attack'

    def _activate(self, target):
        target.damage(self.person.attack/2)

    def select(self):
        targets = [i for i in self.person.enemies]
        random.shuffle(targets)
        while self.can_target_more() and len(targets) > 0:
            self.add_target(targets.pop())
        self._can_target_more = False

    def can_be_applied(self, person):
        if person.type == 'player':
            return True
        else:
            if len(person.enemies) > 1:
                return True
        return False


class Charge(SimpleManeuver):


    def __init__(self, person):

        super(Charge, self).__init__(person)
        self.targets_available = 1
        self.name = 'Charge'
        self.type = 'attack'

    def _activate(self, target):
        target.damage(self.person.attack * 2)

    def select(self):
        targets = [i for i in self.person.enemies]
        target = random.choice(targets)
        self.add_target(target)
        self.person.incoming_damage_multipliers.append(2)
        self._can_target_more = False

    def can_be_applied(self, person):
        if person.type == 'player':
            return True
        else:
            if len(person.enemies) > 1:
                return False
        return True


class Block(SimpleManeuver):


    def __init__(self, person):

        super(Block, self).__init__(person)
        self.targets_available = 1
        self.type = 'protection'
        self.name = 'Block'
        self.self_targeted = True

    def _activate(self, target):
        target.protections.append(self)


    def protect(self, value):
        return value/2

    def can_be_applied(self, person):
        if person.type == 'player':
            return True
        else:
            if len(person.enemies) > 1:
                return True
        return False
class Parry(SimpleManeuver):


    def __init__(self, person):

        super(Parry, self).__init__(person)
        self.targets_available = 1
        self.self_targeted = True
        self.type = 'protection'
        self.name = 'Parry'

    def _activate(self, target):
        self.protected = [i for i in self.targets]
        target.protections.append(self)

    def protect(self, value):
        if value > 0:
            for i in self.protected:
                i.protections.remove(self)
            return 0
        return value

    def can_be_applied(self, person):
        if person.type == 'player':
            return True
        else:
            if len(person.enemies) > 1:
                return False
        return True

class Recovery(SimpleManeuver):


    def __init__(self, person):

        super(Recovery, self).__init__(person)
        self.targets_available = 1
        self.self_targeted = True
        self.type = 'recovery'
        self.name = 'Recovery'

    def _activate(self, target):
        if target.armor_rate is None:
            value = target.agility * 3
        elif target.armor_rate == 'light_armor':
            value = target.agility * 2
        else:
            value = target.physique * 2
        target.defence = min(target.max_defence(), target.defence+value)
        self.person.fight.escalation += 1

class ShielUp(RuledManeuver):


    def __init__(self, person):

        super(ShielUp, self).__init__(person)
        self.targets_available = 1
        self.type = 'protection'
        self.name = 'Shield up'

    def _activate(self, target):
        target.protections.append(self)
        self.p_target = target

    def protect(self, value):
        if self.p_target == self.person:
            target = self.person
            if target.armor_rate is None:
                heal = target.agility * 3
            elif target.armor_rate == 'light_armor':
                heal = target.agility * 2
            else:
                heal = target.physique * 2
            target.defence = min(target.max_defence(), target.defence+heal)
            self.person.fight.escalation += 1
        if value > 0:
            self.p_target.protections.remove(self)
            return 0
        return value

    def can_be_applied(self, person):

        return any([i.size == 'shield' for i in person.weapons()])

class Grapple(RuledManeuver):


    def __init__(self, person):

        super(Grapple, self).__init__(person)
        self.targets_available = 1
        self.type = 'disable'
        self.name = 'Grapple'

    def _activate(self, target):
        target.disabled = True

    def can_be_applied(self, person):
        two_weapons = len(person.weapons()) > 1
        twohand = any([i.size == 'twohand' for i in person.weapons()])
        return not (twohand and two_weapons)

class Precision(RuledManeuver):


    def __init__(self, person):

        super(Precision, self).__init__(person)
        self.targets_available = 1
        self.type = 'attack'
        self.name = 'Precision'

    def _activate(self, target):
        target.hp -= self.person.agility

    def can_be_applied(self, person):
        return any([i.size == 'offhand' for i in person.weapons()])


class PowerStrike(RuledManeuver):


    def __init__(self, person):

        super(PowerStrike, self).__init__(person)
        self.targets_available = 1
        self.type = 'attack'
        self.name = 'Power strike'

    def _activate(self, target):
        target.damage(int(self.person.attack * 1.5))

    def can_be_applied(self, person):
        return any([i.size == 'twohand' for i in person.weapons()])


class Fiencing(RuledManeuver):


    def __init__(self, person):

        super(Fiencing, self).__init__(person)
        self.type = 'attack'
        self.name = 'Fiencing'
        self.targets_available = 1

    def _activate(self, target):
        value = int(self.person.attack / 2)
        target.damage(value)
        self.person.defence += value

    def can_be_applied(self, person):
        return any([i.size == 'versatile' for i in person.weapons()])


class PinDown(RuledManeuver):


    def __init__(self, person):

        super(PinDown, self).__init__(person)
        self.targets_available = 1
        self.type = 'special'
        self.name = 'Pin down'

    def _activate(self, target):
        target.knockdown()

    def can_be_applied(self, person):
        if len(person.enemies) < 1:
            return False
        enemy = person.enemies[0]
        amount = len(person.enemies) < 2
        physique = enemy.physique < person.physique
        skill = enemy.combat_level <= person.combat_level
        return amount and skill and physique