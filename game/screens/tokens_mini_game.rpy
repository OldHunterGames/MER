label lbl_tokens_game(tokens_game):
    call screen sc_chances(tokens_game)
    return

screen sc_chances(tokens_game):
    $ chances = tokens_game.person.chances_left()
    window:
        xfill True
        yfill True  
        vbox:
            xalign 0.0
            xmaximum 400
            ymaximum 500
            image im.Scale('images/tarot/card_back.jpg', 300, 400)
            text 'Cards: %s'%chances:
                xalign 0.5
        vbox:
            xalign 1.0
            imagebutton:
                idle im.Scale('images/tarot/card_back.jpg', 300, 400)
                hover im.MatrixColor(im.Scale('images/tarot/card_back.jpg', 300, 400), im.matrix.brightness(0.05))
                action Function(tokens_game.start_rolling)
            python:
                chance = tokens_game.active_chance
                chance_value = tokens_game.chance_value
                txt = encolor_text(chance.id, chance_value)
            text txt:
                xalign 0.5
        textbutton 'Leave':
            xalign 0.5
            yalign 1.0
            action Return()


screen sc_tokens_game(tokens_game):
    modal True
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
            ysize 420

            hbox:
                yalign 0.5
                xalign 0.5
                spacing 10
                for i in range(0, len(tokens_game.revolver)):
                    python:
                        value = tokens_game.revolver
                        card = value[i]
                        key = i
                    if tokens_game.roll_phase:
                        vbox:
                            imagebutton:
                                idle im.Scale(card.image, 300, 480)
                                hover im.MatrixColor(im.Scale(card.image, 300, 480), im.matrix.brightness(0.05))
                                insensitive im.Grayscale(im.Scale(card.image, 300, 480))
                                action Function(tokens_game.use_card, i), Hide('sc_tokens_game')
                                hovered Show('sc_taro_description', card=card)
                                unhovered Hide('sc_taro_description')
                            text card.encolor_name():
                                xalign 0.5
    on 'hide':
        action Hide('sc_taro_description')

screen sc_taro_description(card):
    frame:
        xmaximum 400
        xalign 0.5
        yalign 1.0
        text card.display_description()


