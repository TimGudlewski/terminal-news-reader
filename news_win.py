import curses


class NewsWin:
    HEIGHT = 29
    WIDTH = 60
    TOP_MARGIN = 3
    LEFT_MARGIN = 3
    RIGHT_MARGIN = 3
    BOTTOM_MARGIN = 0
    START_X = 0
    START_Y = 0
    START_X_TXT = LEFT_MARGIN + 1
    START_Y_TXT = TOP_MARGIN + 1
    END_X_TXT = WIDTH - (RIGHT_MARGIN + 1)
    END_Y_TXT = HEIGHT - (BOTTOM_MARGIN + 1)
    WIDTH_TXT = END_X_TXT - START_X_TXT
    HEIGHT_TXT = END_Y_TXT - START_Y_TXT  # Height of each Text Region
    START_X_WIN_NAME = 2

    def __init__(self, startx):
        self.win = curses.newwin(
            self.HEIGHT,
            self.WIDTH,
            self.START_Y,
            startx,
        )
        self.win.keypad(True)

    def print_box(self):
        self.win.box("|", "-")

    def print_win_name(self, name):
        self.win.addstr(
            self.START_X_WIN_NAME,
            self.START_X_TXT,
            name,
            curses.A_BOLD | curses.A_ITALIC | curses.color_pair(3),
        )

    def refresh_win(self):
        self.win.refresh()
