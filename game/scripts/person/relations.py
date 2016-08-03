# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy


class Relations(object):
    _fervor = {-1: "delicate", 0: "plain", 1: "passionate"}
    _distance = {-1: "intimate", 0: "close", 1: "formal"}
    _congruence = {-1: "contradictor", 0: "associate", 1: "supporter"}
    def __init__(self, person1, person2):
        self.persons = [person1, person2]
        self._fervor = 0
        self._distance = 0
        self._congruence = 0
        self.stability = 0
        self.is_player_relations()
            

    def is_player_relations(self):
        if self.persons[0].player_controlled or self.persons[1].player_controlled:
            if not hasattr(self, 'player') and not hasattr(self, 'npc'):
                for p in self.persons:
                    if p.player_controlled:
                        self.player = p
                    else:
                        self.npc = p
            return True
        else:
            return False
    def is_max(self, axis, border):
        d = {'-': -1, '+': 1}
        if getattr(self, axis) == d[border]:
            return True
        return False
    @property
    def fervor(self):
        if self.is_player_relations():
            return self._fervor
        fervor = self._fervor + self.persons[0].alignment.activity + self.persons[1].alignment.activity
        if fervor < -1:
            fervor = -1
        elif fervor > 1:
            fervor = 1
        return fervor
    def show_fervor(self):
        return Relations._fervor[self.fervor]
    

    @property
    def distance(self):
        if self.is_player_relations():
            return self._distance
        distance = self._distance + self.persons[0].alignment.orderliness + self.persons[1].alignment.orderliness
        if distance < -1:
            distance = -1
        elif distance > 1:
            distance = 1
        return distance
    def show_distance(self):
        return Relations._distance[self.distance]
    

    @property
    def congruence(self):
        if self.is_player_relations():
            return self._congruence
        congruence = self._distance + self.persons[0].alignment.morality + self.persons[1].alignment.morality
        if congruence < -1:
            congruence = -1
        elif congruence > 1:
            congruence = 1
        return congruence
    def show_congruence(self):
        return Relations._congruence[self.congruence]

    
    def set_axis(self, axis, value):
        ax = '_%s'%(axis)
        if hasattr(self, ax) and value in range(-1, 2):
            self.__dict__[ax] = value

    def description(self):
        return (self.show_fervor(), self.show_distance(), self.show_congruence())
        
    def change(self, axis, direction):
        if not self.is_player_relations():
            return
        ax = getattr(self, '_%s'%(axis))
        if direction == "+":
            ax += 1
            if ax > 1:
                ax = 1
        elif direction == '-':
            ax -= 1
            if ax < -1:
                ax = -1
        self.set_axis(axis, ax)

    def is_harmony_points(self, *args):
        points = self.harmony()[1]
        return any([point in points for point in args])
    def harmony(self):
        value = 0
        axis = []
        if not self.is_player_relations():
            return value
        tendence = self.npc.attitude_tendency()
        activity = self.npc.alignment.activity
        orderliness = self.npc.alignment.orderliness
        morality = self.npc.alignment.morality
        if tendence == 'conquest':
            if activity == 0:
                activity = 1
            if morality == 0:
                morality = -1
        if tendence == 'contribution':
            if orderliness == 0:
                orderliness = -1
            if morality == 0:
                morality = 1
        if tendence == 'convention':
            if orderliness == 0:
                orderliness == 1
            if activity == 0:
                activity = -1

        difference = self.fervor + activity
        if abs(difference) > 1:
            value += 1
            axis.append(self.show_fervor())
        elif difference == 0:
            if self.fervor != 0:
                value -= 1
        
        difference = self.distance + orderliness
        if abs(difference) > 1:
            value += 1
            axis.append(self.show_distance())
        elif difference == 0:
            if self.distance != 0:
                value -= 1
        
        difference = self.congruence + morality
        if abs(difference) > 1:
            value += 1
            axis.append(self.show_congruence())
        elif difference == 0:
            if self.congruence != 0:
                value -= 1
        if value < 0:
            value = 0
        return value, axis



