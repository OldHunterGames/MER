import collections


class Modifier(object):
    """Used to modify any numeric attribute of holder"""
    def __init__(self, name, attribute, value, source, slot=None):
        self.name = name
        self.attribute = attribute
        self.value = value
        self.source = source
        self.slot = slot

    def description(self):
        pass


class ModifiersStorage(object):

    def __init__(self):
        self._list = []

    def get_modifier_separate(self, attribute):
        # obsolete?
        values = []
        slotted = collections.defaultdict(list)
        for mod in self.get_all_modifiers():
            if attribute == mod.attribute:
                if mod.slot is None:
                    values.append(mod)
                else:
                    slotted[mod.slot].append(mod)
        for list_ in slotted.values():
            max_ = 0
            modifier = None
            for mod in list_:
                if abs(mod.value) > abs(max_):
                    modifier = mod
                    max_ = mod.value
            values.append(mod)
        return values

    def count_modifier_separate(self, attribute):
        return [mod.value for mod in self.get_modifier_separate(attribute)]

    def count_modifiers(self, attribute):
        list_ = self.count_modifier_separate(attribute)
        return sum(list_)

    def remove_modifier(self, source):
        to_remove = []
        for mod in self.get_all_modifiers():
            if mod.source == source:
                to_remove.append(mod)
        for mod in to_remove:
            self._list.remove(mod)

    def get_all(self):
        return [mod.description for mod in self.get_all_modifiers()]

    def add_modifier(self, name, stats_dict, source, slot=None):
        for key in stats_dict:
            attribute = key
            value = stats_dict[key]
            self._list.append((Modifier(name, attribute, value, source, slot)))

    def get_all_modifiers(self):
        return self._list


class Modifiable(object):
    # Interface for modifiable objects
    # maybe rewrite this as fully interface-like class
    # without init 'dirty' hack?
    def init_modifiable(self):
        self._modifiers = ModifiersStorage()

    def remove_modifier(self, source):
        self._modifiers.remove_modifier(source)

    def add_modifier(self, id_, stats_dict, source, slot=None):
        self._modifiers.add_modifier(id_, stats_dict, source, slot)

    def count_modifiers(self, key):
        # any numeric attribute can be modified with modifiers
        # should be used in attribute get func or property
        val = self.__dict__['_modifiers'].count_modifiers(key)
        return val

    def modifiers_separate(self, modifier):
        # obsolete?
        return self._modifiers.get_modifier_separate(modifier)

    def get_all_modifiers(self):
        return self._modifiers.get_all_modifiers()
