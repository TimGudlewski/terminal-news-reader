import helper
import headlines_win
import article_win
import commands
import curses


class NewsReader:
    def __init__(self, use_saved=False) -> None:
        self.helper = helper.Helper(use_saved=use_saved)
        self.use_saved = use_saved

    def set_news_data(
        self,
        top: bool = True,
        lang: str = "en",
        query: str = "",
        prev_days: int = 0,
        sort_pop: bool = True,
    ) -> None:
        # TODO: Make these kwargs to streamline passing them to helper.set_news_from_newsapi?
        # TODO: Use helper.set_news_from_newsapi docstring here to explain kwargs.
        # Keep full helper docstring or put something like 'see NewsReader.set_news_data docstring'?
        if self.use_saved:
            self.helper.set_news_from_newsapi_file(1)
        else:
            self.helper.set_news_from_newsapi(
                top=top, lang=lang, query=query, prev_days=prev_days, sort_pop=sort_pop
            )

    def curses_setup(self) -> None:
        self.screen.clear()
        curses.use_default_colors()
        curses.init_pair(2, 196, -1)
        curses.init_pair(3, 27, -1)
        curses.curs_set(0)

    def news_main(self, stdscr: curses.window) -> None:
        self.screen = stdscr
        self.curses_setup()
        self.headlines_win = headlines_win.HeadlinesWin(self.helper.get_news_data())
        self.headlines_win.print_win_name("Headlines")
        self.headlines_win.init_blocks()
        self.headlines_win.print_box()
        self.screen.refresh()
        self.headlines_win.refresh_win()
        self.article_win = article_win.ArticleWin()
        self.article_win.print_win_name("Article")
        self.article_win.print_box()
        self.article_win.refresh_win()
        while True:
            cmd = self.screen.getch()
            if cmd in [
                commands.Commands.HEADLINES_DOWN,
                commands.Commands.HEADLINES_UP,
            ]:
                self.headlines_win.move_vert(cmd)
            elif cmd in [
                commands.Commands.MAIN_LINE_LEFT,
                commands.Commands.MAIN_LINE_RIGHT,
            ]:
                self.headlines_win.move_horiz(cmd)
            elif cmd in [
                commands.Commands.SECONDARY_LINE_LEFT,
                commands.Commands.SECONDARY_LINE_RIGHT
            ]:
                self.headlines_win.move_horiz(cmd, is_main_line=False)
            elif cmd == commands.Commands.ARTICLE_SELECT:
                selected_headline = self.headlines_win.get_selected_blk()
                self.article_win.load_page(selected_headline)
            elif cmd in [commands.Commands.ARTICLE_DOWN, commands.Commands.ARTICLE_UP]:
                self.article_win.move_vert(cmd)
            elif cmd in [
                commands.Commands.OPEN_BROWSER,
                commands.Commands.OPEN_BROWSER_ARCHIVE,
                commands.Commands.OPEN_BROWSER_TWELVE_FT,
            ]:
                self.headlines_win.load_selected_in_browser(
                    commands.Commands.get_browser_prefix_choice(cmd)
                )
            elif cmd == commands.Commands.SAVE_HEADLINES:
                self.helper.save_news(1)
            elif cmd == commands.Commands.QUIT:
                # TODO: Add save_news logic here? If not use_saved
                break


if __name__ == "__main__":
    nr = NewsReader(use_saved=True)
    nr.set_news_data()
    a = curses.wrapper(nr.news_main)
    print(a)
