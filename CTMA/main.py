"""
main.py is the entry point of CTMA
From here either the gui or the cli version of the program may be launched

Functions:
    main(): Lauches the program
"""

import gui
import cli
import argparse


def main():
    """
    Starts the main program.
    Defaults to GUI. Use --cli argument to start in command line mode.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Launch the application in Command Line Interface mode",
    )

    args = parser.parse_args()

    if args.cli:
        cli.startProgram()
    else:
        gui.start_gui()


if __name__ == "__main__":
    main()
