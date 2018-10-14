"""
Main program file which parses a file with commands to run

Example:
    $ python3 main.py cmds.txt

TODO:
    * Make usage more intuitive and code more readable
"""

import sys
from deckcreator import DeckCreator

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: main.py <filename>")
        print("\tfilename:\tfile containing list of commands to call")
        exit(1)
    
    cmds = []
    with open(sys.argv[1]) as f:
        for line in f:
            cmds.append(line.strip('\n'))
    
    dc = DeckCreator()
    for cmd_line in cmds:
        cmd = cmd_line.split()[0]
        params = ()
        if len(cmd_line) > 1:
            params = cmd_line.split()[1:]
        dc.call_command(cmd, params)
