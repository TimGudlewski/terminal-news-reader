import curses


def main(stdscr: curses.window):
    a = stdscr.getch()
    # h = 104
    # s = 115
    # f = 102
    return a


b = curses.wrapper(main)
print(b)
print(curses.KEY_LEFT) # 260
print(curses.KEY_RIGHT)
