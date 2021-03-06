# -*- coding: <UTF-8> -*-
import random
import renpy.store as store
import renpy.exports as renpy


def encolor_text(text, value, protected=False):
    if isinstance(value, str):
        colors = {'red': 'ff0000', 'green': '00ff00', 'cyan': '00ffff',
                  'gold': 'DAA520'}
    else:
        colors = ['ff0000', 'ff00ff', '00ffff',
                  '0000FF', '00ff00', 'DAA520', '000000']
        if value < 0:
            value = 0
        if value > 6:
            value = 6
    if not protected:
        return '{color=#%s}%s{/color}' % (colors[value], text)
    else:
        return '{{color=#%s}}%s{{/color}}' % (colors[value], text)


def get_files(path):
    files = renpy.list_files()
    return [i for i in files if path in i]


def default_avatar_path():
    return 'images/avatar/none.jpg'


def empty_card():
    return 'images/gui/blank_card.png'


def card_back():
    return 'images/tarot/card_back.jpg'


def empty_sex_image():
    return 'images/sexcards/blank.png'


def weighted_random(pairs):
    for i in pairs:
        try:
            iter(i)
        except TypeError:
            raise ValueError('weighted random takes pairs or dict as arg')
    try:
        pairs = pairs.items()
    except AttributeError:
        pass
    total = sum(w for c, w in pairs)
    r = random.uniform(0, total)
    upto = 0
    for c, w in pairs:
        if upto + w >= r:
            return c
        upto += w


def roll(value, max_):
    dice = random.randint(1, max_)
    if value < dice:
        return False
    return True


def change_needs(person, satisfy, tense, result):
    if result < 0:
        return
    for i in tense:
        getattr(person, i).set_tension()
    if result > 0:
        for i in satisfy:
            getattr(person, i).set_satisfaction(result)


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
            observer(self.instance, list(args), dict(**kwargs))
        return result

    def add_callback(self, callback):
        self.observers.append(callback)

    def remove_callback(self, callback):
        self.observers.remove(callback)


"""class DefaultObservable(object):

    def init_observable(self):
        self._observers = []

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, **kwargs):
        for i in self._observers:
            i.notify(**kwargs)"""


def sex_images_path():
    return 'images/sexcards'


def make_sex_card(quality, type_, contact_type, size=None):
    if size is None:
        size = (400, 600)
    qualities = {1: sex_images_path() + '/base_bronze.jpg',
                 2: sex_images_path() + '/base_silver.jpg',
                 3: sex_images_path() + '/base_gold.jpg'}
    quality_image = qualities[quality]
    types = {
        'bizarre': sex_images_path() + '/over_bizarre.png',
        'passionate': sex_images_path() + '/over_passion.png',
        'rough': sex_images_path() + '/over_rage.png',
        'tender': sex_images_path() + '/over_tender.png'
    }
    type_image = types[type_]
    image_start = sex_images_path() + '/%s' % contact_type
    images = [i for i in renpy.list_files() if i.startswith(image_start)]
    try:
        image = renpy.display.im.Scale(random.choice(images), *size)
        image = renpy.display.im.Composite(size,
                                           (0, 0), quality_image,
                                           (0, 0), image,
                                           (0, 0), type_image,)
    except IndexError:
        image = renpy.display.im.Scale(empty_sex_image(), *size)

    return image
