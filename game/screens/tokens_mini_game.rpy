label lbl_tokens_game(tokens_game):
    call screen sc_tokens_game(tokens_game)
    return


screen sc_tokens_game(tokens_game):
    python:
        colors = [(1, 0, 0), (1, 0, 1), (0, 1, 1), (0, 0, 1), (0, 1, 0), (0.85, 0.64, 0.12)]
    window:
        xfill True
        yfill True
        window:
            image im.Scale('images/tarot/card_table.jpg', 1280, 720)
            xalign 0.5
            yalign 0.0
            yfill False
            xsize 1280
            ysize 720

            hbox:
                yalign 0.5
                xalign 0.5
                spacing 10
                if not tokens_game.roll_phase:
                    imagebutton:
                        if tokens_game.free_turn > 0:
                            idle im.Scale('images/tarot/arcana_judgement.jpg', 300, 480)
                        else:
                            idle im.MatrixColor(im.Scale('images/tarot/card_draw.jpg', 300, 480), im.matrix.tint(*colors[tokens_game.chances]))
                        insensitive im.Grayscale(im.Scale('images/tarot/card_draw.jpg', 300, 480))
                        action [Function(tokens_game.start_rolling),
                            SensitiveIf(tokens_game.chances > -1 or tokens_game.free_turn > 0)]
                else:
                    for i in range(0, 3):
                        $ value = tokens_game.revolver[i]
                        $ card = value[0]
                        $ revealed = value[2]
                        $ locked = tokens_game.is_locked(i)
                        $ key = i
                        if tokens_game.roll_phase:
                            if revealed:
                                vbox:
                                    imagebutton:
                                        idle im.Scale(card.image, 300, 480)
                                        hover im.MatrixColor(im.Scale(card.image, 300, 480), im.matrix.brightness(0.05))
                                        insensitive im.Grayscale(im.Scale(card.image, 300, 480))
                                        action Function(tokens_game.use_card, i), SensitiveIf(not locked)
                                    text card.encolor_name():
                                        xalign 0.5
                            else:
                                imagebutton:
                                    idle im.Scale('images/tarot/card_back.jpg', 300, 480)
                                    hover im.MatrixColor(im.Scale('images/tarot/card_back.jpg', 300, 480), im.matrix.brightness(0.05))
                                    insensitive im.Grayscale(im.Scale('images/tarot/card_back.jpg', 300, 480))
                                    action Function(tokens_game.open_card, i), SensitiveIf(not locked)
    if not tokens_game.roll_phase:
        vbox:
            xalign 0.5
            yalign 1.0
            
            if tokens_game.free_turn <= 0:
                textbutton 'Done':
                    action Return()
                    xsize 200



