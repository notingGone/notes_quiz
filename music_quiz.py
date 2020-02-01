#!/usr/bin/python3

import random
import sys
# import string
import curses
from curses import wrapper

CLEF = "treble"
NOTE_SYMBOL = "O"
PADDING = 4
NUMBER_PER_LINE = 13
# wrong = 0
NOTE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
GET_ANSWER = ANSWER = [
    'X', 'X ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']

TREBLE_CLEF = [
    "       __",
    "|-----/--\\",
    "|     |  |",
    "|-----|-/-",
    "|     /   ",
    "|---/-|---",
    "| / /-|--,",
    "|-|---+--|",
    "|  \\--|--\'",
    "|-----|---",
    "     /    ",
    "    @     "]


def print_staff(stdscr):
    clef_counter = 0
    if CLEF == "treble":
        stdscr.addstr(5, 0, TREBLE_CLEF[clef_counter])
        clef_counter = clef_counter + 1
    for line in range(1, 10):
        if line % 2 == 1:
            line_spacing = "-"
        else:
            line_spacing = " "
        stdscr.addstr(5 + line, 0, TREBLE_CLEF[clef_counter])
        clef_counter = clef_counter + 1
        stdscr.addstr(line_spacing * PADDING)
        for current_note in range(0, NUMBER_PER_LINE):
            if NOTE[current_note] == line:
                # window.addch(ch)
                stdscr.addch(NOTE_SYMBOL, curses.color_pair(1))
            else:
                stdscr.addch(line_spacing)
            stdscr.addstr(line_spacing * PADDING)
        stdscr.addch("|")
    stdscr.addstr(5 + 10, 0, TREBLE_CLEF[clef_counter])
    clef_counter = clef_counter + 1
    stdscr.addstr(5 + 11, 0, TREBLE_CLEF[clef_counter])


def generate_notes():
    for i in range(0, NUMBER_PER_LINE):
        NOTE[i] = random.randrange(1, 10)
        if NOTE[i] == 1 or NOTE[i] == 8:
            [i] = "F"
        elif NOTE[i] == 2 or NOTE[i] == 9:
            ANSWER[i] = "E"
        elif NOTE[i] == 3:
            ANSWER[i] = "D"
        elif NOTE[i] == 4:
            ANSWER[i] = "C"
        elif NOTE[i] == 5:
            ANSWER[i] = "B"
        elif NOTE[i] == 6:
            ANSWER[i] = "A"
        elif NOTE[i] == 7:
            ANSWER[i] = "G"


def print_notes(stdscr):
    line_spacing = " "
    stdscr.addstr(line_spacing * PADDING)

    for current_note in range(0, NUMBER_PER_LINE):
        stdscr.addch(ANSWER[current_note])
        stdscr.addstr(line_spacing * PADDING)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    random.seed()
    stdscr.refresh()
    while 1:
        wrong = 0
        another = 0
        generate_notes()
        print_staff(stdscr)
        stdscr.addstr(17, 0, "Name the notes: \n")
        stdscr.addstr(" " * 10)
        print_notes(stdscr)
        stdscr.refresh()
        # make this range(0,len(ANSWER)) or range(0,len(GET_ANSWER)
        # depending on which is shorter
        for i in range(0, len(GET_ANSWER)):
            # make sure I'm testing the right things here
            if ANSWER[i] != GET_ANSWER[i]:
                wrong = wrong + 1
        # stdscr.addstr(25, 0, "You got " + str(wrong
        # + NUMBER_PER_LINE - len(GET_ANSWER))
        # + " notes wrong out of " + str(NUMBER_PER_LINE))
        while another != ord('y') and another != ord('n'):
            stdscr.addstr(20, 0, "Would you like to try another? (y/n): ")
            another = stdscr.getch()
        if another == ord('n'):
            sys.exit(0)


wrapper(main)
