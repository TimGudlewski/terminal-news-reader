import headlines_win
import headline_block
import curses


class HeadlineBlockList:
    def __init__(self, data: list[dict]):
        self.headlines = [
            headline_block.HeadlineBlock(hblist_idx=i, **article)
            for i, article in enumerate(data)
        ]
        self.selection_idx: int = 0
        self.get_selection_blk().toggle_selection_status()

    def get_visi_range_start(self, sel_idx: int = -1) -> int:
        mid = int(headlines_win.HeadlinesWin.get_BLOCK_CAP() / 2)
        if sel_idx < 0:
            sel_idx = self.get_selection_idx()
        if sel_idx >= mid and sel_idx <= self.get_len() - mid:
            return sel_idx - mid
        elif sel_idx < mid:
            return 0
        else:
            return self.get_len() - headlines_win.HeadlinesWin.get_BLOCK_CAP()

    def get_visi_range(self, visi_range_start: int = -1):
        if visi_range_start < 0:
            visi_range_start = self.get_visi_range_start()
        return range(
            visi_range_start,
            visi_range_start + headlines_win.HeadlinesWin.get_BLOCK_CAP(),
        )

    def print_block_at_idx(self, win: curses.window, idx: int):
        self.get_block_at_idx(idx).new_print_block(win, self.get_visi_range_start())

    def get_selection_idx(self) -> int:
        return self.selection_idx

    def incr_selection_idx(self, incr: int) -> None:
        old_idx: int = self.get_selection_idx()
        self.selection_idx += incr
        self.toggle_block_selection_status(old_idx)
        self.toggle_block_selection_status(self.get_selection_idx())

    def toggle_block_selection_status(self, idx: int):
        self.get_block_at_idx(idx).toggle_selection_status()

    def reset_horizontal_offsets_at_idx(self, idx: int) -> None:
        self.get_block_at_idx(idx).reset_horiz_offsets()

    def new_print_blocks(self, win: curses.window):
        for i in self.get_visi_range():
            self.print_block_at_idx(win, i)

    def get_block_at_idx(self, idx: int) -> headline_block.HeadlineBlock:
        # TODO: Try-catch idx out of range
        return self.headlines[idx]

    def print_block_selector_char(self, win: curses.window, idx: int = -1):
        if idx < 0:
            idx = self.get_selection_idx()
        block = self.get_block_at_idx(idx)
        block.print_selector_char(win, self.get_visi_range_start())

    def get_selection_blk(self) -> headline_block.HeadlineBlock:
        return self.get_block_at_idx(self.get_selection_idx())

    def move_selected_horiz_and_print(
        self, incr, is_main_line: bool, win: curses.window
    ):
        selected_block: headline_block.HeadlineBlock = self.get_selection_blk()
        selected_block.incr_line_horiz_offset(is_main_line, incr)
        selected_block.new_print_line(
            win, is_main_line, self.get_visi_range_start()
        )

    def get_len(self):
        return len(self.headlines)
