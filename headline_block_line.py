import news_win
import headlines_win


class HeadlineBlockLine:
    def __init__(
        self,
        line_type: str,
        ypos_in_blk: int,
        ypos_in_txt: int,
        full_txt: str,
        color_pair: int,
    ) -> None:
        self.line_type = line_type
        self.ypos_in_blk = ypos_in_blk
        self.ypos_in_txt = ypos_in_txt
        self.full_txt = full_txt
        # ID number of the Curses color pair for this line
        self.color_pair = color_pair or 0
        self.offset_horiz = 0

    def get_ypos_in_txt(self):
        return self.ypos_in_txt

    def update_ypos_in_txt(self, blk_pos):
        self.ypos_in_txt = (
            news_win.NewsWin.START_Y_TXT
            + (blk_pos * headlines_win.HeadlinesWin.HEIGHT_BLK)
            + self.ypos_in_blk
        )

    def reset_ypos_in_txt(self):
        self.ypos_in_txt = -1

    def incr_offset_horiz(self, incr):
        self.offset_horiz = max(self.offset_horiz + incr, 0)
        self.offset_horiz = min(len(self.full_txt) - news_win.NewsWin.WIDTH_TXT, self.offset_horiz)

    def reset_offset_horiz(self):
        self.offset_horiz = 0

    def get_disp_txt(self) -> str:
        # TODO: Create custom exception for if the length of the string 
        # returned by this method is less than NewsWin.WIDTH_TXT
        return (
            self.full_txt
            and self.full_txt[self.offset_horiz : self.offset_horiz + news_win.NewsWin.WIDTH_TXT]
        ) or " " * news_win.NewsWin.WIDTH_TXT
