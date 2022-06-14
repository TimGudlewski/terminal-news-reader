import headlines_win
import headline_block
import curses


class HeadlineBlockList:
    def __init__(self, data: list[dict]):
        self.headlines = [headline_block.HeadlineBlock(**article) for article in data]
        # Set initial block positions. RTB is the block capacity of the headlines window.
        visible_blocks_range = min(
            headlines_win.HeadlinesWin.get_BLOCK_CAP(), self.get_len()
        )
        for i in range(visible_blocks_range):
            self.headlines[i].update_lines_init(i)

    def get_visible_block_idxs(self):
        """Returns a list of the indices of all visible HeadlineBlocks"""
        return [
            bi for bi in range(self.get_len()) if self.headlines[bi].is_visible()
        ]

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

    def print_block_at_idx(self, idx: int, win: curses.window) -> None:
        self.headlines[idx].print_block(win)

    def print_blocks(self, win: curses.window):
        for i in self.get_visible_block_idxs():
            self.print_block_at_idx(i, win)

    def get_selected_idx(self) -> int:
        return next(
            (i for i in range(len(self.headlines)) if self.headlines[i].selected), -1
        )

    def get_selected(self) -> headline_block.HeadlineBlock:
        # TODO: Raise exception if no selected headline was found.
        return next(
            (block for block in self.headlines if block.selected), self.headlines[0]
        )

    def toggle_block_selected_status_and_print(self, idx, win: curses.window):
        self.headlines[idx].toggle_selected_status_and_print(win)

    def toggle_selected_block(self, idx):
        self.headlines[idx].toggle_selected_status()

    def move_selected_horiz(self, incr, is_main_line: bool, win: curses.window):
        selected_block: headline_block.HeadlineBlock = self.get_selected()
        selected_block.incr_line_horiz_offset(is_main_line, incr)
        selected_block.print_line(is_main_line, win)

    def get_len(self):
        return len(self.headlines)

    def shift_selection_and_update(self, new_idx, win: curses.window):
        old_idx = self.get_selected_idx()
        self.toggle_block_selected_status_and_print(old_idx, win)
        self.headlines[old_idx].print_block(win)
        self.headlines[new_idx].toggle_selected_status_and_print(win)
