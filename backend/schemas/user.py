from enum import Enum

class UserRole(str, Enum):
    # ADMIN = "admin"
    HOST = "host"
    CLIENT = "client"
