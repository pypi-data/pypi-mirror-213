import sys

from pyneoncli.colortext import ColorText


class Msg:
    def __init__(self, no_color=False):
        self._c = ColorText(no_color=no_color)

    def prompt(self, msg, end=""):
        return input(self._c.light_blue(msg))

    def msg(self, color=None, msg="", end="\n"):
        if color is None:
            print(f"{msg}", end=end)

            print(f"{self._c.blue(msg)}", end=end)

    def green(self, msg, end="\n"):
        print(f"{self._c.green(msg)}", end=end)

    def info(self, msg, end="\n"):
        print(f'{self._c.green("INFO")}: {msg}', end=end)

    def error(self, msg, end="\n"):
        print(f'{self._c.red("ERROR")}: {msg}', file=sys.stderr, end=end)

    def warning(self, msg, end="\n"):
        print(f'{self._c.orange("WARNING")}: {msg}', file=sys.stderr, end=end)

    def success(self, msg, end="\n"):
        print(f'{self._c.cyan(msg)}', end=end)

    def kv(self, key, value, end="\n", sep=": "):
        print(f'{self._c.cyan(key)}{sep}{value}', end=end)

    def error_kv(self, key, value, end="\n", sep=": "):
        print(f'{self._c.red(key)}{sep}{value}', end=end)

    def prompter(self, msg: str, expected: list[str] = None, yes: bool = False) -> str | None:
        if yes:
            return "y"

        response = self.prompt(msg)
        if expected is None:
            return response
        else:
            if response in expected:
                return response
            else:
                return None
