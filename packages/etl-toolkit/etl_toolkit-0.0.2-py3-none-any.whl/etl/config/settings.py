#
# (C) Eithery Lab, 2023
# Settings module
# Contains TypedDict definitions for application and DB configuration settings
#
from typing import TypedDict


class DbConfigSettings(TypedDict, total = False):
    dialect: str
    driver: str
    host: str
    instance_name: str
    db_name: str
    connection: str


class AppConfigSettings(TypedDict, total = False):
    database: DbConfigSettings
    inbox: list[str]
    templates: list[str]
