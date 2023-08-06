#
# (C) Eithery Lab, 2023
# ETL top-level package primitives and service functions
#
import os
from dotenv import load_dotenv
from etl.config.app import ENVIRONMENT_ENV_VAR, DEFAULT_ENVIRONMENT

load_dotenv()


def current_environment() -> str:
    env = os.getenv(ENVIRONMENT_ENV_VAR)
    return env.lower() if env else DEFAULT_ENVIRONMENT
