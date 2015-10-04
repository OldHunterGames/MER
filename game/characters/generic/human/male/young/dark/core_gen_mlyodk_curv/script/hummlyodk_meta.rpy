init python:
    from mer_metaperson import *
    from random import *

    class Hummlyodk1(MetaPerson):
        meta_code = 'hummlyodk'
        def __init__(self):
            self.name = choice(("Derek", "Ben"))
            self.sparks = 100
            self.chakra = 4


    class Hummlyodk2(MetaPerson):
        meta_code = 'hummlyodk'
        def __init__(self):
            self.name = choice(("Kennie", "John"))
            self.sparks = 35
            self.chakra = 2
