import news_win
import headline_block_list
import commands
import webbrowser
import helper


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

    def move_horiz(self, cmd, is_main_line: bool = True) -> None:
        incr = commands.Commands.get_horiz_incr(cmd, is_main_line)
        self.headline_blocks.move_selected_horiz_and_print(incr, is_main_line, self.win)
        self.refresh_win()

    def init_blocks(self) -> None:
        self.headline_blocks.toggle_block_selected_status_and_print(0, self.win)
        self.headline_blocks.print_blocks(self.win)

    def new_init_blocks(self) -> None:
        self.headline_blocks.new_print_blocks(self.win)
        self.headline_blocks.print_block_selector_char(self.win)

    def new_move_vert(self, cmd: int) -> None:
        # Arrow down is increment of 1. Arrow up is increment of -1.
        selection_incr: int = commands.Commands.get_vert_incr(cmd)
        old_selection_idx: int = self.headline_blocks.get_selection_idx()
        if old_selection_idx + selection_incr in range(
            0, self.headline_blocks.get_len()
        ):
            self.headline_blocks.incr_selection_idx(selection_incr)
            new_sel_idx = self.headline_blocks.get_selection_idx()
            write_str = (
                "new sel_idx: "
                + str(new_sel_idx)
                + "\nold selected block char: "
                + str(self.headline_blocks.get_block_at_idx(old_selection_idx).get_selector_char())
                + "\nold sel_idx: "
                + str(old_selection_idx)
                + "\n"
            )
            h = helper.Helper()
            h.save_debug_txt(write_str, 9)
            self.headline_blocks.print_block_selector_char(self.win, old_selection_idx)
            old_visi_range_start = self.headline_blocks.get_visi_range_start(
                old_selection_idx
            )
            if old_visi_range_start != self.headline_blocks.get_visi_range_start():
                self.headline_blocks.new_print_blocks(self.win)
            self.headline_blocks.print_block_selector_char(self.win)
            self.refresh_win()

    def move_vert(self, cmd: int) -> None:
        selection_incr = commands.Commands.get_vert_incr(cmd)
        new_selected_idx = self.get_new_selected_idx(selection_incr)
        if new_selected_idx not in self.headline_blocks.get_visible_block_idxs():
            self.headline_blocks.scroll_blocks(selection_incr)
            self.headline_blocks.print_blocks(self.win)
            self.print_box()
        self.headline_blocks.move_selection_vert_and_print(new_selected_idx, self.win)
        self.refresh_win()

    def load_selected_in_browser(self, prefix_choice: str | None) -> None:
        webbrowser.open_new(
            self.headline_blocks.get_selected_blk().get_url(prefix_choice)
        )
