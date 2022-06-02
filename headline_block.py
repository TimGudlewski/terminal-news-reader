import headline_block_line
import headlines_win
import news_win
import curses


class HeadlineBlock:
    LT = [
        "title",
        "description",
    ]  # Line types. Length should equal lengths of LYB and LCPAIRS.
    LYB = [0, 2]  # Line Ys within block
    LCPAIRS = [2, 0]  # Line color pairs

    def __init__(self, **kwargs):
        s = kwargs.get("source")
        self.source = s and s["name"]
        self.title = kwargs.get("title")
        self.date = kwargs.get("publishedAt")
        self.author = kwargs.get("author")
        self.url = kwargs.get("url") or ""
        self.description = kwargs.get("description")
        self.content = kwargs.get("content")
        self.lines: list[headline_block_line.HeadlineBlockLine] = []
        for i, line_type in enumerate(self.LT):
            block_line = headline_block_line.HeadlineBlockLine(
                line_type=line_type,
                ypos_in_blk=self.LYB[i],
                ypos_in_txt=-1,
                full_txt=getattr(self, line_type),
                color_pair=self.LCPAIRS[i],
            )
            self.lines.append(block_line)
        self.block_pos = -1
        self.selected = False

    def update_lines(self, incr):
        # As the selector moves down past the blocks, the blocks move up, and vice versa.
        self.block_pos -= incr
        self.block_pos = ((self.block_pos < 0) and 5) or self.block_pos
        for line in self.lines:
            line.update_ypos_in_txt(self.block_pos)

    def reset_lines(self):
        self.block_pos = -1
        for line in self.lines:
            line.reset_ypos_in_txt()

    def reset_lines_horiz(self):
        for line in self.lines:
            line.reset_offset_horiz()

    def toggle_selected_status(self):
        self.selected = not self.selected
        self.reset_lines_horiz()

    def toggle_selected_status_and_update(self, win: curses.window):
        self.toggle_selected_status()
        self.print_selected_status(win)

    def print_selected_status(self, win: curses.window):
        if self.block_pos > -1:
            win.addch(
                self.get_main_line().get_ypos_in_txt(),
                headlines_win.HeadlinesWin.get_selector_x(),
                self.get_select_char(),
            )

    def get_select_char(self):
        return (self.selected and "*") or " "

    def print_block(self, win: curses.window):
        if self.block_pos > -1:
            for line in self.lines:
                win.addstr(
                    line.get_ypos_in_txt(),
                    news_win.NewsWin.START_X_TXT,
                    line.get_disp_txt(),
                    curses.color_pair(line.color_pair),
                )

    def scroll_line_horiz(self, line_idx, incr):
        self.lines[line_idx].incr_offset_horiz(incr)

    def print_line(self, line_idx, win: curses.window):
        win.addstr(
            self.lines[line_idx].get_ypos_in_txt(),
            news_win.NewsWin.START_X_TXT,
            self.lines[line_idx].get_disp_txt(),
            curses.color_pair(self.lines[line_idx].color_pair),
        )

    def get_main_line(self):
        return self.lines[0]

    def get_url(self) -> str:
        return self.url
