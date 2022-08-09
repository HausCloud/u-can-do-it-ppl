from sqlalchemy.orm import Session
from models import api_models, db_models
from sqlalchemy.exc import IntegrityError

# Create


def create_user(db: Session, user: api_models.UserIn):
    new_user = db_models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        birth_date=user.birth_date,
        password=user.password,
        is_active=True,
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as e:
        return str(e)
    db.refresh(new_user)

    return new_user


# Read


def get_user_by_username(db: Session, username: str):
    return db.query(db_models.User).filter(db_models.User.username == username).first()


def get_permissions(db: Session, user: db_models.User, scopes: list):
    user_roles = (
        db.query(db_models.Role)
        .join(db_models.user_roles)
        .filter(db_models.Role.name.in_(scopes))
        .filter(db_models.user_roles.columns.user_id == user.id)
        .all()
    )

    return [role.name for role in user_roles]


# Update


# Delete
