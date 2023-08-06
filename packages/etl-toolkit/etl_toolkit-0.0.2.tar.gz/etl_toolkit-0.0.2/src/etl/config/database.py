#
# (C) Eithery Lab, 2023
# Database configuration module
# Contains database related configuration settings
#
from __future__ import annotations
import os
from typing import Optional
from etl.config.auth_type import AuthType
from etl.config.settings import DbConfigSettings


DEFAULT_DB_DIALECT = 'mssql'
DEFAULT_ODBC_DRIVER = 'ODBC Driver 17 for SQL Server'
DEFAULT_DB_HOST = 'localhost'
DEFAULT_DB_NAME = 'etl_db'
_SSPI_AUTH = ['sspi', 'windows']

DB_HOST_ENV_VAR = 'ETL_DB_HOST'
DB_INSTANCE_ENV_VAR = 'ETL_DB_INSTANCE'
DB_NAME_ENV_VAR = 'ETL_DB_NAME'
DB_USER_ENV_VAR = 'ETL_DB_USER'
DB_PWD_ENV_VAR = 'ETL_DB_PWD'               # nosec
DB_AUTH_TYPE_ENV_VAR = 'DB_AUTH_TYPE'


class DbConfiguration:
    def __init__(
        self,
        dialect: Optional[str] = None,
        driver: Optional[str] = None,
        host: Optional[str] = None,
        instance_name: str = '',
        db_name: Optional[str] = None,
        connection_type: Optional[str] = None,
        uid: Optional[str] = None,
        pwd: Optional[str] = None
    ):
        self._dialect = dialect or DEFAULT_DB_DIALECT
        self._driver = driver or DEFAULT_ODBC_DRIVER
        self._host = host or DEFAULT_DB_HOST
        self._instance_name = instance_name or ''
        self._db_name = db_name or DEFAULT_DB_NAME
        self._connection_type = connection_type or 'default'
        self._uid = uid
        self._pwd = pwd


    @property
    def host(self) -> str:
        return f'{self._host}\\{self._instance_name}' if self._instance_name else self._host


    @property
    def db_name(self) -> str:
        return self._db_name


    @property
    def auth_type(self) -> AuthType:
        return AuthType.SSPI if self._connection_type in _SSPI_AUTH else AuthType.DEFAULT


    @property
    def uid(self) -> Optional[str]:
        return self._uid


    @property
    def pwd(self) -> Optional[str]:
        return self._pwd


    @property
    def connection_string(self) -> str:
        prefix = '' if self.auth_type == AuthType.SSPI else f'{self._uid}:{self._pwd}@'
        return f'mssql+pyodbc://{prefix}{self.host}/{self.db_name}?driver={self._driver}'


    def merge(self, params: Optional[DbConfigSettings]) -> DbConfiguration:
        return DbConfiguration(
            dialect = params.get('dialect', self._dialect),
            driver = params.get('driver', self._driver),
            host = params.get('host', self._host),
            instance_name = params.get('instance_name', self._instance_name),
            db_name = params.get('db_name', self._db_name),
            connection_type = params.get('connection', self._connection_type),
            uid = self._uid,
            pwd = self._pwd
        ) if params else self


    def apply_env_vars(self) -> DbConfiguration:
        return DbConfiguration(
            dialect = self._dialect,
            driver = self._driver,
            host = os.getenv(DB_HOST_ENV_VAR, self._host),
            instance_name = os.getenv(DB_INSTANCE_ENV_VAR, self._instance_name),
            db_name = os.getenv(DB_NAME_ENV_VAR, self._db_name),
            connection_type = os.getenv(DB_AUTH_TYPE_ENV_VAR, self._connection_type),
            uid = os.getenv(DB_USER_ENV_VAR, self._uid),
            pwd = os.getenv(DB_PWD_ENV_VAR, self._pwd)
        )
