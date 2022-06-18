import news_win
import curses
import headlines_win
import typing


class HeadlineBlockLine:
    YPOS_IN_BLK_OPTS: typing.Tuple[int, int] = (0, 2)
    COLOR_PAIR_OPTS: typing.Tuple[int, int] = (2, 0)

    def __init__(
        self,
        is_main_line: bool,
        block_visi_pos: int,
        full_txt: str,
    ) -> None:
        self.is_main_line = is_main_line
        self.block_visi_pos = block_visi_pos
        self.full_txt = full_txt
        self.offset_horiz = 0  # Horizontal display offset factor

    def get_ypos_in_blk(self) -> int:
        return (
            not self.is_main_line and self.YPOS_IN_BLK_OPTS[1]
        ) or self.YPOS_IN_BLK_OPTS[0]

    def print_sel_char(self, win: curses.window, block_visi_pos: int, sel_char: str):
        win.addch(
            self.new_get_ypos_in_txt(block_visi_pos),
            headlines_win.HeadlinesWin.get_START_X_SELECTOR(),
            sel_char,
        )

    def print_self(self, win: curses.window, block_visi_pos: int):
        win.addstr(
            self.new_get_ypos_in_txt(block_visi_pos),
            news_win.NewsWin.START_X_TXT,
            self.get_disp_txt(),
            curses.color_pair(self.get_color_pair()),
        )

    def new_get_ypos_in_txt(self, block_visi_pos: int):
        if block_visi_pos > -1:
            return (
                news_win.NewsWin.START_Y_TXT
                + (block_visi_pos * headlines_win.HeadlinesWin.HEIGHT_BLK)
                + self.get_ypos_in_blk()
            )
        else:
            return -1

    def get_ypos_in_txt(self):
        if self.block_visi_pos > -1:
            return (
                news_win.NewsWin.START_Y_TXT
                + (self.block_visi_pos * headlines_win.HeadlinesWin.HEIGHT_BLK)
                + self.get_ypos_in_blk()
            )
        else:
            return -1

    def get_color_pair(self) -> int:
        return (self.is_main_line and self.COLOR_PAIR_OPTS[0]) or self.COLOR_PAIR_OPTS[
            1
        ]

    def update_block_visi_pos(self, new_pos: int):
        self.block_visi_pos = new_pos

    def incr_offset_horiz(self, incr):
        self.offset_horiz = max(self.offset_horiz + incr, 0)
        self.offset_horiz = min(
            len(self.full_txt) - news_win.NewsWin.WIDTH_TXT, self.offset_horiz
        )

    def reset_offset_horiz(self):
        self.offset_horiz = 0

    def get_disp_txt(self) -> str:
        # TODO: Create custom exception for if the length of the string
        # returned by this method is less than NewsWin.WIDTH_TXT
        return (
            self.full_txt
            and self.full_txt[
                self.offset_horiz : self.offset_horiz + news_win.NewsWin.WIDTH_TXT
            ]
        ) or " " * news_win.NewsWin.WIDTH_TXT
