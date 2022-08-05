from fastapi import HTTPException
from helper.enums import HttpStatusCodes


def get_http_exc(enum_attr: str = "", customer_header: dict = {}):
    headers = {"WWW-Authenticate": "Bearer"} if customer_header else customer_header

    try:
        enum = getattr(HttpStatusCodes, enum_attr)
        err = getattr(enum, "value")
    except AttributeError as e:
        err = None

    if not err:
        return HTTPException(
            status_code=500, detail="Unable to process request", headers=headers
        )
    return HTTPException(
        status_code=err["status_code"], detail=err["msg"], headers=headers
    )
