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
        self.employes = None
        self.active = False

    def description(self):
        no_desc = 'No description'
        return self._data.get('description', no_desc)

    def activate(self):
        self._active = True
        self._activate()

    def _activate(self):
        return

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
        if self.employer is not None:
            self.employer.debt = True
        return True

    def available(self, performer):
        if self._one_time:
            if self._completed > 0:
                return False
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


class BringPerson(QuestTarget):

    def __init__(self, stats_dict, *args, **kwargs):
        self.stats = stats_dict

    def completed(self, performer):
        return any(self.get_available_slaves(performer))

    def get_available_slaves(self, performer):
        list_ = []
        for i in performer.slaves:
            for key, value in self.stats.items():
                if getattr(i, key) < value:
                    continue
            list_.append(i)
        return list_


class SlaverQuest(Quest):

    def __init__(self, *args, **kwargs):
        super(SlaverQuest, self).__init__(
            end_label='lbl_slaver_quest_end', *args, **kwargs)
        self.add_target(BringPerson({'allure': 4}))

    def _available(self, performer):
        relations = self.employer.relations(performer)
        axis = ['fervor', 'congruence', 'distance']
        return any([relations.active(i) for i in axis])

    def get_available_slaves(self, performer):
        return self.targets[0].get_available_slaves(performer)


class BringBars(QuestTarget):

    def __init__(self, bars=5, *args, **kwargs):
        super(BringBars, self).__init__(*args, **kwargs)
        self.bars = bars

    def completed(self, performer):
        return performer.money >= self.bars


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
        return True

    def _activate(self):
        self.employer.player_relations().use(self.axis)
