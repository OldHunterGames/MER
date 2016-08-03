import collections


class Modifier(object):
    def __init__(self, name, stats_dict, source, slot=None):
        self.name = name
        self.stats = stats_dict
        self.source = source
        self.slot = slot
    def description(self):
        pass

class ModifiersStorage(object):
    def __init__(self):
        self._list = []
    
    def get_modifiers_separate(self, attribute):
        values = []
        slotted = collections.defaultdict(list)
        for mod in self._list:
            if attribute in mod.stats.keys():
                if mod.slot == None:
                    values.append(mod)
                else:
                    slotted[mod.slot].append(mod)
        for list_ in slotted.values():
            max_ = 0
            modifier = None
            for mod in list_:
                if abs(mod.stats[attribute]) > abs(max_):
                    modifier = mod
                    max_ = mod.stats[attribute]
            values.append(mod)
        return values
    
    def count_modifiers_separate(self, attribute):
        return [mod.stats[attribute] for mod in self.get_modifiers_separate(attribute)]
    
    def count_modifiers(self, attribute):
        list_ = self.count_modifiers_separate(attribute)
        return sum(list_)
    
    def remove_modifier(self, source):
        to_remove = []
        for mod in self._list:
            if mod.source == source:
                to_remove.append(mod)
        for mod in to_remove:
            self._list.remove(mod)


    def get_all(self):
        return [mod.description for mod in self._list]


    def add_modifier(self, name, stats_dict, source, slot=None):
        self._list.append(Modifier(name, stats_dict, source, slot))


    def get_modifier(self, name):
        for mod in self._list:
            if mod.name == name:
                return mod
        return None
