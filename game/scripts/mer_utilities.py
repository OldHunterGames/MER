# -*- coding: <UTF-8> -*-


def encolor_text(text, value):
    if value < 0:
        value = 0
    if value > 6:
        value = 6
    colors = ['ff0000', 'ff00ff', '00ffff',
              '0000FF', '00ff00', 'DAA520', '000000']
    return '{b}{color=#%s}%s{/color}{/b}' % (colors[value], text)

def default_avatar_path():
    return 'images/avatar/none.jpg'

class Observable(object):


        def __init__(self, func, instance=None, observers=None):
            self.func = func
            self.instance = instance
            self.observers = [] if observers is None else observers

        def __get__(self, obj, cls=None):
            if obj is None:
                return self
            else:
                func = self.func.__get__(obj, cls)
            return Observable(func, obj, self.observers)

        def __call__(self, *args, **kwargs):
            result = self.func(*args, **kwargs)
            for observer in self.observers:
                observer(self.instance)
            return result

        def add_callback(self, callback):
            self.observers.append(callback)
