#
# (C) Eithery Lab, 2023
# Application configuration module
# Contains application level configuration settings
#
from __future__ import annotations
import os
import etl
import etl.config.yaml as yaml
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
from etl.config.database import DbConfiguration
from etl.config.settings import AppConfigSettings
from etl.paths import CONFIG_DIR, ROOT_DIR, TEMPLATES_DIR


CONFIG_FILE_NAME = '.etlrc.yml'
DEV_CONFIG_FILE_NAME = '.etlrc.dev.yml'
TEST_CONFIG_FILE_NAME = '.etlrc.test.yml'
PROD_CONFIG_FILE_NAME = '.etlrc.prod.yml'

DEV_ENV_NAMES = ['dev', 'development']
TEST_ENV_NAMES = ['test', 'testing']
PROD_ENV_NAMES = ['prod', 'production']

DEFAULT_INBOX_HOME = './data/inbox'
DEFAULT_ENVIRONMENT = 'prod'

ENVIRONMENT_ENV_VAR = 'ETL_ENVIRONMENT'
CONFIG_HOME_ENV_VAR = 'ETL_CONFIG_HOME'


class AppConfiguration:
    def __init__(
        self,
        db: Optional[DbConfiguration] = None,
        inbox: Optional[list[str]] = None,
        templates: Optional[list[str]] = None
    ):
        self._db = db or DbConfiguration()
        self._inbox = inbox or []
        self._templates = templates or []


    @property
    def db(self) -> DbConfiguration:
        return self._db


    @property
    def inbox(self) -> list[str]:
        return self._inbox or [DEFAULT_INBOX_HOME]


    @property
    def templates(self) -> list[Path]:
        return [self._to_absolute_path(template) for template in self._templates] or [TEMPLATES_DIR]


    @staticmethod
    def load(config_option: Optional[str] = None, verbose: bool = False) -> AppConfiguration:
        load_dotenv()
        return AppConfiguration()\
            ._load_from_home(verbose)\
            ._load_from_dir(CONFIG_DIR, verbose)\
            ._load_env_config(CONFIG_DIR, verbose)\
            ._load_from_dir(Path('.'), verbose)\
            ._load_from_env(CONFIG_HOME_ENV_VAR, verbose)\
            ._load_from_option(config_option, verbose)\
            ._apply_env_vars()


    def _load_from_home(self, verbose: bool) -> AppConfiguration:
        return self._load(Path.home(), verbose = verbose)


    def _load_from_dir(self, config_path: Path, verbose: bool) -> AppConfiguration:
        return self._load(config_path, verbose = verbose) if config_path else self


    def _load_from_env(self, env_var: str, verbose: bool) -> AppConfiguration:
        config_dir = os.getenv(env_var)
        return self._load(Path(config_dir), verbose = verbose) if config_dir else self


    def _load_from_option(self, option: Optional[str], verbose: bool) -> AppConfiguration:
        return self._load(Path(option), verbose = verbose) if option else self


    def _load_env_config(self, config_path: Path, verbose: bool) -> AppConfiguration:
        env = etl.current_environment()
        if env in DEV_ENV_NAMES:
            return self._load(config_path, DEV_CONFIG_FILE_NAME, verbose)
        if env in TEST_ENV_NAMES:
            return self._load(config_path, TEST_CONFIG_FILE_NAME, verbose)
        if env in PROD_ENV_NAMES:
            return self._load(config_path, PROD_CONFIG_FILE_NAME, verbose)
        return self


    def _load(
        self,
        config_dir: Path,
        config_file_name: str = CONFIG_FILE_NAME,
        verbose: bool = False
    ) -> AppConfiguration:
        config_path = config_dir.joinpath(config_file_name)
        return yaml.load(config_path, verbose).match(
            ok = self._merge_config,
            err = lambda _: self
        )


    def _apply_env_vars(self) -> AppConfiguration:
        return AppConfiguration(
            db = self.db.apply_env_vars(),
            inbox = self._inbox,
            templates = self._templates
        )


    def _merge_config(self, params: AppConfigSettings) -> AppConfiguration:
        return AppConfiguration(
            db = self.db.merge(params.get('database')),
            inbox = self._prepend_list(self._inbox, params.get('inbox', [])),
            templates = self._prepend_list(self._templates, params.get('templates', []))
        )


    def _prepend_list(self, source: list[str], values: list[str]) -> list[str]:
        return values + source if values else source


    def _to_absolute_path(self, template: str) -> Path:
        path = Path(template)
        return path if path.is_absolute() else ROOT_DIR.joinpath(path)
