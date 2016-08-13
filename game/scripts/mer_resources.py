class Resources(object):
    def __init__(self):
        self.resources = {'drugs': 0, 'provision': 0, 'fuel': 0, 'munition': 0, 'hardware': 0, 'clothes': 0}
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
    

    def consumption_remove(self, name):
        for res in self._resources_consumption:
            if res[3] == name:
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
