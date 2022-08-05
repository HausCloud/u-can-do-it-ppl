from enum import Enum
from fastapi import status


class HttpStatusCodes(Enum):
    general = {
        "msg": "Unable to process request",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    bad_general = {
        "msg": "Bad request",
        "status_code": status.HTTP_400_BAD_REQUEST,
    }
    bad_pass = {
        "msg": "Password doesn't match",
        "status_code": status.HTTP_400_BAD_REQUEST,
    }
    bad_perms = {
        "msg": "Permissions are invalid",
        "status_code": status.HTTP_403_FORBIDDEN,
    }
    # too_many_login = {
    #     "msg": "Max login attempt exceeded",
    #     "status_code": status.HTTP_429_TOO_MANY_REQUESTS,
    # }
    exist_user = {
        "msg": "Username already registered",
        "status_code": status.HTTP_400_BAD_REQUEST,
    }
    no_user = {
        "msg": "Username isn't registered",
        "status_code": status.HTTP_404_NOT_FOUND,
    }
    inactive_user = {
        "msg": "User is inactive",
        "status_code": status.HTTP_423_LOCKED,
    }
    # mia_username = {
    #     "msg": "Username is required",
    #     "status_code": status.HTTP_400_BAD_REQUEST,
    # }
    # mia_pass = {
    #     "msg": "Password is required",
    #     "status_code": status.HTTP_400_BAD_REQUEST,
    # }


class Scopes(Enum):
    oneself = "Read current user's data"
    oneself_workouts = "Read current user's workout(s)"
    oneself_maxes = "Read current user's max(es)"
