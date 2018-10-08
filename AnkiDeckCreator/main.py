"""
Main program file

Example:
    $ python3 main.py input.xlsx

TODO:
    * Make usage more intuitive
"""

import sys
from parser import Parser
from deckcreator import DeckCreator, basic_model, short_ans_model

def print_usage():
    # Print command line arguments
    print("Usage: main.py <filename>")

def print_commands():
    print("\nAvailable commands:")
    print("\tcreate_deck <deck name> [deck id]")
    # print("\tprint_decks")
    # print("\tprint_models")
    # print("\tprint_data")
    print("\tmake_notes <deck name> <front column> <back column> <card model>")
    print("\twrite_out <deck name> <filename>")
    print("\thelp")
    print("\tquit")
    print("\nAvailable models:")
    print("\tshort_ans_model")
    print("\tbasic_model")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit(1)
    
    try:
        fp = Parser(sys.argv[1])
    except FileNotFoundError:
        print("Error: Could not open file", sys.argv[1])
        exit(1)
    
    print("Data found:")
    for title in fp.get_titles():
        print("{:10s}:".format(title), len(fp.data[title]), "items")
        
    decks = {}
    
    models = {
        'short_ans_model': short_ans_model,
        'basic_model': basic_model
    }
    
    print_commands()
    ui = ""
    while ui == "" or ui[0] != "quit":
        ui = input("\nEnter a command: ").split()
        if ui[0] == "create_deck":
            if len(ui) == 3:
                decks[ui[1]] = DeckCreator(ui[1], ui[2])
            elif len(ui) == 2:
                decks[ui[1]] = DeckCreator(ui[1])
            else:
                print("Expected 2 or 3 arguments, got", len(ui))
                continue
                
        elif ui[0] == "make_notes":
            if len(ui) != 5:
                print("Expected 4 arguments, got", len(ui))
                continue
                
            # Determine model
            if ui[4] not in models.keys():
                print("Unknown model", ui[4],".")
                continue
            
            # Check if deck exists
            if ui[1] not in decks.keys():
                print("Unknown deck", ui[1])
                continue
    
            # Check if columns exist
            if ui[2] not in fp.get_titles():
                print("Unknown column", ui[2])
                continue
            if ui[3] not in fp.get_titles():
                print("Unknown column", ui[3])
                continue
            
            front = fp.data[ui[2]]
            back = fp.data[ui[3]]
            
            if len(front) != len(back):
                print("Error: could not pair columns, mismatched lengths")
                continue
            
            for i in range(len(front)):
                decks[ui[1]].create_note((front[i], back[i]), models[ui[4]])
            
            print("Created {:d} notes in deck {:s}.".format(len(front), ui[1]))

        elif (ui[0] == "write_out"):
            if (len(ui) != 3):
                print("Expected 3 arguments, received", len(ui))
                continue
            decks[ui[1]].write_to_file(ui[2])
            print("Write out complete")

        elif (ui[0] == "help"):
            print_commands()
        elif (ui[0] == "quit"):
            print("Program ending.")
            continue
        else:
            print("Error: unknown command", ui[0])
            continue
            