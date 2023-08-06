import pprint

import requests


class NeonTimeoutException(Exception):
    pass


class NeonAPIException(requests.exceptions.HTTPError):

    def __init__(self, *args, **kwargs):
        self._path = kwargs.pop("path", None)
        self._header = kwargs.pop("header", None)
        self._method = kwargs.pop("method", None)
        self._err = kwargs.pop("err", None)
        self._text = kwargs.pop("text", None)
        self._operation = kwargs.pop("operation", None)
        super().__init__(*args, **kwargs)

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        self._operation = value

    @property
    def path(self):
        return self._path

    @property
    def header(self):
        return self._header

    @property
    def method(self):
        return self._method

    @property
    def err(self):
        return self._err

    @property
    def text(self):
        return self._text

    @staticmethod
    def blank_if_none(label: str, value: str, end="\n") -> str:
        if value is None:
            return ""
        else:
            return f"{label}: {value}{end}"

    def __str__(self):
        if self._header is None:
            h = ""
        else:
            h = f"header: {pprint.pformat(self._header)}"
        m = self.blank_if_none("method", self._method)
        o = self.blank_if_none("operation", self._operation)
        p = self.blank_if_none("path", self._path)
        msg = self.blank_if_none("message", self._text)

        return f'{p}{h}{m}{o}{msg}'
