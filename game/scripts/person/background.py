    # -*- coding: UTF-8 -*-
import random

import renpy.store as store
import renpy.exports as renpy

from mer_item import create_item
import mer_utilities


class BackgroundBase(object):

    def __init__(self, id_, data_dict):
        self.id = id_
        self.data_dict = getattr(store, data_dict)
        self.name = self.data_dict[id_]['name']
        self._description = None
        try:
            self.available_technical_levels = self.data_dict[
                id_]['available_technical_levels']
        except KeyError:
            self.available_technical_levels = [1, 2, 3, 4, 5]
        try:
            self.available_prestige_levels = self.data_dict[
                id_]['available_prestige_levels']
        except KeyError:
            self.available_prestige_levels = [1, 2, 3, 4, 5]
        try:
            self.technical_level = self.data_dict[id_]['technical_level']
        except KeyError:
            self.technical_level = 0
        try:
            self.prestige_level = self.data_dict[id_]['prestige_level']
        except KeyError:
            self.prestige_level = 0
        try:
            self.features = self.data_dict[id_]['features']
        except KeyError:
            self.features = []

    def is_available(self, background):
        return (background.technical_level in self.available_technical_levels
                and background.prestige_level in self.available_prestige_levels)

    def is_available_tech(self, background):
        return background.technical_level in self.available_technical_levels

    def is_available_prestige(self, background):
        return background.prestige_level in self.available_prestige_levels

    def apply(self, owner):
        for feature in self.features:
            owner.add_feature(feature)
        dice = mer_utilities.roll(1, 10)

        if dice:
            feature = 'talanted_%s' % self.id
            if feature not in store.person_features.keys():
                feature = self.id
            if feature in store.person_features.keys():
                owner.add_feature(feature)
        else:
            feature = self.id
            if feature in store.person_features.keys():
                owner.add_feature(feature)
        self.apply_other(owner)

    def apply_other(self, owner):
        return

    @property
    def description(self):
        if self._description is not None:
            return self._description
        else:
            return 'No description'


class Homeworld(BackgroundBase):

    def __init__(self, id_, data_dict='homeworlds_dict'):
        super(Homeworld, self).__init__(id_, data_dict)
        value = self.data_dict[id_]['descriptions']
        self._description = random.choice(value)


class Family(BackgroundBase):

    def __init__(self, id_, data_dict='families_dict'):
        super(Family, self).__init__(id_, data_dict)
        self._description = self.data_dict[id_]['description']


class Education(BackgroundBase):

    def __init__(self, id_, data_dict='educations_dict'):
        super(Education, self).__init__(id_, data_dict)
        try:
            self.skills = self.data_dict[id_]['skills']
        except KeyError:
            self.skills = None
        self._description = self.data_dict[id_]['description']


class Occupation(BackgroundBase):

    def __init__(self, id_, data_dict='occupations_dict'):
        super(Occupation, self).__init__(id_, data_dict)
        try:
            self.skills = self.data_dict[id_]['skills']
        except KeyError:
            self.skills = None


class Culture(BackgroundBase):

    def __init__(self, id_, data_dict='cultures_dict'):
        super(Culture, self).__init__(id_, data_dict)
        self.available_skin_colors = self.data_dict[
            id_]['available_skin_colors']


class Background(object):

    def __init__(self, age, world=None, culture=None, family=None, education=None,
                 occupation=None):
        self.world = None
        self.culture = None
        self.family = None
        self.education = None
        self.occupation = None
        self.make(world, culture, family, education, occupation, age)
        self._applied = False

    def equip(self, owner):
        if self.occupation is None:
            return
        id_ = self.occupation.id
        try:
            equipment = store.background_equipment[id_]
        except KeyError:
            return
        for key, value in equipment.items():
            if value is not None:
                if key == 'armor':
                    item = create_item(value, 'armor')
                    owner.equip_item(item, 'overgarments')
                else:
                    item = create_item(value, 'weapon')
                    owner.equip_item(item, key)

    def make(self, world, culture, family, education, occupation, age):
        self._set_culture(culture)
        self._set_world(world)
        self._set_family(family)
        self._set_education(education)
        if age != 'junior':
            self._set_occupation(occupation)

    def _set_world(self, world=None):
        if world is None:
            world = random.choice(store.homeworlds_dict.keys())
        self.world = Homeworld(world)

    def _set_culture(self, culture=None):
        if culture is None:
            culture = random.choice(store.cultures_dict.keys())
        self.culture = Culture(culture)

    def _set_family(self, family=None):
        if family is None:
            families = [Family(family)
                        for family in store.families_dict.keys()]
            available_families = []
            for family in families:
                if self.world.is_available_prestige(family):
                    available_families.append(family)

            try:
                self.family = random.choice(available_families)
            except IndexError:
                print 'family randomed'
                self.family = random.choice(families)
        else:
            self.family = Family(family)

    def _set_education(self, education=None):
        if education is None:
            educations = [Education(education)
                          for education in store.educations_dict.keys()]
            available_educations = []
            for education in educations:
                if self.world.is_available_tech(education) and self.family.is_available_prestige(education):
                    available_educations.append(education)
            try:
                self.education = random.choice(available_educations)
            except IndexError:
                self.education = Education('carefree')
        else:
            self.education = Education(education)

    def _set_occupation(self, occupation=None):
        if occupation is None:
            available_occupations = []
            for occupation in store.occupations_dict.keys():
                current = Occupation(occupation)
                if (self.world.is_available_tech(current) and
                    self.family.is_available_prestige(current)):
                    available_occupations.append(current)
            try:
                self.occupation = random.choice(available_occupations)
            except IndexError:
                self.occupation = None
        else:
            self.occupation = Occupation(occupation)

    def apply(self, owner):
        if not self._applied:
            list_ = ['world', 'culture', 'family', 'education', 'occupation']
            if owner.age == 'junior':
                list_.remove('occupation')
            for i in list_:
                bg = getattr(self, i)
                if bg is not None:
                    bg.apply(owner)
            self.equip(owner)
            self._applied = True
