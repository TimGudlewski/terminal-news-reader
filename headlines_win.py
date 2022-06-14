import news_win
import headline_block
import headline_block_list
import commands
import webbrowser


class HeadlinesWin(news_win.NewsWin):
    START_X = 0
    HEIGHT_BLK = 4  # Block Height

    @classmethod
    def get_START_X_SELECTOR(cls) -> int:
        """Returns the starting X position of the headline block selector character."""
        return super().START_X_TXT - 2

    @classmethod
    def get_BLOCK_CAP(cls) -> int:
        """Returns how many headline blocks can fit in the text region."""
        return int(super().HEIGHT_TXT / cls.HEIGHT_BLK)

    def __init__(self, data: list) -> None:
        super().__init__(self.START_X)
        self.headline_blocks = headline_block_list.HeadlineBlockList(data)

    def get_new_selected_idx(self, incr):
        """Returns the index in self.headline_blocks of the HeadlineBlock object that
        should be the new selected block based on the index of the current selected
        block and the increment value."""
        return min(
            max(self.headline_blocks.get_selected_idx() + incr, 0),
            self.headline_blocks.get_len() - 1,
        )

    def get_selected_blk(self) -> headline_block.HeadlineBlock:
        return self.headline_blocks.get_selected()

    def move_horiz(self, cmd, is_main_line: bool = True) -> None:
        incr = commands.Commands.get_horiz_incr(cmd, is_main_line)
        self.headline_blocks.move_selected_horiz(incr, is_main_line, self.win)
        self.refresh_win()

    def init_blocks(self) -> None:
        self.headline_blocks.toggle_block_selected_status_and_print(0, self.win)
        self.headline_blocks.print_blocks(self.win)

    def move_vert(self, cmd: int) -> None:
        selection_incr = commands.Commands.get_vert_incr(cmd)
        new_selected_idx = self.get_new_selected_idx(selection_incr)
        if new_selected_idx not in self.headline_blocks.get_visible_block_idxs():
            self.headline_blocks.scroll_blocks(selection_incr)
            self.headline_blocks.print_blocks(self.win)
            self.print_box()
        self.headline_blocks.shift_selection_and_update(new_selected_idx, self.win)
        self.refresh_win()

    def load_selected_in_browser(self, prefix_choice: str | None) -> None:
        webbrowser.open_new(self.get_selected_blk().get_url(prefix_choice))
