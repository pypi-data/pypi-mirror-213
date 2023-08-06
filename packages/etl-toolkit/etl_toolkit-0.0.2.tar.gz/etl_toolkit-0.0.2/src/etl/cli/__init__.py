#
# (C) Eithery Lab, 2023
# CLI package level primitives
# Provides the app version and service functions for stdout/stderr colorful output
#
import click
import importlib.metadata
from typing import Optional


_ERROR_COLOR = 'red'
_WARNING_COLOR = 'yellow'
_SUCCESS_COLOR = 'green'

APP_DISPLAY_NAME = 'ETL CLI Toolkit'

__version__ = importlib.metadata.version('etl-toolkit')


def error(message: str, prefix: Optional[str] = 'Error:', prepend_line: bool = True) -> None:
    _display_message(message, prefix, color = _ERROR_COLOR, prepend_line = prepend_line)


def warning(message: str, prefix: Optional[str] = 'Warning:', prepend_line: bool = False) -> None:
    _display_message(message, prefix, color = _WARNING_COLOR, prepend_line = prepend_line)


def success(message: str, prefix: Optional[str] = None, prepend_line: bool = True) -> None:
    _display_message(message, prefix, color = _SUCCESS_COLOR, prepend_line = prepend_line)


def echo(message: str) -> None:
    click.echo(message)


# private

def _display_message(message: str, prefix: Optional[str], color: str, prepend_line: bool = False) -> None:
    if prepend_line:
        click.echo()
    combined_message = ' '.join(filter(None, [prefix, message]))
    click.secho(combined_message, fg = color)
