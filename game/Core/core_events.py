
from random import *
from mer_events import *
import renpy.store as store
import renpy.exports as renpy
import sys
import inspect


# TODO: The list of all events should be generated dynamically
# def list_of_core_events():
#    return inspect.getmembers(sys.modules[__name__], inspect.isclass)


class EVUnique(Event):
    """
    Unique event for test
    """

    def __init__(self, env):
        super(EVUnique).__init__(env)
        self.natures = ["triggered", "turn_end", "faction"]
        self.goto = "evn_unic"
        self.unique = True


class EVGeneric(Event):
    """
    Generic event for test
    """

    def __init__(self, env):
        super(EVGeneric).__init__(env)
        self.goto = "evn_1"
        self.natures = ["triggered", "turn_end", "faction"]


