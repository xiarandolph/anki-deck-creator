import genanki
import random   # generating UUID

card_css = '''.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}'''

fill_in_model = genanki.Model(
    random.randrange(1 << 30, 1 << 31),     # UUID
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

test_note = genanki.Note(
    model=fill_in_model,
    fields=['Question', 'Answer']
)

test_deck = genanki.Deck(
    2095839102,     # DECK ID
    'Test Deck'
)

test_deck.add_note(test_note)

genanki.Package(test_deck).write_to_file('test.apkg')
