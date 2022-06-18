import headlines_win
import headline_block
import curses
import helper


class HeadlineBlockList:
    def __init__(self, data: list[dict]):
        self.headlines = [
            headline_block.HeadlineBlock(hblist_idx=i, **article)
            for i, article in enumerate(data)
        ]
        self.selection_idx: int = 0
        self.headlines[self.selection_idx].toggle_selection_status()
        # Set initial block positions. RTB is the block capacity of the headlines window.
        # visible_blocks_range = min(
        #     headlines_win.HeadlinesWin.get_BLOCK_CAP(), self.get_len()
        # )
        # for i in range(visible_blocks_range):
        #     self.headlines[i].update_lines_init(i)

    def get_visi_range_start(self, sel_idx: int = -1) -> int:
        mid = int(headlines_win.HeadlinesWin.get_BLOCK_CAP() / 2)
        if sel_idx < 0:
            sel_idx = self.selection_idx
        if sel_idx >= mid and sel_idx <= self.get_len() - mid:
            return sel_idx - mid
        elif sel_idx < mid:
            return 0
        else:
            return self.get_len() - headlines_win.HeadlinesWin.get_BLOCK_CAP()

    def get_visi_range(self, visi_range_start: int):
        return range(
            visi_range_start,
            visi_range_start + headlines_win.HeadlinesWin.get_BLOCK_CAP(),
        )

    def print_block_at_idx(self, win: curses.window, idx: int):
        self.headlines[idx].new_print_block(win, self.get_visi_range_start())

    def get_selection_idx(self) -> int:
        return self.selection_idx

    def incr_selection_idx(self, incr: int) -> None:
        old_selection_idx: int = self.get_selection_idx()
        self.selection_idx += incr
        self.move_selection(old_selection_idx)

    def move_selection(self, old_idx: int):
        self.toggle_block_selection_status(old_idx)
        self.toggle_block_selection_status(self.get_selection_idx())

    def toggle_block_selection_status(self, idx: int):
        self.get_block_at_idx(idx).toggle_selection_status()

    def new_print_blocks(self, win: curses.window):
        for i in self.get_visi_range(self.get_visi_range_start()):
            self.print_block_at_idx(win, i)

    def get_block_at_idx(self, idx: int) -> headline_block.HeadlineBlock:
        # TODO: Try-catch idx out of range
        return self.headlines[idx]

    def print_block_selector_char(self, win: curses.window, idx: int = -1):
        if idx < 0:
            idx = self.get_selection_idx()
        write_str = (
            "sel_idx: "
            + str(idx)
            + "\nvisi_range_start: "
            + str(self.get_visi_range_start())
        )
        h = helper.Helper()
        h.save_debug_txt(write_str, 7)
        block = self.get_block_at_idx(idx)
        block.print_selector_char(win, self.get_visi_range_start())

    def get_visible_block_idxs(self):
        """Returns a list of the indices of all visible HeadlineBlocks"""
        return [bi for bi in range(self.get_len()) if self.headlines[bi].is_visible()]

    def scroll_blocks(self, incr):
        visible_blocks_idxs = self.get_visible_block_idxs()
        new_range_start = visible_blocks_idxs[0] + incr
        new_range_end = new_range_start + headlines_win.HeadlinesWin.get_BLOCK_CAP()
        # Reset the zeroth index if incr is 1
        # Reset the last index if incr is -1
        reset_idx = (incr - 1) and -1
        self.headlines[visible_blocks_idxs[reset_idx]].reset_lines()
        for i in range(new_range_start, new_range_end):  # Up to but not including
            self.headlines[i].update_lines_incr(incr)

    def print_blocks(self, win: curses.window):
        for i in self.get_visible_block_idxs():
            self.headlines[i].print_block(win)

    def get_selected_idx(self) -> int:
        # TODO: Raise exception if no selected headline index was found.
        return next(
            (i for i in range(len(self.headlines)) if self.headlines[i].selected), -1
        )

    def get_selected_blk(self) -> headline_block.HeadlineBlock:
        # TODO: Raise exception if no selected headline was found.
        return next(
            (block for block in self.headlines if block.selected), self.headlines[0]
        )

    def get_selection_blk(self) -> headline_block.HeadlineBlock:
        return self.get_block_at_idx(self.get_selection_idx())

    def toggle_block_selected_status_and_print(self, idx, win: curses.window):
        self.headlines[idx].toggle_selected_status_and_print(win)

    def toggle_selected_block(self, idx):
        self.headlines[idx].toggle_selected_status()

    def move_selected_horiz_and_print(
        self, incr, is_main_line: bool, win: curses.window
    ):
        selected_block: headline_block.HeadlineBlock = self.get_selection_blk()
        selected_block.incr_line_horiz_offset(
            is_main_line, incr 
        )
        selected_block.new_print_line(win, is_main_line, self.get_visi_range_start(self.get_selection_idx()))

    def get_len(self):
        return len(self.headlines)

    def move_selection_vert_and_print(self, new_idx, win: curses.window):
        old_idx = self.get_selected_idx()
        self.toggle_block_selected_status_and_print(old_idx, win)
        self.headlines[old_idx].print_block(win)
        self.headlines[new_idx].toggle_selected_status_and_print(win)
