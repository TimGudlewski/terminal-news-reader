import headline_block_line
import headlines_win
import news_win
import curses


class HeadlineBlock:
    LINE_CONTENTS_TYPES = [
        # Change these to a different one of the kwargs below
        # if you want different contents for one of the lines.
        "title",
        "description",
    ]

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
        self.visi_pos = -1  # Visible position
        for i, contents_type in enumerate(self.LINE_CONTENTS_TYPES):
            self.lines.append(
                headline_block_line.HeadlineBlockLine(
                    (not i), self.visi_pos, getattr(self, contents_type, "")
                )
            )
        self.selected = False
        self.selection_status = False
        hblist_idx_temp = kwargs.get("hblist_idx")
        if not type(hblist_idx_temp) is int:
            hblist_idx_temp = -1
        self.hblist_idx = hblist_idx_temp

    def get_block_visi_pos(self, visi_range_start: int):
        return self.hblist_idx - visi_range_start

    def toggle_selection_status(self) -> None:
        self.selection_status = not self.selection_status

    def update_lines_init(self, visi_pos: int) -> None:
        self.visi_pos = visi_pos
        self.update_lines()

    def update_lines_incr(self, incr: int) -> None:
        # As the selector moves down past the last visible block, the blocks move up.
        # As the selector moves up past the first visible block, the blocks move down.
        self.visi_pos -= incr
        # Within the new visible range, a block whose visi_pos is still -1 after the
        # minus-equals operation above MUST be the new last visible block after a
        # down-move, since an up-move would subtract -1 (i.e. add 1) to the -1 visi_pos
        # of the new first visible block, resulting in the desired value of 0.
        self.visi_pos = (
            (self.visi_pos < 0) and (headlines_win.HeadlinesWin.get_BLOCK_CAP() - 1)
        ) or self.visi_pos
        self.update_lines()

    def update_lines(self) -> None:
        for line in self.lines:
            line.update_block_visi_pos(self.visi_pos)

    def reset_lines(self) -> None:
        self.visi_pos = -1
        self.update_lines()

    def reset_lines_horiz(self) -> None:
        for line in self.lines:
            line.reset_offset_horiz()

    def toggle_selected_status(self) -> None:
        self.selected = not self.selected
        self.reset_lines_horiz()

    def toggle_selected_status_and_print(self, win: curses.window) -> None:
        self.toggle_selected_status()
        self.print_selected_status(win)

    def print_selected_status(self, win: curses.window) -> None:
        if self.is_visible():
            win.addch(
                self.get_line(True).get_ypos_in_txt(),
                headlines_win.HeadlinesWin.get_START_X_SELECTOR(),
                self.get_select_char(),
            )

    def get_select_char(self) -> str:
        return (self.selected and "*") or " "

    def is_visible(self) -> bool:
        return self.visi_pos > -1

    def print_block(self, win: curses.window) -> None:
        self.print_line(True, win)
        self.print_line(False, win)

    def get_selector_char(self) -> str:
        return (self.selection_status and "*") or " "

    def print_selector_char(self, win: curses.window, visi_range_start: int):
        self.get_main_line().print_sel_char(win, self.get_block_visi_pos(visi_range_start), self.get_selector_char())

    def get_main_line(self) -> headline_block_line.HeadlineBlockLine:
        return self.lines[0]

    def get_secondary_line(self) -> headline_block_line.HeadlineBlockLine:
        return self.lines[1]

    def new_print_block(self, win: curses.window, visi_range_start: int) -> None:
        block_visi_pos: int = self.get_block_visi_pos(visi_range_start)
        self.lines[0].print_self(win, block_visi_pos)
        self.lines[1].print_self(win, block_visi_pos)

    def incr_line_horiz_offset(self, is_main_line: bool, incr: int) -> None:

        if is_main_line:
            self.get_main_line().incr_offset_horiz(incr)
        else:
            self.get_secondary_line().incr_offset_horiz(incr)

    def get_line(self, is_main_line: bool):
        # TODO: Raise exception if matching line not found.
        line = next((l for l in self.lines if l.is_main_line == is_main_line), None)
        return line or self.lines[0]

    def print_line(self, is_main_line: bool, win: curses.window):
        if self.is_visible():
            line = self.get_line(is_main_line)
            win.addstr(
                line.get_ypos_in_txt(),
                news_win.NewsWin.START_X_TXT,
                line.get_disp_txt(),
                curses.color_pair(line.get_color_pair()),
            )

    def new_print_line(self, win: curses.window, is_main_line: bool, visi_range_start: int):
        bvp = self.get_block_visi_pos(visi_range_start)
        if is_main_line:
            self.get_main_line().print_self(win, bvp)
        else:
            self.get_secondary_line().print_self(win, bvp)

    def get_url(self, prefix_choice: str | None = None) -> str:
        prefix_options = {
            "archive": "https://archive.is/newest/",
            "twelve": "https://12ft.io/",
        }
        prefix = (prefix_choice and prefix_options[prefix_choice]) or ""
        return prefix + self.url
