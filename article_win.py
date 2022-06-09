import news_win
import article
import headline_block
import commands


class ArticleWin(news_win.NewsWin):
    LINE_SPACING = 2  # Article line print spacing

    @classmethod
    def get_START_X(cls):
        return super().START_X + super().WIDTH + super().RIGHT_MARGIN + 1

    @classmethod
    def get_LINE_RANGE(cls) -> list[int]:
        return list(range(super().START_Y_TXT, super().END_Y_TXT, cls.LINE_SPACING))

    def __init__(self):
        super().__init__(self.get_START_X())
        self.is_article_displayed = False

    def set_article(self, article: article.Article):
        self.article = article

    def load_page(self, blk: headline_block.HeadlineBlock):
        art = article.Article(blk.get_url())
        art.set_article_txt()
        self.set_article(art)
        self.reset_win()
        self.print_article()
        self.set_displayed_status()
        self.refresh_win()

    def move_vert(self, cmd: int):
        incr = commands.Commands.get_vert_incr(cmd, is_article=True)
        if self.get_displayed_status():
            self.article.incr_offset(incr)
            self.print_article()
            self.refresh_win()

    def print_article(self):
        if self.article.get_article_len():
            display_height = min(len(self.get_LINE_RANGE()), self.article.get_article_len())
            for i in range(display_height):
                print_string = self.article.get_offset_line(i)
                line_length_diff = super().WIDTH_TXT - len(print_string)
                print_string += " " * line_length_diff
                self.win.addstr(self.get_LINE_RANGE()[i], super().START_X_TXT, print_string)
        else:
            self.win.addstr(4, super().START_X_TXT, "No article.")
        super().print_box()

    def reset_win(self):
        for i in range(len(self.get_LINE_RANGE())):
            print_string = " " * super().WIDTH_TXT
            self.win.addstr(self.get_LINE_RANGE()[i], super().START_X_TXT, print_string)

    def set_displayed_status(self):
        self.is_article_displayed = True

    def get_displayed_status(self):
        return self.is_article_displayed
