init python:
    
    class CardMenu(object):


        def __init__(self, cards_list, current=None, cancel=False):

            self._cards_list = cards_list
            self.current_card = current
            self.cancel = cancel

        @property
        def cards_list(self):
            return [i for i in self._cards_list if i != self.current_card]

        def get_sorted(self):
            return sorted(self.cards_list, key=lambda card: card.name)

        def set_card(self, card):
            current = self.current_card
            if current is not None and current not in self._cards_list:
                self._cards_list.append(self.current_card)
            self.current_card = card

        def show(self, call=True, x_size=200, y_size=300, spacing=5):
            call = True
            renpy.call_in_new_context('_lbl_card_menu', self, call, x_size, y_size, spacing, self.cancel)

        def run(self):
            card = self.current_card
            card.run()
            renpy.return_statement()
            

    class SellMenu(CardMenu):

        def run(self, card):
            self.current_card = None
            self._cards_list.remove(card)
            return card.run()

label _lbl_card_menu(card_menu, called=True, x_size=200, y_size=300, spacing_=5, cancel=False):
    call screen sc_card_menu(card_menu, called, x_size, y_size, spacing_, cancel)
    return


screen sc_card_menu(card_menu, called=True, x_size=200, y_size=300, spacing_=5, cancel=False):
    modal True
    python:
        cards = card_menu.get_sorted()
        card_menu.called = called
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
                spacing spacing_
                for i in cards:
                    vbox:
                        imagebutton:
                            idle im.Scale(i.image(), x_size, y_size)
                            action Function(card_menu.set_card, i)
                        text i.name():
                            xalign 0.5
                if cancel:
                    imagebutton:
                        idle im.Scale(card_back(), x_size, y_size)
                        action If(called, Return(), false=Hide('sc_card_menu'))
        if card_menu.current_card is not None:
            vbox:
                xpos 900
                xsize 380
                box_wrap False
                imagebutton:
                    idle im.Scale(card_menu.current_card.image(), x_size+100, y_size+100)
                    
                    action Function(card_menu.run)
                            
                    xalign 0.5
                viewport:
                    scrollbars 'vertical'
                    draggable True
                    mousewheel True
                    xmaximum 380
                    text card_menu.current_card.description():
                        xalign 0.5
                        xmaximum 380