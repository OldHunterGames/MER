class Resources(object):
    def __init__(self):
        self.resources = {'drugs': 0, 'provision': 0, 'weapon': 0}
        self.money = 0
        self._resources_consumption = []
    def __getattr__(self, key):
        try:
            attr = self.resources[key]
            return attr
        except KeyError:
            raise AttributeError(key)
    def __setattr__(self, key, value):
        try:
            self.__dict__['resources'][key] = value
        except KeyError:
            super(Resources, self).__setattr__(key, value)
    @property
    def money(self):
        return self.resources['money']
    
    @money.setter
    def money(self, value):
        if not value < 0:
            self.resources['money'] = value
    
    @property
    def provision_consumption(self):
        return self.consumption('provision')
    
    @property
    def drugs(self):
        return self.resources['drugs']
    
    @drugs.setter
    def drugs(self, value):
        if not value < 0:
            self.resources['drugs'] = value
    
    @property
    def provision(self):
        return self.resources['provision']
    
    @provision.setter
    def provision(self, value):
        if not value < 0:
            self.resources['provision'] = value


    def consumption(self, res):
        value = 0
        for i in self._resources_consumption:
            if i[0] == res:
                try:
                    value += i[1]()
                except TypeError:
                    value += i[1]
        return value
    

    def consumption_remove(self, name):
        for i in self._resources_consumption:
            if i[3] == name:
                self.resources.remove(i)

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
    

    def res_to_money(self, res, exchange_rate=1):# exchange rate is amount of money you should pay for 1 unit of resource
        rate = exchange_rate
        resource = self.resources[res]-self.consumption(res)
        return -(resource)*rate
    
    def consumption_remove_by_name(self, name):
        for res in self._resources_consumption:
            if res[3] == name:
                self._resources_consumption.remove(res)
    def add_consumption(self, name, res, value, time=1):
        self.consumption_remove_by_name(name)
        self._resources_consumption.append([res, value, time, name])
    


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
