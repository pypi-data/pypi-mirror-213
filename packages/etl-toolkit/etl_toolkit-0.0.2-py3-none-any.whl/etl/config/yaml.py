#
# (C) Eithery Lab, 2023
# YAML configuration module
# Supports reading configuration from YAML files
#
import yaml
import etl.cli as cli
from pathlib import Path
from etl.config.settings import AppConfigSettings
from etl.std.error_results import FileDoesNotExistError
from etl.std.result import Result, Ok


def load(file_path: Path, verbose: bool = False) -> Result[AppConfigSettings]:
    if file_path.is_file():
        with open(file_path) as infile:
            settings: AppConfigSettings = yaml.safe_load(infile)
            if verbose:
                cli.echo(f"'{file_path.absolute()}' LOADED")
            return Ok(settings)

    return FileDoesNotExistError(file_path)
