#!/usr/bin/env python3
import curses

def main(stdscr):
    curses.use_default_colors()

    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    for i in range(0, 255):
        stdscr.addstr(str(i), curses.color_pair(i))
    stdscr.getch()

curses.wrapper(main)
