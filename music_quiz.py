#!/usr/bin/python3

"""Guess the notes
copyright 1997 - 2020 by Elliott Woodward"""

import random
import curses
from curses import wrapper

DEBUG = True
NOTE_SYMBOL = "0"
PADDING = 4
NUMBER_PER_LINE = 13
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


def padding_generator():
    """Generator iterating upon which returns the next padding character"""
    while True:
        yield '-'
        yield ' '


def print_staff(screen, notes, clef='treble'):
    """Outputs staff populated with notes.

    Arguments:
    screen -- Curses screen object to print to
    notes  -- Numerical list of notes to display
    clef   -- (optional) Which clef to display. Defaults to 'treble'
    """
    yellow_text = curses.color_pair(2)
    red_text = curses.color_pair(1)
    line_counter = 0
    get_padding = padding_generator()
    if clef == "treble":
        screen.addstr(1, 0, TREBLE_CLEF[line_counter], yellow_text)
        line_counter += 1
    for line in range(1, 10):
        pad_char = next(get_padding)
        screen.addstr(1 + line, 0, TREBLE_CLEF[line_counter], yellow_text)
        line_counter += 1
        screen.addstr(pad_char * PADDING, yellow_text)
        for current_note in range(1, NUMBER_PER_LINE + 1):
            if notes[current_note] == line:
                screen.addch(NOTE_SYMBOL, red_text)
            else:
                screen.addch(pad_char, yellow_text)
            screen.addstr(pad_char * PADDING, yellow_text)
        screen.addch("|", yellow_text)
    screen.addstr(1 + 10, 0, TREBLE_CLEF[line_counter], yellow_text)
    line_counter += 1
    screen.addstr(1 + 11, 0, TREBLE_CLEF[line_counter], yellow_text)


def generate_notes(num):
    """Generates and returns a numerical list representing notes.

    Argument:
    num -- int(), number of notes to generate
    """
    answers = ['x']
    for _ in range(0, num):
        answers.append(random.randrange(1, 10))
    return answers


def print_notes(screen, answer_letters):
    """Print note names in line with notes on staff.

    Arguments:
    screen         -- Curses screen object to print to
    answer_letters -- List of notes as single characters
    """
    screen.addstr(' ' * PADDING)
    for letter in answer_letters:
        if letter != 'x':
            screen.addch(letter)
            screen.addstr(' ' * PADDING)


def nums_to_letters(nums, clef='treble'):
    """Takes list of integers and returns list of notes as characters.

    Arguments:
    nums -- Numerical list of notes
    clef -- String indicating to which clef the numbers will be mapped
    """
    if clef == 'treble':
        notes_map = ('x', 'F', 'E', 'D', 'C', 'B', 'A', 'G', 'F', 'E')
    else: # assuming bass clef
        notes_map = ('x', 'A', 'G', 'F', 'E', 'D', 'C', 'B', 'A', 'G')
    letters = ['x']
    for num in nums:
        if num != 'x':
            letters.append(notes_map[num])
    return letters


def quiz_player(screen, letters):
    """Quiz player on displayed staff.

    Argument:
    screen  -- Curses screen object to print to
    letters -- List of correct answers as capital letter elements
    """
    green_text = curses.color_pair(3)
    correct = 0
    screen.addstr(0, 0, "Name the notes:", green_text)
    screen.addstr(" " * 10)
    correct = len(letters)
    return correct


def play_again(screen):
    """Ask if player wants to go again.

    Argument:
    screen -- Curses screen object to print to
    """
    green_text = curses.color_pair(3)
    another = ''
    while another not in (ord('y'), ord('n')):
        screen.addstr(13, 0, "Would you like to try another? (y/n): ", green_text)
        another = screen.getch()
    return another is ord('y')


def main(stdscr):
    """Start the quiz"""
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    random.seed()
    stdscr.refresh()

    again = True
    while again:
        answer_nums = generate_notes(NUMBER_PER_LINE)
        answer_letters = nums_to_letters(answer_nums)
        if DEBUG:
            debug_nums = ''.join(map(str, answer_nums)) + '\n'
            debug_letters = ''.join(answer_letters) + '\n'
            stdscr.addstr(14, 5, debug_nums)
            stdscr.addstr(15, 5, debug_letters)
        print_staff(stdscr, answer_nums)

        print_notes(stdscr, answer_letters)
        stdscr.refresh()
        quiz_player(stdscr, answer_letters)
        again = play_again(stdscr)


wrapper(main)
