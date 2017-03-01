# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy

from collections import OrderedDict
from copy import copy
import mer_utilities as utilities


class ScheduleObject(object):


    def __init__(self, id, data_dict):
        self._data = data_dict
        self.id = id
        self.locked = False
        self._additional_data = dict()

    def add_data(self, dict):
        self._additional_data = dict

    def _image_raw(self):
        return self._data.get('image', utilities.empty_card())

    def image(self, size=None):
        if size is None:
            size = (200, 300)
        return renpy.display.im.Scale(self._image_raw(), *size)
    
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

    def use(self, person, type):
        self._use(person)
        lbl = self.world+'_%s'%type+'_%s'%self.id
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
        self.focus = 0

    def _use(self, person):
        if self.skill is not None:
            if person.player_controlled:
                renpy.call_in_new_context('lbl_jobcheck', person=person, attribute=self.skill)
            else:
                renpy.call_in_new_context('lbl_jobcheck_npc', person=person, attribute=self.skill)


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
            getattr(self, 'set_' + type)(obj, **kwargs)

    def get_cost(self):
        return (self._accommodation.cost +
            self._ration.cost +
            sum([i.cost for i in self._optional.values() if i is not None]))

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
        return getattr(self, '_'+key).description

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

    def unlock_optional(self, id, schedule_object):
        self._available_optionals[id] = schedule_object

    def remove_optional(self, id):
        try:
            del self._available_optionals[id]
        except KeyError:
            pass

    def available_optionals(self, current_world):
        return [i for i in self._available_optionals.values() if i.world == current_world and
            i not in self._optional.values()]

    def get_optional(self, key):
        return self._optional[key]

    def get_all_optionals(self):
        return copy(self._optional)


    def name(self, key):
        return getattr(self, '_'+key).name

    @utilities.Observable
    def set_job(self, job, single=False, **kwargs):
        job.add_data(kwargs)
        difficulty = job.difficulty
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

    def set_accommodation(self, accommodation, single=False, **kwargs):
        self._set('_accommodation', accommodation, single, **kwargs)

    def set_ration(self, ration, single=False, **kwargs):
        self._set('_ration', ration, single, **kwargs)

    def _set(self, attr_name, obj, single=False, **kwargs):
        obj.single = single
        obj.add_data(kwargs)
        setattr(self, attr_name, obj)
    
    def _unlock(self, id_, attr_name, value):
        getattr(self, attr_name)[id_] = value

    def _remove(self, id_, attr_name):
        try:
            del getattr(self, attr_name)[id_]
        except KeyError:
            pass

    def _available(self, attr_name, world):
        value = getattr(self, attr_name)
        return [i for i in value.values() if i.world == world]
    
    def unlock_job(self, job_id, job_object):
        self._unlock(job_id, '_available_jobs', job_object)

    def remove_job(self, job_id):
        self._remove(job_id, '_available_jobs')

    def available_jobs(self, current_world):
        return self._available('_available_jobs', current_world)

    def unlock_accommodation(self, accommodation_id, schedule_object):
        self._unlock(accommodation_id, '_available_accommodations', schedule_object)

    def remove_accommodation(self, accommodation_id):
        self._remove(accommodation_id, '_available_accommodations')

    def available_accommodations(self, current_world):
        return self._available('_available_accommodations', current_world)

    def unlock_ration(self, ration_id, schedule_object):
        self._unlock(ration_id, '_available_rations', schedule_object)

    def remove_ration(self, ration_id):
        self._remove(ration_id, '_available_rations')

    def available_rations(self, current_world):
        return self._available('_available_rations', current_world)

    def get_schedule_object(self, type, world, id):
        return getattr(self, 'available_'+type+'s')(world).get(id)