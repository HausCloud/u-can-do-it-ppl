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
    mia_perms = {
        "msg": "No permissions defined in 'scopes'",
        "status_code": status.HTTP_400_BAD_REQUEST,
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
    oneself_read = "Read current user's data"
    oneself_write = "Modify current user's data"
    oneself_read_workouts = "Read current user's workout(s)"
    oneself_read_maxes = "Read current user's max(es)"
    oneself_write_workouts = "Modify current user's workout(s)"
    oneself_write_maxes = "Modify current user's max(es)"
    others_read = "Read other user's data"
    others_write = "Modify other user's data"
    others_read_workouts = "Read other user's workout(s)"
    others_read_maxes = "Read other user's max(es)"
    others_write_workouts = "Modify other user's workout(s)"
    others_write_maxes = "Modify other user's max(es)"
