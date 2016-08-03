class Alignment(object):
    _needs = {'orderliness': {-1: 'independence', 1:'stability'},
            'activity': {-1: 'approval', 1: 'trill'},
            'morality': {-1: 'power', 1: 'altruism'}
            }

    _orderliness = {-1: "chaotic", 0: "conformal", 1: "lawful"}
    _activity = {-1: "timid", 0: "reasonable", 1: "ardent"}
    _morality = {-1: "evil", 0: "selfish", 1: "good"}
    _relation_binding = {'activity': 'fervor', 'morality': 'congruence', 'orderliness': 'distance'}
    def __init__(self):
        self._orderliness = 0
        self._activity = 0
        self._morality = 0
    
    @property
    def orderliness(self):
        return self._orderliness
    @orderliness.setter
    def orderliness(self, value):
        if isinstance(value, str):
            for k, v in Alignment._orderliness.items():
                if v == value:
                    self._orderliness = k
                    return
            raise Exception("Orderliness set with string value, but %s is not valid for this axis"%(value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._orderliness = value

    
    @property
    def activity(self):
        return self._activity
    @activity.setter
    def activity(self, value):
        if isinstance(value, str):
            for k, v in Alignment._activity.items():
                if v == value:
                    self._activity = k
                    return
            raise Exception("Activity set with string value, but %s is not valid for this axis"%(value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._activity = value
    

    @property
    def morality(self):
        return self._morality
    @morality.setter
    def morality(self, value):
        if isinstance(value, str):
            for k, v in Alignment._morality.items():
                if v == value:
                    self._morality = k
                    return
            raise Exception("Morality set with string value, but %s is not valid for this axis"%(value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._morality = value


    def show_orderliness(self):
        return Alignment._orderliness[self.orderliness]
    def show_activity(self):
        return Alignment._activity[self.activity]
    def show_morality(self):
        return Alignment._morality[self.morality]

    def description(self):
        return self.show_orderliness(), self.show_activity(), self.show_morality()


    def special_needs(self):
        n = Alignment._needs
        needs = []
        zero_needs = []
        default = []
        for k in n.keys():
            try:
                val = getattr(self, k)
                needs.append(n[k][val])
                zero_needs.append(n[k][val - val*2])
            except KeyError:
                for val in n[k].values():
                    default.append(val)
        return needs, zero_needs, default