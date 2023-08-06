#
# (C) Eithery Lab, 2023
# Error class
# Represents a basic value for error result
#
from __future__ import annotations
from typing import Optional


class Error:
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        description: Optional[str] = None,
        inner_error: Optional[Error] | Optional[BaseException] = None
    ):
        self._message = message
        self._code = code
        self._description = description
        self._inner_error = inner_error


    @property
    def code(self) -> Optional[str]:
        return self._code


    @property
    def message(self) -> str:
        return self._message


    @property
    def description(self) -> Optional[str]:
        return self._description


    def __repr__(self) -> str:
        return self._message


def error(message: str) -> Error:
    return Error(message)
