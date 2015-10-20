import renpy.store as store
import renpy.exports as renpy


class OWVillage(object):
    def __init__(self):
        self.name = "VillageWorld"
        self.visited = False
        self.point_of_arrival = "owvillage_gates"