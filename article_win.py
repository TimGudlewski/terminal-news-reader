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
    def get_LINE_RANGE(cls) -> range:
        return range(super().START_Y_TXT, super().END_Y_TXT, cls.LINE_SPACING)

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
        self.refresh_win()

    def move_vert(self, cmd: int):
        incr = commands.Commands.get_vert_incr(cmd, is_article=True)
        if self.get_displayed_status():
            self.article.incr_offset(incr)
            self.print_article()
            self.refresh_win()

    def print_article(self):
        if self.article.get_article_len():
            for i, ypos in enumerate(self.get_LINE_RANGE()):
                if i < self.article.get_article_len():
                    line = self.article.get_offset_line(i)
                    print_string = line + self.get_blank_line_str(
                        self.get_line_length_diff(line)
                    )
                else:
                    print_string = self.get_blank_line_str()
                self.print_article_line(ypos, print_string)
            if self.article.get_article_len() > len(self.get_LINE_RANGE()):
                self.set_displayed_status()
        else:
            msg: str = "No article."
            extra_spaces: str = self.get_blank_line_str(self.get_line_length_diff(msg))
            self.print_article_line(self.get_LINE_RANGE()[0], msg + extra_spaces)
            for i in self.get_LINE_RANGE()[1:]:
                self.print_article_line(i, self.get_blank_line_str())
        super().print_box()

    def get_line_length_diff(self, line: str) -> int:
        return super().WIDTH_TXT - len(line)

    def get_blank_line_str(self, num_spaces: int = -1) -> str:
        if num_spaces < 0:
            num_spaces = super().WIDTH_TXT
        return " " * num_spaces

    def print_article_line(self, line_ypos: int, line_str: str) -> None:
        self.win.addstr(line_ypos, super().START_X_TXT, line_str)

    def reset_win(self):
        for i in self.get_LINE_RANGE():
            print_string = " " * super().WIDTH_TXT
            self.win.addstr(i, super().START_X_TXT, print_string)

    def set_displayed_status(self):
        self.is_article_displayed = True

    def get_displayed_status(self):
        return self.is_article_displayed
