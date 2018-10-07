"""
Main program file
"""

import sys
from parser import Parser

def print_usage():
    # Print command line arguments
    print("Usage: main.py <filename>")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit(1)
    
    try:
        fp = Parser(sys.argv[1])
    except FileNotFoundError:
        print("Error: Could not open file", sys.argv[1])
        exit(1)
        