# -*- coding: UTF-8 -*-
from collections import OrderedDict
from copy import copy

import mer_utilities as utilities
from mer_command import MenuCard

import renpy.exports as renpy
import renpy.store as store


class ScheduleObject(MenuCard):

    def __init__(self, id, data_dict, locked=False):
        self._data = data_dict[id]
        self.id = id
        self.locked = locked
        self._additional_data = dict()

    def add_data(self, dict):
        self._additional_data = dict

    def _image_raw(self):
        img = self.get_image()
        if img is None:
            return utilities.empty_card()
        return img

    def image(self, size=None):
        if size is None:
            size = (200, 300)
        return renpy.display.im.Scale(self._image_raw(), *size)

    @property
    def _image(self):
        return self._data.get('image')

    def get_image(self):
        # testing image getting system
        path = 'images/%s/%s' % (self._image, self.id)
        images = utilities.get_files(path)
        try:
            img = images[0]
        except IndexError:
            img = None
        return img

    @property
    def cost(self):
        try:
            cost = self._data['cost']
        except KeyError:
            cost = 0
        return cost

    def __getattr__(self, key):
        try:
            value = self.__dict__['_data'][key]
        except KeyError:
            value = self.__dict__['_additional_data'].get(key)
        return value

    def description(self):
        return self._data.get('description', 'No description')

    def name(self):
        return self._data.get('name', 'No name')

    def use(self, person, type):
        self._use(person)
        lbl = self.world + '_%s' % type + '_%s' % self.id
        if renpy.has_label(lbl):
            renpy.call_in_new_context(lbl, person)
        self.locked = False

    def lock(self):
        self.locked = True

    def _use(self, person):
        return


class ScheduleJob(ScheduleObject):

    def __init__(self, *args, **kwargs):
        super(ScheduleJob, self).__init__(*args, **kwargs)
        # job's focus controlled by person
        self.focus = 0

    def full_description(self):
        string = self.name()
        string += '\n current effort: %s' % utilities.encolor_text(
            store.focus_description[self.focus], self.focus)
        if self.focus != 5:
            string += '\n needed effort: %s' %\
                store.effort_quality[self.focus + 1]
        return string

    def _use(self, person):
        if self.skill is not None:
            if person.player_controlled:
                renpy.call_in_new_context(
                    'lbl_jobcheck', person=person, attribute=self.skill)
            else:
                renpy.call_in_new_context(
                    'lbl_jobcheck_npc', person=person, attribute=self.skill)


class Schedule(object):

    def __init__(self):

        self._available_rations = {}
        self._available_jobs = {}
        self._available_accommodations = {}
        self._available_optionals = {}
        self._optional = OrderedDict({0: None, 1: None, 2: None})
        self._job = None
        self._job_buffer = None
        self._accommodation = None
        self._ration = None
        self._default_job = None
        self._default_accommdation = None
        self._default_ration = None

    def set_default(self, type, obj, **kwargs):
        setattr(self, '_default_' + type, obj)
        if getattr(self, '_' + type) is None:
            self.set(type, obj, **kwargs)

    def make_default(self, attr_name):
        self.set(attr_name, getattr(self, '_default_%s' % attr_name))

    def get_cost(self):
        return (self._accommodation.cost +
                self._ration.cost +
                sum([i.cost for i in self._optional.values() if i is not None])
                )

    @property
    def job(self):
        return self._job

    @property
    def accommodation(self):
        return self._accommodation

    @property
    def ration(self):
        return self._ration

    def description(self, key):
        return getattr(self, '_' + key).description

    def remove_buffer(self):
        self._job_buffer = None

    def use(self, user):
        self._job.use(user, 'job')
        self._accommodation.use(user, 'accommodation')
        self._ration.use(user, 'ration')
        for i in self._optional.values():
            if i is not None:
                i.use(user, 'optional')

    def set_optional(self, slot, schedule_object):
        if slot in self._optional.keys():
            self._optional[slot] = schedule_object

    def remove_optional(self, id):
        try:
            del self._available_optionals[id]
        except KeyError:
            pass

    def get_optional(self, key):
        return self._optional[key]

    def get_all_optionals(self):
        return copy(self._optional)

    def name(self, key):
        return getattr(self, '_' + key).name

    @utilities.Observable
    def set_job(self, job, single=False, **kwargs):
        job.add_data(kwargs)
        obj = job

        if self._job_buffer is not None:
            if obj == self._job_buffer:
                self._job = self._job_buffer
                self._job_buffer = None
                return

        obj.focus = 0

        if self._job is None:

            self._job = obj
            return

        if self._job.productivity > 0:
            self._job_buffer = self._job
        else:
            self._job_buffer = None

        self._job = obj

    def set(self, attr_name, obj, single=False, **kwargs):
        obj.single = single
        obj.add_data(kwargs)
        if attr_name == 'job':
            self.set_job(obj, single, **kwargs)
        else:
            setattr(self, '_' + attr_name, obj)

    def get(self, attr_name, id):
        return getattr(self, '_available_' + attr_name + 's')[id]

    def unlock(self, attr_name, value):
        getattr(self, '_available_' + attr_name + 's')[value.id] = value

    def remove(self, id_, attr_name):
        try:
            del getattr(self, '_available_' + attr_name + 's')[id_]
        except KeyError:
            pass

    def available_optionals(self, current_world):
        return [i for i in self._available_optionals.values()
                if i.world == current_world and
                i not in self._optional.values()]

    def available(self, attr_name, world):
        if attr_name == 'optional':
            return self.available_optionals(world)
        value = getattr(self, '_available_' + attr_name + 's')
        return [i for i in value.values() if i.world == world]

    def get_schedule_object(self, type, world, id):
        return getattr(self, '_available_' + type + 's')(world).get(id)
