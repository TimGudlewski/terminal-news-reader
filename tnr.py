#!/usr/bin/env python3

import curses
import json


def read_json_file(path: str):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


class windims:
    H = 30                      # Height
    W = 60                      # Width
    SY = SX1 = 0                # Start Y, Start X Window 1
    SX2 = 65                    # Start X Window 2
    M = 3                       # Margin
    TSX = TSY = M + 1           # Start X/Y Text Region
    TEY = H - (M - 1)           # End Y Text Region
    WT = W - (TSX * 2)          # Width Text Region
    HT = TEY - TSY              # Height Text Region
    BH = 4                      # Block Height
    RTB = int(HT / BH)          # Range of Text in Blocks
    SelPosX = M - 1             # Selector character X position


class Block:
    LT = ['title', 'description']   # Line types
    LYB = [0, 2]                    # Line Ys within block
    LCPAIRS = [2, 0]                # Line color pairs


    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.date = kwargs.get('publishedAt')
        self.source = kwargs.get('source')['name']
        self.author = kwargs.get('author')
        self.url = kwargs.get('url')
        self.description = kwargs.get('description')
        self.content = kwargs.get('content')
        self.lines = []
        for i, line_type in enumerate(self.LT):
            block_line = BlockLine(ltype=line_type,
                                   yblock=self.LYB[i],
                                   fline=getattr(self, line_type),
                                   cpair=self.LCPAIRS[i])
            self.lines.append(block_line)
        self.position = None
        self.selected = False


    def update_lines(self, incr):
        self.position += incr
        for line in self.lines:
            line.update_ytext(self.position)


    def remove_ytext(self):
        for line in self.lines:
            line.ytext = None


class BlockLine:
    def __init__(self, **kwargs):
        self.ltype = kwargs.get('ltype')     # Line type
        self.yblock = kwargs.get('yblock')   # Y position of line within the block
        self.ytext = kwargs.get('ytext')     # Y position of line within the text region
        self.fline = kwargs.get('fline')     # Full text of line
        self.cline = self.fline[:windims.WT] # Current displayed text of line
        self.cpair = kwargs.get('cpair') # Color pair


    def update_ytext(self, bpos):
        self.ytext = windims.TSY + (bpos * windims.BH) + self.yblock


class News:
    def __init__(self, data):
        self.blocks = [Block(**article) for article in data]
        for i in range(windims.RTB):
            self.blocks[i].position = i
            self.blocks[i].update_lines(0)
        for j in range(windims.RTB, len(self.blocks)):
            self.blocks[j].position = windims.RTB
        self.blocks[0].selected = True


    def get_block_idxs_by_position(self, pos_range):
        return [bi for bi in range(len(self.blocks)) if self.blocks[bi].position in pos_range]


    def update_blocks(self, bibp, up=True):
        if up:
            incr = -1
            self.blocks[bibp[0]].position = -1
            self.blocks[bibp[0]].remove_ytext()
        else:
            incr = 1
            self.blocks[bibp[-1]].position = windims.RTB
            self.blocks[bibp[0]].remove_ytext()
        new_range_start = bibp[0] - incr
        new_range_end = (bibp[-1] - incr) + 1
        for i in range(new_range_start, new_range_end):
            self.blocks[i].update_lines(incr)
        return [new_range_start, new_range_end]


    def print_blocks(self, target_idxs):
        for i in target_idxs:
            for l in self.blocks[i].lines:
                self.win1.addstr(l.ytext, windims.TSX, l.cline, curses.color_pair(l.cpair))


    def get_selected_idx(self):
        return next(i for i in range(len(self.blocks)) if self.blocks[i].selected)


    def update_selected(self, old_idx, new_idx):
        self.win1.addch(self.blocks[old_idx].lines[0].ytext, windims.M - 1, ' ')
        self.blocks[old_idx].selected = False
        self.blocks[new_idx].selected = True


    def print_selector(self, idx):
        self.win1.addch(self.blocks[idx].lines[0].ytext, windims.M - 1, '*')


    def print_box(self):
        self.win1.box('|', '-')


    def main(self, stdscr):
        stdscr.clear()
        curses.use_default_colors()
        curses.init_pair(2, 196, -1)
        curses.init_pair(3, 27, -1)
        curses.curs_set(0)

        self.win1 = curses.newwin(windims.H, windims.W, windims.SY, windims.SX1)
        self.win1.keypad(True)
        self.win1.scrollok(True)

        self.win1.setscrreg(windims.TSX, windims.TEY)
        stdscr.refresh()
        self.win1.refresh()

        self.win1.addstr(windims.M - 1, windims.M + 1, "Headlines", curses.A_BOLD | curses.A_ITALIC | curses.color_pair(3))
        self.win2 = curses.newwin(windims.H, windims.W, windims.SY, windims.SX2)
        self.win2.addstr(2, 2, "hello2")
        self.win2.box('|', '-')
        self.win2.refresh()
        init_bibp = self.get_block_idxs_by_position(range(windims.RTB))
        self.print_blocks(init_bibp)
        self.print_selector(0)
        self.print_box()
        self.win1.refresh()

        while (True):
            cmd = self.win1.getch()
            cmd_options = [curses.KEY_DOWN, curses.KEY_UP]
            if cmd in cmd_options:
                if cmd == cmd_options[0]:
                    selection_incr = 1
                elif cmd == cmd_options[1]:
                    selection_incr = -1
                old_selected_idx = self.get_selected_idx()
                new_selected_idx = min(max(old_selected_idx + selection_incr, 0), len(self.blocks) - 1)
                bibp = self.get_block_idxs_by_position(range(windims.RTB))
                if new_selected_idx not in bibp:
                    if new_selected_idx > bibp[-1]:
                        self.win1.scroll(windims.BH)
                        new_range = self.update_blocks(bibp)
                    elif new_selected_idx < bibp[0]:
                        new_range = self.update_blocks(bibp, up=False)
                    new_bibp = self.get_block_idxs_by_position(range(windims.RTB))
                    self.print_blocks(new_bibp)
                    self.print_box()
                self.update_selected(old_selected_idx, new_selected_idx)
                try:
                    self.print_selector(new_selected_idx)
                except Exception:
                    return new_range
                self.win1.refresh()
            elif cmd == 113:
                break
            else:
                return cmd


news_data = read_json_file('/home/tim/test_json.json')
news = News(news_data['articles'])
a = curses.wrapper(news.main)
print(a)
