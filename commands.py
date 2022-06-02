import curses

class Commands:
    HEADLINES_DOWN = curses.KEY_DOWN # 258
    HEADLINES_UP = curses.KEY_UP # 259
    HEADLINE_LEFT = curses.KEY_LEFT # 260
    HEADLINE_RIGHT = curses.KEY_RIGHT # 261
    SUMMARY_LEFT = 104 # h
    SUMMARY_RIGHT = 108 # l
    ARTICLE_DOWN = 106 # j
    ARTICLE_UP = 107 # k
    ARTICLE_SELECT = 10 # enter
    QUIT = 113 # q

    @classmethod
    def get_headlines_incr(cls, cmd):
        return ((cmd - cls.HEADLINES_DOWN) and -1) or 1

    @classmethod
    def get_article_incr(cls, cmd):
        return ((cmd - cls.ARTICLE_DOWN) and -1) or 1

    @classmethod
    def get_hl_horiz_incr(cls, cmd):
        return (cmd - cls.HEADLINE_LEFT) or -1

    @classmethod
    def get_sum_horiz_incr(cls, cmd):
        return ((cmd - cls.SUMMARY_LEFT) and 1) or -1
