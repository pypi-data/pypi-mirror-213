#
# (C) Eithery Lab, 2023
# Error results module
# Contains the set of common error results
#
from pathlib import Path
from etl.std import T
from etl.std.error import Error
from etl.std.result import Result, Err


def FileDoesNotExistError(file_path: Path) -> Result[T]:
    return Err(Error(f"The file '{file_path}' doesn't exist"))
