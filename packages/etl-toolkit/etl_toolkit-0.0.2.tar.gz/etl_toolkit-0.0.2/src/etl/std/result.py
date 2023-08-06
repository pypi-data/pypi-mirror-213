#
# (C) Eithery Lab, 2023
# Result[T, E] class
# Represents the result of operation with two possible outcomes
# Result[T, E] = Ok(T) | Err(E)
# It contains either a success result OK(t) where t is a wrapped returned value of type T
# or an error result Err(e) where e is an error of type E explaining what went wrong
#
from __future__ import annotations
from etl.std import T, R
from typing import Generic, Optional, Callable, cast
from etl.std.error import Error, error as to_error
from etl.std.exceptions import InvalidResultException


class Result(Generic[T]):
    def __init__(self, value: Optional[T] = None, error: Error | str | None = None):
        self._value = value
        self._error = _convert_to_error(error)
        if isinstance(value, Error):
            self._value = None
            self._error = value


    @property
    def is_ok(self) -> bool:
        return self._error is None


    @property
    def is_error(self) -> bool:
        return not self.is_ok


    def unwrap(self) -> T:
        return self.expect("Cannot unwrap a value for the Error result")


    def expect(self, message: str) -> T:
        if self.is_ok:
            return cast(T, self._value)
        raise InvalidResultException(message)


    def ok(self) -> Optional[T]:
        return self._value if self.is_ok else None


    def err(self) -> Optional[Error]:
        return self._error if self.is_error else None


    def match(self, ok: Callable[[T], R], err: Callable[[Error], R]) -> R:
        return ok(cast(T, self._value)) if self.is_ok else err(cast(Error, self._error))


    def map(self, func: Callable[[T], R]) -> Result[R]:
        return self.match(
            ok = lambda v: Ok(func(v)),
            err = lambda e: Err(e)
        )


    def bind(self, func: Callable[[T], Result[R]]) -> Result[R]:
        return self.match(
            ok = lambda v: func(v),
            err = lambda e: Err(e)
        )


    def __repr__(self) -> str:
        return self.match(lambda v: f'Ok({v})', lambda e: f'Err({e})')




def Ok(value: Optional[T] = None) -> Result[T]:
    return Result(value)


def Err(error: Error) -> Result[T]:
    return Result(error = error)


# private

def _convert_to_error(error: Error | str | None) -> Optional[Error]:
    err = to_error(error) if error and isinstance(error, str) else error
    return cast(Optional[Error], err)
