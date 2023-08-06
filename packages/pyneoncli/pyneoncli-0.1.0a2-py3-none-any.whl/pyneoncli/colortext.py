import sys

import colorama


class ColorText:

    def __init__(self, no_color: bool = False, std_file: object = sys.stdout, err_file: object = sys.stderr) -> None:
        self._no_color = no_color
        self._std_file = std_file
        self._err_file = err_file
        self._overhead = 0
        if not self.plain_text():
            self._overhead = len(self.green('x')) - len("x")

    @property
    def overhead(self):
        return self._overhead

    def plain_text(self) -> bool:
        if self._std_file.isatty():
            return self._no_color
        else:
            return True

    def color_text(self, color, msg: str) -> str:
        if self.plain_text():
            return msg
        else:
            return f"{color}{msg}{colorama.Style.RESET_ALL}"

    @staticmethod
    def plain(self, msg: str) -> str:
        return msg

    def black(self, msg: str) -> str:
        return self.color_text(colorama.Fore.BLACK, msg)

    def green(self, msg: str) -> str:
        return self.color_text(colorama.Fore.GREEN, msg)

    def red(self, msg: str) -> str:
        return self.color_text(colorama.Fore.RED, msg)

    def yellow(self, msg: str) -> str:
        return self.color_text(colorama.Fore.YELLOW, msg)

    def blue(self, msg: str) -> str:
        return self.color_text(colorama.Fore.BLUE, msg)

    def cyan(self, msg: str) -> str:
        return self.color_text(colorama.Fore.CYAN, msg)

    def orange(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTRED_EX, msg)

    def magenta(self, msg: str) -> str:
        return self.color_text(colorama.Fore.MAGENTA, msg)

    def white(self, msg: str) -> str:
        return self.color_text(colorama.Fore.WHITE, msg)

    def reset(self) -> str:
        return self.color_text(colorama.Style.RESET_ALL, "")

    def light_black(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTBLACK_EX, msg)

    def light_red(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTRED_EX, msg)

    def light_green(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTGREEN_EX, msg)

    def light_yellow(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTYELLOW_EX, msg)

    def light_blue(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTBLUE_EX, msg)

    def light_magenta(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTMAGENTA_EX, msg)

    def light_cyan(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTCYAN_EX, msg)

    def light_white(self, msg: str) -> str:
        return self.color_text(colorama.Fore.LIGHTWHITE_EX, msg)

    def bright(self, msg: str) -> str:
        return self.color_text(colorama.Style.BRIGHT, msg)

    def dim(self, msg: str) -> str:
        return self.color_text(colorama.Style.DIM, msg)
