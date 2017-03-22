init python:
    
    class CardMenu(object):


        def __init__(self, cards_list, current=None, run_args=None, run_kwargs=None):

            self._cards_list = cards_list
            self.current_card = current
            if run_args is None:
                self.run_args = []
            else:
                self.run_args = run_args
            if run_kwargs is None:
                self.run_kwargs = {}
            else:
                self.run_kwargs = run_kwargs

        @property
        def cards_list(self):
            return [i for i in self._cards_list if i != self.current_card]

        def get_sorted(self):
            return sorted(self.cards_list, key=lambda card: card.name)

        def set_card(self, card):
            self.current_card = card

        def show(self, call=True):
            if call:
                renpy.call_screen('sc_card_menu', self, call)
            else:
                renpy.show_screen('sc_card_menu', card_menu=self, called=call)

        def run(self, card):
            return card.run(*self.run_args, **self.run_kwargs)


screen sc_card_menu(card_menu, called=True):
    modal True
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
                    action If(called, Return(), false=Hide('sc_card_menu'))
        if card_menu.current_card is not None:
            vbox:
                xpos 900
                xsize 380
                box_wrap True
                imagebutton:
                    idle im.Scale(card_menu.current_card.image(), 300, 400)
                    
                    action [Function(card_menu.run, card_menu.current_card),
                            If(called, Return(), false=Hide('sc_card_menu'))]
                    xalign 0.5
                text card_menu.current_card.description():
                    xalign 0.5
                    xmaximum 400