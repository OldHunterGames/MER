init python:
    
    class CardMenu(object):


        def __init__(self, cards_list):

            self._cards_list = cards_list
            self.current_card = None

        @property
        def cards_list(self):
            return [i for i in self._cards_list if i != self.current_card]

        def get_sorted(self):
            return sorted(self.cards_list, key=lambda card: card.name)

        def set_card(self, card):
            self.current_card = card

        def show(self):
            renpy.call_screen('sc_card_menu', self)


screen sc_card_menu(card_menu):
    python:
        cards = card_menu.get_sorted()
    window:
        xfill True
        yfill True
        style 'character_info_window'

        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xmaximum 880
            hbox:
                xmaximum 880
                box_wrap True
                spacing 5
                for i in cards:
                    vbox:
                        imagebutton:
                            idle im.Scale(i.image(), 200, 300)
                            action Function(card_menu.set_card, i)
                        text i.name():
                            xalign 0.5
                imagebutton:
                    idle im.Scale(card_back(), 200, 300)
                    action Return()
        if card_menu.current_card is not None:
            vbox:
                xpos 900
                xsize 380
                box_wrap True
                imagebutton:
                    idle im.Scale(card_menu.current_card.image(), 300, 400)
                    
                    action Function(card_menu.current_card.run), Return()
                    xalign 0.5
                text card_menu.current_card.description():
                    xalign 0.5
                    xmaximum 400