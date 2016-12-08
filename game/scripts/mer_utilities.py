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