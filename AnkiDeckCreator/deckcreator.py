"""
Module defines DeckCreator class

TODO:
    * create_notes(): Create card pairings for data
    * card pairing options: pair every column to eachother
"""

import genanki
import random   # generating UUID

card_css = '''.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}'''

class DeckCreator:
    fill_in_model = genanki.Model(
        1835728501,     # MODEL ID
        'Short Answer Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}\n{{type:Answer}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'
            },
        ],
        css=card_css,
    )
    
    def __init__(self, deck_name, deck_id = random.randrange(1 << 30, 1 << 31)):
        self.deck = genanki.Deck(deck_id, deck_name)
    
    def create_notes(self, data):
        notes = []
        test_note = genanki.Note(
            model=fill_in_model,
            fields=['Question', 'Answer']
        )
        notes.append(test_note)
        return notes
    
    def populate_deck(self, data):
        for note in create_notes(data):
            self.deck.add_note(note)
    
    def write_to_file(self, filename):
        genanki.Package(self.deck).write_to_file(filename)
