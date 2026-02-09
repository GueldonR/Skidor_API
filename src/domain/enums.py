from enum import Enum as PyEnum

# This file contains all enums used in the project.


class UserEnum(str, PyEnum):
    admin = "admin"
    user = "user"
