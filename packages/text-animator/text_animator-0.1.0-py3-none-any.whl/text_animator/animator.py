import random
from time import sleep
from enum import Enum
from ascii_animator import Animator, Animation, Speed


class Effect(Enum):
    RANDOM = 1
    LEFT_TO_RIGHT = 2
    RIGHT_TO_LEFT = 3


class Border():

    def __init__(self, tm=1, bm=1, lm=1, rm=1, tp=1, bp=1, lp=1, rp=1):
        self.tm = tm
        self.bm = bm
        self.lm = lm
        self.rm = rm
        self.tp = tp
        self.bp = bp
        self.lp = lp
        self.rp = rp

    def get_border(self, text_length, text_height):
        border = []

        # right edge
        re = self.lm + self.lp + 1 + text_length + self.rp  # 1 is for the left border char

        # top edge
        te = self.tm

        # bottom edge
        be = self.tm + 1 + self.tp + text_height + self.bp  # 1 is for the top border char

        # right bottom edge
        border.append(((be, re), 9499))  # ┛

        # right bottom padding - right text height - right top padding
        y = be
        for _ in range(self.bp + text_height + self.tp):
            y -= 1
            border.append(((y, re), 9475))  # ┃

        # right top edge
        border.append(((self.tm, re), 9491))  # ┓

        # upper border
        for index in range(re, self.lm, -1):  # ━ 9473
            border.append(((self.tm, index), 9473))

        # left top edge
        border.append(((self.tm, self.lm), 9487))  # ┏ 9487

        # left top padding - left text height - left bottom padding
        y = te
        for _ in range(self.tp + text_height + self.bp):
            y += 1
            border.append(((y, self.lm), 9475))  # ┃ 9475

        # left bottom edge
        border.append(((be, self.lm), 9495))  # ┗ 9495

        # lower border
        for index in range(self.lm, re):
            border.append(((be, index), 9473))  # ━ 9473

        return border

    @property
    def text_start_pos(self):
        return((self.tm + 1 + self.tp, self.lm + 1 + self.lp))

    @property
    def height(self):
        return(self.tm + 1 + self.tp + self.bp + 1 + self.bm)

    @property
    def length(self):
        return(self.lm + 1 + self.lp + self.rp + 1 + self.rm)


class TextAnimation(Animation):

    def __init__(self, text, effect=Effect.LEFT_TO_RIGHT, speed=Speed.FAST, border=None):
        self.text = text
        self.effect = effect
        self.speed = speed
        self.text_lines = [line.strip() for line in self.text.splitlines() if line]
        text_length = len(max(self.text_lines, key=len))
        text_height = len(self.text_lines)
        length = text_length
        height = text_height
        self.border = border
        if self.border:
            height += self.border.height
            length += self.border.length
        self.y_size = height
        self.x_size = length
        self.clear_grid()
        self._text = self._init_text()
        self._border = None
        if self.border:
            self._border = border.get_border(text_length, text_height)

    def _init_text(self):

        def _add_random():
            chars = []
            for line_count, line in enumerate(self.text_lines):
                for item in random.sample(list(enumerate(line)), len(line)):
                    index = item[0]
                    char = item[1]
                    chars.append(((y_start_pos + line_count, x_start_pos + index), ord(char)))
            for item in random.sample(chars, len(chars)):
                items.append(item)

        def _add_left_to_right():
            chars = []
            for line_count, line in enumerate(self.text_lines):
                for index, char in enumerate(line):
                    chars.append(((y_start_pos + line_count, x_start_pos + index), ord(char)))
            for item in reversed(chars):
                items.append(item)

        def _add_right_to_left():
            for line_count, line in enumerate(self.text_lines):
                for index, char in enumerate(line):
                    items.append(((y_start_pos + line_count, x_start_pos + index), ord(char)))

        y_start_pos = 0
        x_start_pos = 0
        if self.border:
            (y_start_pos, x_start_pos) = self.border.text_start_pos
        items = []
        if self.effect == Effect.RANDOM:
            _add_random()
        elif self.effect == Effect.LEFT_TO_RIGHT:
            _add_left_to_right()
        elif self.effect == Effect.RIGHT_TO_LEFT:
            _add_right_to_left()
        return items

    def _update_grid(self, items):
        item = items.pop()
        y_pos = item[0][0]
        x_pos = item[0][1]
        ucode = item[1]
        self._grid[y_pos][x_pos] = chr(ucode)

    @property
    def grid(self):
        return self._grid

    def clear_grid(self):
        self._grid = [[' ' for x in range(self.x_size)] for y in range(self.y_size)]

    def cycle(self):
        if self._text:
            self._update_grid(self._text)
        else:
            if self._border:
                self._update_grid(self._border)
            else:
                return True

    def __call__(self):
        Animator(animation=self, speed=self.speed, show_axis=False, max_loops=1)
