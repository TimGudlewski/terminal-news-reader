import article_win
import requests
import html2text
import textwrap


class Article:
    USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
    )
    REFERER = "https://t.co/"
    ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    HEADERS = {
        "User-Agent": USER_AGENT,
        "Referer": REFERER,
        "Accept": ACCEPT,
    }

    def __init__(self, url: str):
        self.article_txt: list[str] = []
        self.offset = 0
        self.url = url

    def get_html(self):
        try:
            response = requests.get(self.url, headers=self.HEADERS)
            return response.text
        except Exception:
            pass

    def set_article_txt(self):
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = text_maker.ignore_images = True
        text_maker.bypass_tables = False
        html = self.get_html()
        if html:
            text = text_maker.handle(html)
            self.article_txt = textwrap.wrap(
                text, width=article_win.ArticleWin.WIDTH_TXT
            )

    def get_article_len(self):
        return len(self.article_txt)

    def incr_offset(self, incr):
        if self.article_txt:
            self.offset = max(self.offset + incr, 0)
            self.offset = min(
                (self.get_article_len() - 1)
                - (len(article_win.ArticleWin.get_line_range()) - 1),
                self.offset,
            )
        else:
            self.reset_offset()

    def reset_offset(self):
        self.offset = 0

    def get_offset_line(self, idx):
        return self.article_txt[idx + self.offset]
