# -*- coding: UTF-8 -*-
class Resources(object):

    def __init__(self):
        self.resources = {'drugs': 0, 'provision': 0,
                          'fuel': 0, 'munition': 0, 'hardware': 0, 'clothes': 0}
        self._money = 0
        self._resources_consumption = []

    def __getattr__(self, key):
        try:
            attr = self.__dict__['resources'][key]
            return attr
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if 'resources' in self.__dict__:
            if key in self.__dict__['resources']:
                self.__dict__['resources'][key] = max(0, value)
                return
        super(Resources, self).__setattr__(key, value)

    def increase(self, resource, value):
        new_value = value + getattr(self, resource)
        setattr(self, resource, new_value)

    def decrease(self, resource, value):
        new_value = -value + getattr(self, resource)
        setattr(self, resource, new_value)

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        self._money = max(0, value)

    @property
    def provision_consumption(self):
        return self.consumption('provision')

    def consumption(self, res):
        value = 0
        for i in self._resources_consumption:
            if i[0] == res:
                try:
                    value += i[1]()
                except TypeError:
                    value += i[1]
        return value

    def consumption_remove(self, source, slot):
        for res in self._resources_consumption:
            if res[3] == source and res[4] == slot:
                self._resources_consumption.remove(res)

    def consumption_tick(self):
        to_remove = []
        for i in self._resources_consumption:
            try:
                i[2] -= 1
                if i[2] < 1:
                    to_remove.append(i)
            except TypeError:
                pass
        for i in to_remove:
            self._resources_consumption.remove(i)

    # exchange rate is amount of money you should pay for 1 unit of resource
    def res_to_money(self, res, exchange_rate=1):
        rate = exchange_rate
        resource = self.resources[res] - self.consumption(res)
        return -(resource) * rate

    def consumption_remove_by_source(self, source):
        for res in self._resources_consumption:
            if res[3] == source:
                self._resources_consumption.remove(res)

    def add_consumption(self, source, res, value, time=1, slot=None):
        if slot is not None:
            self.consumption_remove(source, slot)
        self._resources_consumption.append([res, value, time, source, slot])

    def has_money(self, value):
        if self.money >= value:
            return True
        else:
            return False

    def can_consume(self, res):
        if self.resources[res] - self.consumption(res) >= 0:
            return True
        else:
            return False

    def is_deficit(self, res):
        if self.consumption(res) > self.resources[res]:
            return True
        return False

    def consume(self):
        for res in self.resources.keys():
            if self.can_consume(res):
                self.resources[res] -= self.consumption(res)
            elif self.has_money(self.res_to_money(res)):
                self.resources[res] = 0
                self.use_money(self.res_to_money(res))

    def to_zero(self):
        for res in self.resources.keys():
            self.resources[res] = 0


class Consumption(object):


    def __init__(self, source, name, value, slot, time=1, description=""):
        self.source = source
        self.name = name
        self._value = value
        self.slot = slot
        self.time = time

    @property
    def value(self):
        try:
            value = self._value()
        except TypeError:
            value = self._value
        return value
    
    def tick_time(self):
        try:
            self.time -= 1
        except TypeError:
            pass


class BarterSystem(object):


    def __init__(self):
        self._value = 0
        self._tendency = 0
        self._consumptions_list = []

    @property
    def tendency(self):
        return self._tendency

    def increase_tendency(self):
        if self._tendency > 0:
            self.value += 1
            self._tendency = 0
        else:
            self._tendency += 1

    def decrease_tendency(self):
        if self._tendency < 0:
            self.value -= 1
            self._tendency = 0
        else:
            self._tendency -= 1

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = max(0, min(value, 5))

    def income(self, value):
        if value < self.value:
            return
        elif value > self.value:
            self.value = value
            self._tendency = 0
        else:
            self.increase_tendency()

    def spend(self, value):
        difference = self.value - value
        if difference >= 3 or value == 0:
            return
        elif difference == 2:
            self.decrease_tendency()
        elif difference == 1:
            self.value -= 1
            self._tendency = 0
        elif difference == 0:
            self._value = 0
            self._tendency = 0

    def can_spend(self, value):
        if value > self.value:
            return False
        return True

    def add_consumption(self, source, name, value, slot, time=1, description=""):
        self.remove_consumption(source, slot)
        self._consumptions_list.append(Consumption(source, name, value, slot, time, description))

    def remove_consumption(self, source, slot):
        for i in self._consumptions_list:
            if i.source == source and i.slot==slot:
                self._consumptions_list.remove(i)
                break

    def remove_all_with_source(self, source):
        to_remove = []
        for i in self._consumptions_list:
            if i.source == source:
                to_remove.append(i)
        for i in to_remove:
            self._consumptions_list.remove(i)
        
    def tick_time(self):
        to_remove = []
        for i in self._consumptions_list:
            i.tick_time()
            try:
                if i.time < 0:
                    to_remove.append(i)
            except TypeError:
                pass
        for i in to_remove:
            self._consumptions_list.remove(i)
        self.spend(self._get_max_consumption())

    def _get_consumptions_list(self):
        return [i for i in self._consumptions_list]

    def calculate_consumption(self, value):
        if value == 0:
            return 4
        difference = self.value - value
        if difference >= 3:
            return 4
        elif difference == 2:
            return 3
        elif difference == 1:
            return 2
        elif difference == 0:
            return 1
        else:
            return 0

    def _get_max_consumption(self):
        consumptions = [i.value for i in self._get_consumptions_list()]
        try:
            max_consumption = max(consumptions)
        except ValueError:
            max_consumption = 0
        return max_consumption
    
    """
    def can_tick(self):
        simulation = BarterSystem()
        simulation._value = self.value
        simulation._tendency = self.tendency
        consumptions = [i.value for i in self.get_consumptions_list()]
        consumptions.sort()
        for i in consumptions:
            if simulation.can_spend(i):
                simulation.spend(i)
            else:
                return False
        return True
    """
    def can_tick(self):
        if self.can_spend(self._get_max_consumption()):
            return True
        return False

    def consumption_level(self):
        return self.calculate_consumption(self._get_max_consumption())