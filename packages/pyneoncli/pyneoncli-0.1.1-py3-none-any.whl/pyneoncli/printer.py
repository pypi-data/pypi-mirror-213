import collections
import json
import sys
from typing import Any
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import JsonLexer
from pygments import highlight

from pyneoncli.colortext import ColorText
from pyneoncli.neon import NeonObject, NeonProject, NeonBranch


# red-sea-544606

def dict_filter(d: dict, keys: list[str]):
    retValue = {}
    if keys is None or len(keys) == 0:
        return d
    for k, v in flatten(d):
        if k in keys:
            retValue[k] = v
    return retValue


def flatten(d: dict, root: str = None):
    for k, v in d.items():
        if type(v) == dict:
            yield from flatten(v, k)
        else:
            if root is None:
                yield k, v
            else:
                yield f"{root}.{k}", v


class Printer:

    def __init__(self, nocolor: bool = False, filters: list[str] = None) -> None:
        self._filters = filters
        self._nocolor = nocolor
        self._args = None
        self._c = ColorText(no_color=nocolor)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self._printer = Printer(nocolor=self._args.nocolor, filters=self._args.fieldfilter)
        return self._args

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, value):
        self._filters = value

    @property
    def nocolor(self):
        return self._nocolor

    @nocolor.setter
    def nocolor(self, value):
        self._nocolor = value

    def error(self, errmsg="ERROR: ", msg: str = "") -> None:
        print(f"{self._c.red('ERROR:')}{msg}", file=sys.stderr)

    def color_len(self, color, msg: str) -> tuple[int, str]:
        msg = color(msg)
        l = len(msg) - self._c.overhead
        return l, msg

    def name_id(self, p: NeonObject, name_label: str = "name: ", id_label: str = "id: ") -> str:

        name_label_len, name_label = self.color_len(self._c.green, name_label)
        id_label_len, id_label = self.color_len(self._c.green, id_label)
        name = p.name
        id = p.id

        name_str = "{0:{1}} {2:{3}}".format(name_label, name_label_len, name, len(name) + 5)
        id_str = "{0:{1}} {2:{3}}".format(id_label, id_label_len, id, len(id))
        return f"{name_str} {id_str}"

    def project_id(self, p: NeonProject) -> str:
        return self.name_id(p, name_label="Project name: ", id_label="Project id: ")

    def branch_id(self, b: NeonBranch) -> str:
        return self.name_id(b, name_label="Branch name: ", id_label="Branch id: ")

    @staticmethod
    def parse_name_id(name_id: str) -> tuple[None, None] | tuple[str | Any, Any | None]:
        if name_id is None or len(name_id) == 0:
            return None, None
        else:
            try:
                tokens = name_id.split()
                name = None
                _id = None
                for i, token in enumerate(tokens, start=0):
                    token = token.strip()
                    if token.endswith(":"):
                        if name is None:
                            name = tokens[i + 1].strip()
                        else:
                            _id = tokens[i + 1].strip()
                            break
            except ValueError:
                return None, None

        return name, _id

    @staticmethod
    def parse_name_id_list(name_id_list: list[str]) -> list[tuple[str | Any, Any | None]]:
        """

        @rtype: object
        """
        return [Printer.parse_name_id(name_id) for name_id in name_id_list]

    def pprint(self, obj) -> None:
        json_str = json.dumps(obj, indent=4, sort_keys=True)
        if self._nocolor or not sys.stdout.isatty():
            print(json_str)
        else:
            print(highlight(json_str, JsonLexer(), TerminalTrueColorFormatter()), end="")

    def print(self, obj: Any) -> None:
        if type(obj) == dict:
            o = dict_filter(obj, self._filters)
            self.pprint(o)
        elif isinstance(obj, collections.abc.Iterable):
            for i in obj:
                if type(i) == dict:
                    o = dict_filter(i, self._filters)
                    self.pprint(o)
                else:
                    self.pprint(i)
        else:
            self.pprint(obj)

    def name_id_list(self, d:list[NeonObject], name_label, id_label):
        if d is None:
            return []
        else:
            return [self.name_id(p, name_label, id_label) for p in d]
