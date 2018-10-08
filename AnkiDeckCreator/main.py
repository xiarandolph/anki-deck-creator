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
    print("\tmake_notes <front column> <back column> <card model>")
    print("\twrite_out <filename>")
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
    
    deck_name = input("\nEnter a deck name: ")
    #id = input("\nEnter a deck id (zero for random): ")
    deck = DeckCreator(deck_name)
    
    print_commands()
    ui = ""
    while (ui == "" or ui[0] != "quit"):
        ui = input("\nEnter a command: ").split()
        if (ui[0] == "make_notes"):
            if len(ui) != 4:
                print("Expected 4 arguments, got", len(ui))
                continue
            # Determine model
            if (ui[3] == "short_ans_model"):
                model = short_ans_model
            elif (ui[3] == "basic_model"):
                model = basic_model
            else:
                print("Unknown model", ui[3])
                continue
            
            if (ui[1] not in fp.get_titles()):
                print("Unknown column", ui[1])
                continue
            if (ui[2] not in fp.get_titles()):
                print("Unknown column", ui[2])
                continue
            
            if (len(fp.data[ui[1]]) != len(fp.data[ui[2]])):
                print("Error: could not pair columns, mismatched lengths")
                continue
            
            for i in range(len(fp.data[ui[1]])):
                deck.create_note((fp.data[ui[1]][i], fp.data[ui[2]][i]), model)
            
            print("Created {:d} notes in deck .".format(len(fp.data[ui[1]]))
                                                        , deck_name)

        elif (ui[0] == "write_out"):
            if (len(ui) != 2):
                print("Expected 2 arguments, received", len(ui))
                continue
            deck.write_to_file(ui[1])
            print("Write out complete")

        elif (ui[0] == "help"):
            print_commands()
        elif (ui[0] == "quit"):
            continue
        else:
            print("Error: unknown command", ui[0])
            continue
            