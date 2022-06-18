import headline_block_line
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
        for i, contents_type in enumerate(self.LINE_CONTENTS_TYPES):
            self.lines.append(
                headline_block_line.HeadlineBlockLine(
                    (not i), getattr(self, contents_type, "")
                )
            )
        self.selection_status = False
        hblist_idx_temp = kwargs.get("hblist_idx")
        if not type(hblist_idx_temp) is int:
            hblist_idx_temp = -1
        self.hblist_idx = hblist_idx_temp

    def get_block_visi_pos(self, visi_range_start: int):
        return self.hblist_idx - visi_range_start

    def toggle_selection_status(self) -> None:
        self.selection_status = not self.selection_status

    def get_selector_char(self) -> str:
        return (self.selection_status and "*") or " "

    def reset_horiz_offsets(self) -> None:
        self.get_main_line().reset_offset_horiz()
        self.get_secondary_line().reset_offset_horiz()

    def print_selector_char(self, win: curses.window, visi_range_start: int):
        self.get_main_line().print_sel_char(
            win, self.get_block_visi_pos(visi_range_start), self.get_selector_char()
        )

    def get_main_line(self) -> headline_block_line.HeadlineBlockLine:
        return self.lines[0]

    def get_secondary_line(self) -> headline_block_line.HeadlineBlockLine:
        return self.lines[1]

    def new_print_block(self, win: curses.window, visi_range_start: int) -> None:
        block_visi_pos: int = self.get_block_visi_pos(visi_range_start)
        self.get_main_line().print_self(win, block_visi_pos)
        self.get_secondary_line().print_self(win, block_visi_pos)

    def incr_line_horiz_offset(self, is_main_line: bool, incr: int) -> None:
        if is_main_line:
            self.get_main_line().incr_offset_horiz(incr)
        else:
            self.get_secondary_line().incr_offset_horiz(incr)

    def new_print_line(
        self, win: curses.window, is_main_line: bool, visi_range_start: int
    ):
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
