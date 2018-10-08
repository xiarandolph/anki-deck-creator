"""
Module defines DeckCreator class and some basic models
"""

import genanki
import random   # generating UUID

## CONSTS
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

def custom_model(self, id, name, fields, templates, css):
    """
    @param  id          model id
    @param  name        model name
    @param  fields      list of dictionaries {'name': 'field name'}
    @param  templates   list of card templates
    @param  css         custom css string .card {}
    """
    
    return genanki.Model(
        id,
        name,
        fields=fields,
        templates=templates,
        css=css
    )

class DeckCreator:
    def __init__(self, deck_name, deck_id = random.randrange(1 << 30, 1 << 31)):
        self.deck = genanki.Deck(deck_id, deck_name)
    
    def create_note(self, data, model):
        """
        @param  data    two-tuple containing front and back fields (front, back)
        @param  model   basic_model or short_ans_model
        """

        note = genanki.Note(
            model=model,
            fields=[str(data[0]), str(data[1])]
        )
        self.deck.add_note(note)
    
    def write_to_file(self, filename):
        extension = filename.split('.')
        if (len(extension) != 2 or extension[1] != 'apkg'):
            print("Error: invalid filename, expected .apkg")
        genanki.Package(self.deck).write_to_file(filename)
