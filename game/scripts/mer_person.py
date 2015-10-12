# -*- coding: <UTF-8> -*-
from random import *
import renpy.store as store
import renpy.exports as renpy


class Person(object):

    def __init__(self):
        self.name = "Stranger"
        self.avatar = "characters/none.jpg"
        self.age = "adult"          # can be "child", "young", "adult" or "elder"
        self.gender = "male"        # can be "male", "female", "shemale" or "sexless"
        self.species = "human"      # "human", ???
        self.morphology = "humanoid"    # "humanoid", "centaur", "amorphous", "quadruped", "insectoid"
        self.lawfulness = 0             # more is Lawful, less is Chaotic, about 0 is Conformal
        self.goodness = 0            # more is Good, less is Evil, about 0 is Egoist
        self.features = []          # gets Feature() objects and their child's
        self.ration = "full"        # can be  "none", "half", "full" or "double"
        self.chakra = 1             # Number of magic slots in one's soul
        self.sigil = None           # House sigil on the one's soul. Makes you able to use sparks directly
        self.sparks = 0             # Number of sparks in the soul
        self.inventory = []         # Possessed amd carried, but not worn items
        self.equipment = {}         # Slots for armor, cloth, weapon, jewelry, etc. One slot = one item
        self.ap_spent = 0           # Number of AP spent by player this turn
        self.color = "unknown"
        self.moodlets = {
            "bad": [],
            "good": [],
        }          # Moodlet() or it's child's. Good or bad
        self.lifestyle = 0         # Sparks spend each turn on a lifestyle
        self.skills = {
            "manual": 1,
            "oral": 1,
            "penetration": 1
        }
        self.members = ["Hands", "Mouth", "Butt"]   # Bodyparts to use as implements and more

    def gender_features(self):
        femininity = 0
        masculinity = 0
        if self.gender == "male":
            masculinity += 10
        elif self.gender == "female":
            femininity += 10
        elif self.gender == "shemale":
            femininity += 10
            masculinity += 5

        return femininity, masculinity

    def show_gender(self):
        features = self.gender_features()
        femininity = features[0]
        masculinity = features[1]
        if femininity > masculinity:
            gender = "female"
        elif femininity == masculinity:
            gender = "???"
        else:
            gender = "male"

        return gender

    def attribute(self, attribute):
        """
        Evaluates base attribute value of person based on features, age, gender, etc.
        :param attribute: physique, agility, spirit, mind, sensitivity.
        :return: attribute value averege is 3, no less than 1
        """
        value = 3
        if self.age == "child":
            value -= 1
        if attribute == "physique" or attribute == "phy":
            if self.age == "adult":
                value += 1
            if self.gender == "male":
                value += 1
            elif self.gender == "female":
                value -= 1

        if attribute == "sensitivity" or attribute == "sns":
            if self.age == "child":
                value += 2
            if self.gender == "male":
                value -= 1
            elif self.gender == "female":
                value += 1

        if attribute == "agility" or attribute == "agi":
            if self.age == "child":
                value += 1              # to be equally as high as adult and young
            elif self.age == "elder":
                value -= 1

        if attribute == "mind" or attribute == "mnd":
            if self.age == "elder":
                value += 1

        for feature in self.features:
            if feature.name == "blood":
                for key in feature.modifiers:
                    if attribute == key:
                        value += feature.modifiers[key]

        if value < 1:
            value = 1
        return value

    def hunger(self):
        hunger = self.attribute("physique")
        return hunger

    def food_consumed(self):
        if self.ration == "none":
            consumption = 0
        elif self.ration == "half":
            consumption = self.hunger()/2
            if consumption < 1:
                consumption = 1
        elif self.ration == "double":
            consumption = self.hunger()*2
        else:
            consumption = self.hunger()

        return consumption

    def ap(self):
        """
        :return: Action Points
        """

        if self.mood() in ("depressed", "macabre", "frustrated"):
            ap = 1
        elif self.mood() in ("happy", "amused"):
            ap = 3
        else:
            ap = 2

        ap -= self.ap_spent

        if ap < 0:
            ap = 0

        return ap

    def mood(self):
        mood = "normal"
        bad = len(self.moodlets["bad"])
        good = len(self.moodlets["good"])
        if bad > good:
            if good == 0:
                if bad < 2 + self.attribute("spirit") - self.attribute("sns"):
                    mood = "depressed"
                else:
                    mood = "macabre"
            else:
                mood = "frustrated"
        if bad < good:
            if bad == 0:
                mood = "happy"
            else:
                mood = "content"

        return mood

    def gain_mood(self, moodlet_name):
        moodlet = moodlet_name(self)

        if moodlet.good:
            self.moodlets["good"].append(moodlet)
        else:
            self.moodlets["bad"].append(moodlet)




