import renpy.exports as renpy
import renpy.store as store


class Quest(object):

    def __init__(self, one_time=False,
                 targets=None, reminder=False, *args, **kwargs):
        self._targets = []
        if targets is not None:
            self._targets.extend(targets)
        self._data = kwargs
        self._one_time = one_time
        self._completed = 0
        self._reminder = reminder
        self.employer = None
        self.active = False
        self.ending_tags = []
        self.tags = []

    @property
    def reminder(self):
        return self._reminder

    @property
    def one_time(self):
        return self._one_time

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
        if self.reminder:
            return False
        return all([i.completed(performer) for i in self._targets])

    def finish(self, performer):
        finished = self._finish(performer)
        if finished:
            self._completed += 1
            if self.employer is not None:
                self.employer.obligation = True
        for i in self._targets:
            i.finish(performer)
        return finished

    def _finish(self, performer):
        # override this in child classes
        return True

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

    def finish(self, performer):
        # override this in child classes
        return


class BringPerson(QuestTarget):

    def __init__(self, stats_dict, *args, **kwargs):
        self.stats = stats_dict

    def completed(self, performer):
        return any(self.get_available_slaves(performer))

    def get_available_slaves(self, performer):
        list_ = []
        for i in performer.slaves.slaves():
            for key, value in self.stats.items():
                if getattr(i, key) < value:
                    continue
            list_.append(i)
        return list_


class SlaverQuest(Quest):

    def __init__(self, *args, **kwargs):
        super(SlaverQuest, self).__init__(*args, **kwargs)
        self.add_target(BringPerson({'allure': 4}))

    def get_available_slaves(self, performer):
        return self.targets[0].get_available_slaves(performer)

    def _finish(self, performer):
        slave = performer.remove_slave()
        performer.forget_person(slave)
        return True


class BringBars(QuestTarget):

    def __init__(self, bars=5, *args, **kwargs):
        super(BringBars, self).__init__(*args, **kwargs)
        self.bars = bars

    def completed(self, performer):
        return performer.money >= self.bars

    def finish(self, performer):
        performer.remove_money(self.bars)


class SexualPleasure(QuestTarget):

    def __init__(self, pleasure=5):
        pass


class BasicRelationsQuest(Quest):

    def __init__(self, axis, point, *args, **kwargs):
        super(BasicRelationsQuest, self).__init__(*args, **kwargs)
        self.axis = axis
        self.point = point
        self.add_target(BringBars())

    def _finish(self, performer):
        performer.relations(self.employer).stance += 1
        return True

    def _activate(self):
        self.employer.player_relations().use(self.axis)


class BecomeSlave(QuestTarget):


    def __init__(self, *args, **kwargs):
        super(BecomeSlave, self).__init__(*args, **kwargs)

    def completed(self, performer):
        return performer.master is not None