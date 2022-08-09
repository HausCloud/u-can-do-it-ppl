from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestFormStrict,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from helper.enums import Scopes
from helper.utils import get_http_exc, modify_scope_name
from pydantic import ValidationError
from sqlalchemy.orm import Session
from models import api_models, db_models

# from sqlalchemy import text
# import json
# from pprint import pprint
import db_ops

db_models.Base.metadata.create_all(bind=db_models.engine)


def get_session():
    db = db_models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = "be385abb3f8683552e9a1e0ead03f064ccfd489aa827c1f17b3ce1915d867429"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ACCESS_TOKEN_EXTENSION_MINUTES = 15
# MAX_FAILED_LOGIN_ATTEMPTS = 3
SCOPES = {modify_scope_name(scope): scope.value for scope in Scopes}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=SCOPES)
fastapi = FastAPI()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXTENSION_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
):
    auth_val = (
        f'Bearer scope="{security_scopes.scope_str}"'
        if security_scopes.scopes
        else f"Bearer"
    )
    credentials_exception = get_http_exc("general", customer_header=auth_val)

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = api_models.TokenIn(username=username, scopes=token_scopes)
    except (JWTError, ValidationError) as e:
        raise credentials_exception

    user = db_ops.get_user_by_username(db, token_data.username)

    if user is None:
        raise credentials_exception

    print(security_scopes.scopes)
    print(token_data.scopes)

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise get_http_exc("bad_perms", customer_header=auth_val)
    return user


def get_current_active_user(
    current_user: api_models.UserOut = Depends(get_current_user),
):
    if not current_user.is_active:
        raise get_http_exc("inactive_user")
    return current_user


# Routes / Endpoints


@fastapi.post("/token", response_model=api_models.TokenOut)
def login_for_access_token(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    db: Session = Depends(get_session),
):
    db_user = db_ops.get_user_by_username(db, form_data.username)

    if not db_user:
        raise get_http_exc("no_user")
    # if db_user.failed_login_attempts > MAX_FAILED_LOGIN_ATTEMPTS:
    #     raise get_http_exc("too_many_login")
    elif not verify_password(
        plain_password=form_data.password, hashed_password=db_user.password
    ):
        # db_ops.increment_failed_login_attempts(db, existing_user=db_user)
        raise get_http_exc("bad_pass")
    elif db_user.is_active == False:
        raise get_http_exc("inactive_user")
    elif not form_data.scopes:
        raise get_http_exc("mia_perms")

    scopes = db_ops.get_permissions(db, db_user, form_data.scopes)
    print(scopes)
    access_token = create_access_token(
        data={"sub": db_user.username, "scopes": scopes},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@fastapi.post("/user/", response_model=api_models.UserOut)
def create_user(user: api_models.UserIn, db: Session = Depends(get_session)):
    existing_user = db_ops.get_user_by_username(db, user.username)
    if existing_user:
        raise get_http_exc("exist_user")

    user.password = get_password_hash(user.password)

    new_user = db_ops.create_user(db=db, user=user)

    if type(new_user) == str:
        print(f"ERROR: {new_user}")
        raise get_http_exc("general")

    return new_user


@fastapi.get("/user/oneself", response_model=api_models.UserOut)
def read_user_oneself(
    current_user: api_models.UserBase = Security(
        get_current_active_user, scopes=[modify_scope_name(Scopes.oneself_read)]
    )
):
    return current_user
