import curses


class Commands:
    HEADLINES_DOWN = curses.KEY_DOWN  # 258
    HEADLINES_UP = curses.KEY_UP  # 259
    HEADLINE_LEFT = curses.KEY_LEFT  # 260
    HEADLINE_RIGHT = curses.KEY_RIGHT  # 261
    SUMMARY_LEFT = 104  # h
    SUMMARY_RIGHT = 108  # l
    ARTICLE_DOWN = 106  # j
    ARTICLE_UP = 107  # k
    ARTICLE_SELECT = 10  # enter
    OPEN_BROWSER = 98  # b
    OPEN_BROWSER_TWELVE_FT = 116  # t
    OPEN_BROWSER_ARCHIVE = 97  # a
    SAVE_HEADLINES = 115  # s
    QUIT = 113  # q

    @classmethod
    def get_vert_incr(cls, cmd: int, is_article: bool = False) -> int:
        """A positive increment advances (moves down) through the blocks.
        A negative increment retreats (moves up) through the blocks.
        """
        down_cmd = (is_article and cls.ARTICLE_DOWN) or cls.HEADLINES_DOWN
        return ((cmd - down_cmd) and -1) or 1

    @classmethod
    def get_horiz_incr(cls, cmd: int, is_summary: bool = False) -> int:
        """A positive increment advances (moves right) through the block line.
        A negative increment retreats (moves left) through the block line.
        """
        left_cmd = (is_summary and cls.SUMMARY_LEFT) or cls.HEADLINE_LEFT
        return ((cmd - left_cmd) and 1) or -1

    @classmethod
    def get_browser_prefix_choice(cls, cmd: int) -> str | None:
        if cmd == cls.OPEN_BROWSER_ARCHIVE:
            return "archive"
        elif cmd == cls.OPEN_BROWSER_TWELVE_FT:
            return "twelve"
