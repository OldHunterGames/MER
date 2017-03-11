import renpy.exports as renpy
import renpy.store as store


class Quest(object):

    def __init__(self, performer, employer, *args, **kwargs):
        self.performer = performer
        self.employer = employer
        self._data = kwargs

    def description(self):
        no_desc = 'No description'
        try:
            value = self._data.get('description', no_desc)
        except AttributeError:
            return no_desc
        else:
            return value

    def name(self):
        name = 'Unnamed'
        try:
            value = self._data.get('name', name)
        except AttributeError:
            return name
        else:
            return value

    def check(self):
        raise Exception("Not implemented")

    def finish(self):
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

    def check(self):
        for i in self.performer.slaves:
            if i.allure() >= self.allure:
                return True
        return False

    def finish(self):
        finished = renpy.call_in_new_context('lbl_slaver_quest_end', self)
        return finished

    def get_available_slaves(self):
        return [i for i in self.performer.slaves if i.allure() >= self.allure]


class BringBars(Quest):

    def __init__(self, bars=5, *args, **kwargs):
        super(BringBars, self).__init__(*args, **kwargs)
        self.bars = bars

    def check(self):
        return self.perfromer.money >= self.bars

    def finish(self):
        finished = renpy.call_in_new_context('lbl_bring_bars_end', self)
        return finished
