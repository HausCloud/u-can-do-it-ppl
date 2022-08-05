from sqlalchemy.orm import Session
from models import api_models, db_models
from sqlalchemy.exc import IntegrityError


def get_user_by_username(db: Session, username: str):
    return db.query(db_models.User).filter(db_models.User.username == username).first()


def create_user(db: Session, user: api_models.UserCreate):
    db_user = db_models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        birth_date=user.birth_date,
        password=user.password,
        is_active=True,
    )

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        return str(e)
    db.refresh(db_user)

    return db_user