init python:
    import collections
    class TokensGame(object):


        def __init__(self, person):
            self.roll_phase = False
            self.failed = False
            self.person = person
            self.chance = None
            self.chance_value = None
            self.blocked = False
            self.revolver = []
            self.free_turn = 0
            self.get_chance()

        def start(self):
            renpy.call_in_new_context('lbl_tokens_game', self)


        def get_chance(self):
            person = self.person
            chance = choice(person.get_all_chances())
            self.chance = chance
            person.remove_chance(chance.id)
            self.active_chance = chance
            if chance.negative:
                self.chance_value = 3-chance.value
            else:
                self.chance_value = chance.value

        @property
        def chances(self):
            return self.person.energy

        def start_rolling(self):
            self.roll_phase = True
            self.failed = False
            self.fill_revolver()

        def fill_revolver(self):
            cards = [i for i in self.get_available_cards()]
            shuffle(cards)
            if self.chance_value <= 2:
                self.chance_value += 1
            for i in range(self.chance_value):
                self.revolver.append(cards[i])
            renpy.show_screen('sc_tokens_game', self)


        def stop_rolling(self):
            self.roll_phase = False

        def clear(self):
            self.revolver = []
            self.stop_rolling()

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
            self.revolver[slot].activate(self)
            self.clear()
            if self.person.chances_left() > 0 and not self.blocked:
                self.get_chance()
            else:
                self.chance = None
                renpy.return_statement()

        @classmethod
        def get_defaults(cls, person):
            defaults = []
            names = ["swords", 'wands', 'pentacles', 'cups']
            for name in names:
                for i in range(1, 6):
                    defaults.append('%s_%s'%(name, i))
            return [card for card in person.resources_deck if card.name in defaults and card.can_be_applied(person)]
        
        def get_available_cards(self):
            chance_value = self.chance_value
            negatives = ['hermit', 'fool', 'mage', 'fortune', 'hangman', 'devil', 'death']
            if chance_value < 3:
                return [card for card in self.person.resources_deck if card.name in negatives]
            else:
                defaults = self.get_defaults(self.person)
                valued = {
                    3: ['fool', 'mage', 'temperance', 'empress'],
                    4: ['fool', 'mage', 'emperor', 'justice'],
                    5: ['fool', 'mage', 'sun', 'pope', 'judgement']
                }
                defaults.extend(values[chance_value])
                return [card for card in self.person.resources_deck in card.name in defaults]

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

        def display_description(self):
            if self.type == 'common':
                return taro_commod[self.name][self.value]['description']
            else:
                return taro_arcanas[self.name]['description']

        def can_be_applied(self, person):
            if self.attribute != 'any':
                return getattr(person, self.attribute) >= self.value
            return True

        def available(self, attribute):
            if self.attribute == 'any':
                return True
            return self.attribute == attribute

    def temperance_activate(taro_game):
        person = taro_game.person
        if person.energy < 3:
            person.gain_energy()
        elif person.energy > 3:
            person.drain_energy()

    def judgement_activate(taro_game):
        taro_game.person.clear_chances()

    def hangman_activate(taro_game):
        taro_game.person.drain_energy(taro_game.person.energy)

    def devil_activate(taro_game):
        person = taro_game.person
        taro_game.blocked = True
        cards = [i for i in person.active_resources]
        for i in cards:
            person.use_resource(i)

    def death_activate(taro_game):
        person = taro_game.person
        taro_game.blocked = True
        person.drain_energy(person.energy)
        person.clear_chances(True)

    def pope_activate(taro_game):
        taro_game.person.gain_energy(3)

    def mage_activate(taro_game):
        taro_game.person.gain_energy(1)

    def justice_activate(taro_game):
        taro_game.person.gain_energy(2)

    default_taro_cards = {"swords": 'physique', 'wands': 'spirit', 'pentacles': 'mind', 'cups': 'agility'}
    taro_suffix = [None, 'slave', 'overseer', 'mistress', 'master', 'ace']

    special_taro_cards = {
        'temperance': {'activate': temperance_activate, 'image': 'images/tarot/arcana_temperance.jpg', 'nature': 'neutral'},
        'judgement': {'activate': judgement_activate, 'image': 'images/tarot/arcana_judgement.jpg', 'locker': True, 'nature': 'neutral'},
        'fool': {'sensitive': False, 'image': 'images/tarot/arcana_fool.jpg', 'nature': 'neutral'},
        'fortune': {'image': 'images/tarot/arcana_fortune.jpg', 'nature': 'good', 'attribute': 'luck'},
        'mage': {'attribute': 'any', 'image': 'images/tarot/arcana_mage.jpg', 'nature': 'good', 'activate': mage_activate},
        'sun': {'value': 5, 'attribute': 'any', 'mood': 5, 'image': 'images/tarot/arcana_sun.jpg', 'nature': 'good'},
        'emperor': {'value': 4, 'attribute': 'any', 'mood': 4, 'image': 'images/tarot/arcana_emperor.jpg', 'nature': 'good'},
        'empress': {'value': 3, 'attribute': 'any', 'mood': 4, 'image': 'images/tarot/arcana_empress.jpg', 'nature': 'good'},
        'hangman': {'locker': True, 'activate': hangman_activate, 'image': 'images/tarot/arcana_hangman.jpg', 'nature': 'bad'},
        'devil': {'mood': 0, 'activate': devil_activate, 'image': 'images/tarot/arcana_devil.jpg', 'locker': True, 'nature': 'bad'},
        'death': {'locker': True, 'activate': death_activate, 'image': 'images/tarot/arcana_death.jpg', 'nature': 'bad'},
        'hermit': {'value': 4, 'image': 'images/tarot/arcana_hermit.jpg', 'nature': 'good', 'attribute': 'any'},
        'pope': {'image': 'images/tarot/arcana_pope.jpg', 'nature': 'good', 'activate': pope_activate},
        'justice': {'image': 'images/tarot/arcana_justice.jpg', 'nature': 'good', 'activate': justice_activate}

    }

    def init_taro(player):
        for key, value in default_taro_cards.items():
            for i in range(1, 6):
                player.resources_deck.append(TaroCard(key+'_%s'%i, 'images/tarot/%s_%s.jpg'%(key, taro_suffix[i]), value, i))
        for key, value in special_taro_cards.items():
            card = TaroCard(key, **value)
            card.type = 'arcana'
            player.resources_deck.append(card)
