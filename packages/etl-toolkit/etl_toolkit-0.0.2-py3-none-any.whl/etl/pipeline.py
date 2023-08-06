#
# (C) Eithery Lab, 2023
# ETL pipeline module
# Implements a pipeline for ETL process
#
import etl
import etl.cli as cli
from typing import Optional
from etl.config.app import AppConfiguration
from etl.std.result import Result, Ok
from etl.models.file_parsing_result import FileParsingResult


def run(
    files: tuple[str, ...],
    template: str,
    config_dir: Optional[str] = None,
    verbose: bool = False
) -> Result[None]:
    if verbose:
        cli.echo(f'Current environment: {etl.current_environment()}')
        cli.echo('Load configuration:')
    config = AppConfiguration.load(config_dir, verbose)
    result = parse_file(template, config)
    if result:
        if result.has_errors:
            cli.warning(f"File '{result.file_name}' has been loaded with errors", prefix = None, prepend_line = True)
            cli.warning(_build_stats_message(result), prefix = None)
        else:
            cli.success(f"File '{result.file_name}' has been loaded successfully")
            if result.has_warnings:
                cli.warning(f'Total {result.warnings_count} warnings detected', prefix = None)
    return Ok()


def parse_file(template: str, config: AppConfiguration) -> FileParsingResult:
    return FileParsingResult('file_name')


# private

def _build_stats_message(result: FileParsingResult) -> str:
    message = f'Total {result.errors_count} errors'
    if result.has_warnings:
        message += f' and {result.warnings_count} warnings'
    return message + ' detected'
