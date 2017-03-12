import renpy.exports as renpy
import renpy.store as store


class Quest(object):

    def __init__(self, employer=None, one_time=False, *args, **kwargs):
        self.employer = employer
        self._data = kwargs
        self._one_time = one_time
        self._completed = 0

    def description(self):
        no_desc = 'No description'
        return self._data.get('description', no_desc)

    def name(self):
        name = 'Unnamed'
        return self._data.get('name', name)

    def end_label(self):
        return self._data['end_label']

    def check(self, performer):
        raise Exception("Not implemented")

    def finish(self, performer):
        finished = self._finish(performer)
        if finished:
            self._completed += 1

    def _finish(self, performer):
        finished = renpy.call_in_new_context(self.end_label, self, performer)
        return finished

    def available(self, performer):
        if self._one_time:
            if self._completed > 0:
                return False
        else:
            return self._available(performer)

    def _available(self, performer):
        raise Exception("Not implemented")

    def __getattr__(self, key):
        try:
            value = self._data[key]
        except KeyError:
            raise AttributeError(key)
        else:
            return value


class SlaverQuest(Quest):

    def __init__(self, allure=4, *args, **kwargs):
        super(SlaverQuest, self).__init__(*args, **kwargs)
        self.allure = allure

    def check(self, performer):
        for i in performer.slaves:
            if i.allure() >= self.allure:
                return True
        return False

    def get_available_slaves(self):
        return [i for i in self.performer.slaves if i.allure() >= self.allure]


class BringBars(Quest):

    def __init__(self, bars=5, *args, **kwargs):
        super(BringBars, self).__init__(*args, **kwargs)
        self.bars = bars

    def check(self, performer):
        return performer.money >= self.bars

    def _available(self, performer):
        return True


class BasicRelationsQuest(BringBars):

    def __init__(self, axis, *args, **kwargs):
        super(BasicRelationsQuest, self).__init__(*args, **kwargs)
        self.axis = axis

    def _available(self, performer):
        relations = performer.relations(self.employer)
        return relations.active(self.axis)
