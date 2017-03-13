import renpy.exports as renpy
import renpy.store as store


class Quest(object):

    def __init__(self, one_time=False,
                 targets=None, *args, **kwargs):
        self._targets = []
        if targets is not None:
            self._targets.extend(targets)
        self._data = kwargs
        self._one_time = one_time
        self._completed = 0
        self.active = False

    def description(self):
        no_desc = 'No description'
        return self._data.get('description', no_desc)

    def add_target(self, quest_target):
        self._targets.append(quest_target)

    @property
    def targets(self):
        return [i for i in self._targets]

    def name(self):
        name = 'Unnamed'
        return self._data.get('name', name)

    def end_label(self):
        return self._data['end_label']

    def completed(self, performer):
        return all([i.completed(performer) for i in self._targets])

    def finish(self, performer):
        finished = self._finish(performer)
        if finished:
            self._completed += 1
        return finished

    def _finish(self, performer):
        finished = renpy.call_in_new_context(self.end_label(), self, performer)
        return finished

    def available(self, performer):
        if self._one_time:
            if self._completed > 0:
                return False
        else:
            return self._available(performer)

    def _available(self, performer):
        raise NotImplementedError()

    def __getattr__(self, key):
        try:
            value = self._data[key]
        except KeyError:
            raise AttributeError(key)
        else:
            return value


class QuestTarget(object):

    def __init__(self, *args, **kwargs):
        self._data = kwargs

    def name(self):
        name = 'Unnamed'
        return self._data.get('name', name)

    def description(self):
        no_desc = 'No description'
        return self._data.get('description', no_desc)

    def completed(self, performer):
        raise NotImplementedError()


class SlaverQuest(Quest):

    def __init__(self, allure=4, *args, **kwargs):
        super(SlaverQuest, self).__init__(*args, **kwargs)
        self.allure = allure

    def completed(self, performer):
        for i in performer.slaves:
            if i.allure() >= self.allure:
                return True
        return False

    def get_available_slaves(self):
        return [i for i in self.performer.slaves if i.allure() >= self.allure]


class BringBars(QuestTarget):

    def __init__(self, bars=5, *args, **kwargs):
        super(BringBars, self).__init__(*args, **kwargs)
        self.bars = bars

    def completed(self, performer):
        return performer.money >= self.bars

    def _available(self, performer):
        return True


class BasicRelationsQuest(Quest):

    def __init__(self, axis, point, *args, **kwargs):
        super(BasicRelationsQuest, self).__init__(*args, **kwargs)
        self.axis = axis
        self.point = point
        self.add_target(BringBars())

    def _available(self, performer):
        relations = performer.relations(self.employer)
        return (relations.active(self.axis) and
                relations.axis_str(self.axis) == self.point)

    def _finish(self, performer):
        performer.relations(self.employer).stance += 1
        performer.relations(self.employer).use(self.axis)
        return True
