import curses


class NewsWin:
    HEIGHT = 30
    WIDTH = 60
    MARGIN = 3
    START_Y = 0
    START_X_TXT = START_Y_TXT = MARGIN + 1
    END_Y_TXT = HEIGHT - (MARGIN - 1)
    WIDTH_TXT = WIDTH - (START_X_TXT * 2)
    HEIGHT_TXT = END_Y_TXT - START_Y_TXT  # Height of each Text Region

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
            self.MARGIN - 1,
            self.START_X_TXT,
            name,
            curses.A_BOLD | curses.A_ITALIC | curses.color_pair(3),
        )

    def refresh_win(self):
        self.win.refresh()
