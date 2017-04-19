init python:
    def withou_faction(player):
        return [i for i in player.known_characters if not i.has_faction()]

    class CardPerson(Card, Command):

        def __init__(self, person, player):
            self.person = person
            self.player = player

        def image(self):
            return self.person.avatar_path

        def name(self):
            return self.person.name

        def description(self):
            person = self.person
            line0 = person.name
            line1 = '{person.age} {person.gender} {person.genus.name}'.format(person=person)
            line2 = '{0} {1} {2}'.format(*person.alignment.description())
            sexual_suite = person.sexual_suite['name']
            orientation = person.sexual_orientation['name']
            line3 = '{0} {1}'.format(sexual_suite, orientation)
            line4 = DescriptionMaker(person).relations_text(protected=False)
            final_text = line0 + '\n' + line1 + '\n' + line2 + '\n' + line3 + '\n' + line4
            return final_text
        
        def run(self):
            renpy.call_in_new_context('_contacts_glue',
                self.person, True, True)       

label lbl_contacts(player):
    $ char_cards = [CardPerson(person, player) for person in player.known_characters]
    $ CardMenu(char_cards, cancel=True).show(True, 150, 150, 10)
    return

label _contacts_glue(person, _return=True, communicate=True):
    call screen sc_character_info_screen(person, _return, communicate)
    return

screen sc_player_contacts():
    modal True
    window:
        xfill True
        yfill True
        xalign 0.0
        yalign 0.0
        style 'char_info_window'
        frame:
            vbox:
                if player.owned_faction() is not None:
                        textbutton player.owned_faction().name:
                            action Show('sc_faction_info', faction=player.owned_faction())
                if any([i.type == 'major_house' for i in player.known_factions()]):
                    textbutton 'Major houses':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('major_house'))
                if any([i.type == 'guild' for i in player.known_factions()]):
                    textbutton 'Guilds':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('guild'))
                if any([i.type == 'minor_house' for i in player.known_factions()]):
                    textbutton 'Minor houses':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('minor_house'))
                if any([i.type == 'unbound' for i in player.known_factions()]) or any(without_faction(player)):
                    textbutton 'Unbound':
                        action Show('sc_list_factions', factions=core.get_factions_by_type('unbound'), show_others=True)
                textbutton 'Leave':
                    action Hide('sc_player_contacts'), Hide('sc_list_factions')

screen sc_list_factions(factions, show_others=False):
    frame:
        xalign 0.5
        vbox:
            for i in factions:
                if player.know_faction(i):
                    textbutton i.name:
                        action Show('sc_faction_info', faction=i)
            if show_others:
                if any([i for i in player.known_characters if not i.has_faction()]):
                    textbutton 'others':
                        action Show('sc_relations')
