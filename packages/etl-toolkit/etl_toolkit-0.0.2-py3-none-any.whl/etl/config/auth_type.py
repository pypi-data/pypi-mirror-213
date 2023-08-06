#
# (C) Eithery Lab, 2023
# Database authentication type
#
from enum import Enum


class AuthType(Enum):
    DEFAULT = 0
    USERNAME = 1
    SSPI = 2
