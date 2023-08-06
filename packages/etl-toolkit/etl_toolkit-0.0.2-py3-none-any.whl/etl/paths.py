#
# (C) Eithery Lab, 2023
# ETL paths module
# Contains the set of path constants
#
from pathlib import Path

ROOT_DIR: Path = Path(__file__).parent.parent.parent
CONFIG_DIR: Path = ROOT_DIR.joinpath("config")
TEMPLATES_DIR: Path = CONFIG_DIR.joinpath("templates")
TEST_DIR: Path = ROOT_DIR.joinpath("tests")
