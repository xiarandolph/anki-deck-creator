"""
Module defines DeckCreator class and some basic models
"""

import genanki
from random import randrange   # generating UUID
from parser import Parser

# CONSTS
card_css = '''.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}'''

basic_model = genanki.Model(
    1936820195,
    'Basic Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="back">{{Back}}'
        },
    ],
    css=card_css,
)

short_ans_model = genanki.Model(
    1835728501,     # MODEL ID
    'Short Answer Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}\n{{type:Back}}',
            'afmt': '{{FrontSide}}<hr id="back">{{Back}}'
        },
    ],
    css=card_css,
)

class DeckCreator:
    def __init__(self):
        self.decks = {}
        self.models = {
            'short_ans_model': short_ans_model,
            'basic_model': basic_model
        }

    def parse_excel(self, params):
        """params[0]    excel filename to open"""
        
        if len(params) != 1:
            print("Error: expected 1 argument, received", len(params))
            return False
        
        try:
            self.fp = Parser(params[0])
        except FileNotFoundError:
            print("Error: Could not open file", params[0])
            return False

        return True

    def create_deck(self, params):
        """
        params[0]   string key to access deck
        params[1]   deck name to create
        params[2]   optional deck id
        """

        if len(params) < 2 or len(params) > 3:
            print("Error: expected 2 or 3 arguments, received", len(params))
            return False
        
        if len(params) == 3:
            deck_id = params[2]
        else:
            deck_id = randrange(1 << 30, 1 << 31)
        
        self.decks[params[0]] = genanki.Deck(deck_id, params[1])

        return True

    def create_notes(self, params):
        """
        params[0]   string key of genanki.Deck to add notes to
        params[1]   string key of genanki.Model to base notes on
        params[2:]  list of string title for each field in the model
                    title corresponds to a column of data parsed by parse_excel
        return      list of notes created
        """

        if len(params) < 3:
            print("Error: expected atleast 3 arguments, received", len(params))
            return False

        if params[0] not in self.decks.keys():
            print("Error: deck {} not found".format(params[0]))
            return False

        if params[1] not in self.models.keys():
            print("Error: model {} not found".format(params[1]))
            return False

        deck = self.decks[params[0]]
        model = self.models[params[1]]
        data = []

        if len(model.fields) != len(params)-2:
            print("Error: {} fields found, expected {}".format(len(data),
                                                               len(model.fields)))
            return False

        for title in params[2:]:
            if title not in self.fp.get_titles():
                print("Error: unknown column", title)
                print("Known columns are:", self.fp.get_titles())
                return False
            if len(data) > 0 and len(self.fp.data[title]) != len(data[0]):
                print("Error: length of column {} does not match".format(title))
            data.append(self.fp.data[title])

        for i in range(len(data[1])):
            fields = list(data[j][i] for j in range(len(data)))
            deck.add_note(genanki.Note(model=model, fields=fields))

        return True

    def write_out(self, params):
        """
        params[0]   string filename to write to
        params[1:]   string key of genanki.Deck to write out
        """

        if len(params) < 2:
            print("Error: expected at least 2 arguments, received", len(params))
            return False

        if params[1] not in self.decks.keys():
            print("Error: deck {} not found".format(params[0]))
            return False

        deck = self.decks[params[1]]
        filename = params[0]

        extension = filename.split('.')
        if (len(extension) != 2 or extension[1] != 'apkg'):
            print("Error: invalid filename, expected .apkg")
        genanki.Package(deck).write_to_file(filename)

        return True

    def print_commands(self, params):
        if len(params) > 0:
            print("Error: expected 0 arguments, received", len(params))
            return False

        print("\nAvailable commands:")
        print("\tparse_excel <filename>")
        print("\tcreate_deck <deck name> [deck id]")
        print("\tcreate_model <uninplemented>")
        print("\tcreate_notes <card model> <field...>")
        print("\twrite_out <deck name> <filename>")
        print("\thelp")
        print("\tquit")
        return True

    def call_command(self, cmd, params):
        """Calls given command with a tuple of the required parameters

        Intended for usage in main.py

        Returns whether the command was successfully called
        """

        commands = {
            'parse_excel': self.parse_excel,
            'create_deck': self.create_deck,
            'create_notes': self.create_notes,
            'write_out': self.write_out,
            'help': self.print_commands,
            #'quit': self.quit,
        }

        if cmd not in commands.keys():
            print("Error: command \'{}\' not found".format(cmd))
            return False

        return commands[cmd](params)
