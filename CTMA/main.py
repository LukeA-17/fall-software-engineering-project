"""
main.py is the entry point of CTMA
From here either the gui or the cli version of the program may be launched

Functions:
    main(): Lauches the program
"""

import gui
import cli


def main():
    "Starts the main program. Swap commenting to toggle versions"
    #gui.start_gui()
    cli.startProgram()


if __name__ == "__main__":
    main()
