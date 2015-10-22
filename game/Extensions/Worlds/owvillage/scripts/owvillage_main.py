import renpy.store as store
import renpy.exports as renpy
from mer_event import Event

class OWVillage(object):
    def __init__(self):
        self.name = "VillageWorld"
        self.visited = False
        self.point_of_arrival = "owvillage_gates"


class OWVillageTavernEvent(Event):
    def __init__(self, env):
        super(OWVillageTavernEvent, self).__init__(env)
        self.goto = 'owvillage_event'
        self.natures = ['triggered', 'special']
        