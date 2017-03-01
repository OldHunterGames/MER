# -*- coding: UTF-8 -*-
from mer_utilities import Observable

class Command(object):

    
    def _run(self):
        return NotImplemented

    @Observable
    def run(self):
        return self._run()

    @classmethod
    def add_observer(self, func):
        self.run.add_callback(func)


class SatisfySex(Command):


    def __init__(self, target, value):
        self.target = target
        self.value = value

    def _run(self):
        pass