init python:
    import collections
    class TokensGame(object):


        def __init__(self, person):
            self.roll_phase = False
            self.failed = False
            self.person = person
            self.revolver = [[None, False, False], [None, False, False], [None, False, False]]
            self.free_turn = 0
            renpy.call_in_new_context('lbl_tokens_game', self)


        @property
        def chances(self):
            return self.person.energy

        def start_rolling(self):
            self.roll_phase = True
            self.failed = False
            if self.free_turn <= 0:

                self.person.drain_energy()
            else:
                self.free_turn -= 1
            self.fill_revolver()

        def fill_revolver(self):
            cards = [i for i in self.person.resources_deck if i.active_if(self)]
            shuffle(cards)
            self.revolver[0][0] = cards[0]
            self.revolver[1][0] = cards[1]
            self.revolver[2][0] = cards[2]


        def stop_rolling(self):
            self.roll_phase = False

        def clear(self):
            self.revolver = [[None, False, False], [None, False, False], [None, False, False]]
            self.stop_rolling()
            if self.free_turn > 0:
                self.start_rolling()
            if self.chances < 0 and self.free_turn <= 0:
                renpy.return_statement()

        def is_locked(self, slot):
            return self.revolver[slot][1]

        def open_card(self, slot):
            self.revolver[slot][2] = True
            card = self.revolver[slot][0]
            if card.locker:
                for i in self.revolver:
                    if i[0] != card:
                        i[1] = True
            if not card.sensitive:
                self.revolver[slot][1] = True

        def use_card(self, slot):
            self.revolver[slot][0].activate(self)
            self.clear()


    class TaroCard(object):


        def __init__(self, name='', image=None, attribute='any', value=0, mood=None, activate=None,
                locker=False, sensitive=True, nature='good'):
            self.name = name
            self.image = image
            self.attribute = attribute
            self.value = value
            self._activate = activate
            self.mood = mood
            self.locker = locker
            self.sensitive = sensitive
            self.type = 'common'
            self.nature = nature

        def activate(self, taro_game):
            if self._activate is None:
                taro_game.person.activate_resource(self)
            else:
                self._activate(taro_game)

        def active_if(self, taro_game):
            if self.name == 'death':
                return taro_game.person.anxiety > 0
            if self.mood is None:
                if self.attribute != 'any' and self.attribute is not None:
                    attr = getattr(taro_game.person, self.attribute)
                    return attr >= self.value
                else:
                    return True
            return taro_game.person.mood >= self.mood

        def display_name(self):
            if self.type == 'common':
                return taro_common[self.name][self.value]['name']
            else:
                return taro_arcanas[self.name]['name']

        def encolor_name(self):
            if self.nature == 'good':
                value = self.value
                if value == 0:
                    value = 4
                return encolor_text(self.display_name(), value)
            elif self.nature == 'bad':
                return encolor_text(self.display_name(), 'red')
            else:
                return self.display_name()

    def temperance_activate(taro_game):
        taro_game.person.gain_energy()

    def judgement_activate(taro_game):
        taro_game.free_turn += 1

    def hangman_activate(taro_game):
        pass

    def devil_activate(taro_game):
        while taro_game.person.energy > -1:
            taro_game.person.drain_energy()

    def death_activate(taro_game):
        person = taro_game.person
        cards = [i for i in person.active_resources]
        for i in cards:
            person.use_resource(i)
        devil_activate(taro_game)

    default_taro_cards = {"swords": 'physique', 'wands': 'spirit', 'pentacles': 'mind', 'cups': 'agility'}
    taro_suffix = [None, 'slave', 'overseer', 'mistress', 'master', 'ace']

    special_taro_cards = {
        'temperance': {'activate': temperance_activate, 'image': 'images/tarot/arcana_temperance.jpg', 'nature': 'neutral'},
        'judgement': {'activate': judgement_activate, 'image': 'images/tarot/arcana_judgement.jpg', 'locker': True, 'nature': 'neutral'},
        'fool': {'sensitive': False, 'image': 'images/tarot/arcana_fool.jpg', 'nature': 'neutral'},
        'fortune': {'image': 'images/tarot/arcana_fortune.jpg', 'nature': 'good', 'attribute': None},
        'mage': {'value': 5, 'attribute': 'any', 'image': 'images/tarot/arcana_mage.jpg', 'nature': 'good'},
        'sun': {'value': 5, 'attribute': 'any', 'mood': 5, 'image': 'images/tarot/arcana_sun.jpg', 'nature': 'good'},
        'emperor': {'value': 4, 'attribute': 'any', 'mood': 4, 'image': 'images/tarot/arcana_emperor.jpg', 'nature': 'good'},
        'empress': {'value': 3, 'attribute': 'any', 'mood': 4, 'image': 'images/tarot/arcana_empress.jpg', 'nature': 'good'},
        'hangman': {'locker': True, 'activate': hangman_activate, 'image': 'images/tarot/arcana_hangman.jpg', 'nature': 'bad'},
        'devil': {'mood': 0, 'activate': devil_activate, 'image': 'images/tarot/arcana_devil.jpg', 'locker': True, 'nature': 'bad'},
        'death': {'locker': True, 'activate': death_activate, 'image': 'images/tarot/arcana_death.jpg', 'nature': 'bad'}

    }

    def init_taro(player):
        for key, value in default_taro_cards.items():
            for i in range(1, 6):
                player.resources_deck.append(TaroCard(key, 'images/tarot/%s_%s.jpg'%(key, taro_suffix[i]), value, i))
        for key, value in special_taro_cards.items():
            card = TaroCard(key, **value)
            card.type = 'arcana'
            player.resources_deck.append(card)

label lbl_jackpot:
    python:
        player.anxiety = 0
        player.add_buff('epic_luck')
    '!!JACKPOT!!'
