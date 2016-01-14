# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
import mer_features


class Person(object):

    def __init__(self):
        self.firstname = "Stranger" # One always must have this one.
        self.surname = ""          # Not obligate.
        self.nickname = ""          # Can be modified by player. If present - shown as default name
        self.avatar = "characters/none.jpg"
        self.age = "adolescent"          # can be "junior", "adolescent", "mature" or "elder"
        self.gender = "male"        # can be "male", "female", "shemale" or "sexless"
        self.species = "human"      # "human", "strange"
        self.morphology = "humanoid"    # "humanoid", "centaur", "amorphous", "quadruped", "insectoid"
        self.members = ["Hands", "Mouth", "Butt"]   # Bodyparts to use as implements and more
        self.alignment = {
            "Orderliness": "Conformal",   # "Lawful", "Conformal" or "Chaotic"
            "Activity": "Reasonable",        # "Ardent", "Reasonable" or "Timid"
            "Morality": "Selfish",       # "Good", "Selfish" or "Evil"
        }
        self.features = []          # gets Feature() objects and their child's
        self.needs = {              # List of persons needs
            "general":  {"level": 3, "status": "relevant", },        # Need {level(1-5), status (relevant, satisfied, overflow, tension, frustration)}
        }
        self.ration = "full"        # ????? can be  "none", "half", "full" or "double"
        self.chakra = 1             # Number of magic item slots in one's soul
        self.sigil = None           # House sigil on the one's soul. Makes you able to use sparks directly
        self.sparks = 0             # Number of sparks in the soul
        self.inventory = []         # Possessed amd carried, but not worn items
        self.equipment = {}         # Slots for armor, cloth, weapon, jewelry, etc. One slot = one item
        self.ap_spent = 0           # Number of AP spent by player this turn
        self.color = "unknown"
        self.ff_combat_style = "bully"
        #attributes:
        self.physique = 3
        self.spirit = 3
        self.agility = 3
        self.mind = 3
        self.sensitivity = 3
        #inner resources:
        self.max_stamina = self.attribute('physique')
        self.stamina = self.max_stamina
        self.max_accuracy = self.attribute('agility')
        self.accuracy = self.max_accuracy
        self.max_concentration = self.attribute('mind')
        self.concenctation = self.max_concentration
        self.max_willpower = self.attribute('spirit')
        self.willpower = self.max_willpower
        self.max_glamour = self.attribute('sensitivity')
        self.glamour = self.max_glamour

        self.moodlets = {
            "bad": [],
            "good": [],
        }          # Moodlet() or it's child's. Good or bad
        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.skills = {
            "training":  ['manual', 'oral', 'penetration'],        # List of skills. Skills get +1 bonus
            "experience":  [],      # List of skills. Skills get +1 bonus
            "specialisation": [],   # List of skills. Skills get +1 bonus
            "talent": [],           # List of skills. Skills get +1 bonus
        }

    
    def add_feature(self, name):#adds features to person, if mutually exclusive removes old feature
        new_feature = mer_features.Feature(name)
        for f in self.features:
            if new_feature.slot == f.slot:
                self.features.remove(f)
        self.features.append(new_feature)


    def use_resource(self, resource, value=1, difficulty=0):#method for using our inner resources for some actions
    """
    :return: True if we are able to do action
    """
        res_to_use = self.__getattribute__(resource)
        if res_to_use < difficulty:
            return False
        if not res_to_use - value < 0:
            self.__dict__[resource] -= value
            return True
        return False
    


    def rest(self):
        self.stamina = self.max_stamina
        self.accuracy = self.max_accuracy
        self.concenctation = self.max_concentration
        self.willpower = self.max_willpower
        self.glamour = self.max_glamour
        self.sparks -= self.allowance
    


    @property
    def name(self):
        # TODO: вставить декоратор чтобы функция вызывалась как переменная (без скобочек в конце)
        """
        :return: Nickname if present or Firstname + Secondname.
        """
        """
        :return:
        """
        if self.nickname:
            return self.nickname
        else:
            return str(self.firstname + " " + self.surname)

    def fullname(self):
        return str(self.firstname + " " + self.nickname + " " + self.surname)

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

        value = self.__getattribute__(attribute)
        for feature in self.features:
            if attribute in feature.modifiers.keys():
                value += feature.modifiers[attribute]
        if value < 1:
            value = 1
        if value > 5:
            value = 5
        return value

    def performance(self, skill):
        """
        :return: performance rate for a given skill
        """
        result = 0
        for factor in self.skills:
            if skill in factor:
                result += 1

        return result

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




