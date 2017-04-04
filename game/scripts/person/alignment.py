import renpy.store as store
import renpy.exports as renpy


class Alignment(object):
    """Controlls alignment of a person"""
    # Strongly coupled with relations
    _orderliness = {-1: "chaotic", 0: "conformal", 1: "lawful"}
    _activity = {-1: "timid", 0: "reasonable", 1: "ardent"}
    _morality = {-1: "evil", 0: "selfish", 1: "good"}

    relation_binding = {'activity': 'fervor',
                        'morality': 'congruence', 'orderliness': 'distance'
                        }

    _chance_names = {
        'morality': {
            -1: ('powerful', 'mean'),
            1: ('nice', 'spineless')
        },
        'orderliness': {
            -1: ('independent', 'scandalous'),
            1: ('respectable', 'detached')
        },
        'activity': {
            -1: ('compose', 'insignificant'),
            1: ('drive', 'intrusive')
        }
    }

    def __init__(self):
        # All alignment axis have numeric and string representation
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
            raise Exception(
                "Orderliness set with string value, but %s is not valid for this axis" % (value))
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
            raise Exception(
                "Activity set with string value, but %s is not valid for this axis" % (value))
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
            raise Exception(
                "Morality set with string value, but %s is not valid for this axis" % (value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._morality = value

    def show_orderliness(self):
        return store.alignments_translation['orderliness'][self.orderliness]

    def show_activity(self):
        return store.alignments_translation['activity'][self.activity]

    def show_morality(self):
        return store.alignments_translation['morality'][self.morality]

    def description(self):
        return self.show_orderliness(), self.show_activity(), self.show_morality()

    # string representation of axis
    def orderliness_str(self):
        return Alignment._orderliness[self.orderliness]

    def morality_str(self):
        return Alignment._morality[self.morality]

    def activity_str(self):
        return Alignment._activity[self.activity]

    def get_chance_name(self, axis, kind, fake_value=None):
        # chances used in Taro mini game, achieved by morality system
        value = getattr(self, axis) if fake_value is None else fake_value
        kind_value = {'good': 0, 'bad': 1}[kind]
        name = self._chance_names[axis][value][kind_value]
        return name
