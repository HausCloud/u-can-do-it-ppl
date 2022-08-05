from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from db import Base, SessionLocal, engine

user_role_association = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        server_default=text("gen_random_uuid()"),
    )
    username = Column(String, unique=True, nullable=False)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    # failed_login_attempts = Column(Integer, default=0, nullable=False)
    birth_date = Column(DateTime)
    created_date = Column(DateTime, server_default=text("now()"), nullable=False)
    last_updated_date = Column(DateTime, server_default=text("now()"), nullable=False)

    user_workouts = relationship("Workout", back_populates="user")
    user_maxes = relationship("UserMax", back_populates="user")
    roles = relationship(
        "Role", secondary=user_role_association, back_populates="users"
    )


class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship(
        "User", secondary=user_role_association, back_populates="roles"
    )


class Standard(Base):
    __tablename__ = "standard"

    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid4
    )
    name = Column(String, nullable=False)
    human_attribute = Column(String, nullable=False)
    weight = Column(Integer)
    repetitions = Column(Integer)
    beginner = Column(Integer, nullable=False)
    novice = Column(Integer, nullable=False)
    intermediate = Column(Integer, nullable=False)
    advanced = Column(Integer, nullable=False)
    elite = Column(Integer, nullable=False)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    standard_workouts = relationship("Workout", back_populates="standard")
    standard_maxes = relationship("UserMax", back_populates="standard")


class Workout(Base):
    __tablename__ = "workout"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    weight = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(String)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        primary_key=True,
    )
    user = relationship("User", back_populates="user_workouts")

    standard_id = Column(
        UUID(as_uuid=True),
        ForeignKey("standard.id"),
        primary_key=True,
    )
    standard = relationship("Standard", back_populates="standard_workouts")


class UserMax(Base):
    __tablename__ = "user_max"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    weight = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        primary_key=True,
    )
    user = relationship("User", back_populates="user_maxes")

    standard_id = Column(
        UUID(as_uuid=True),
        ForeignKey("standard.id"),
        primary_key=True,
    )
    standard = relationship("Standard", back_populates="standard_maxes")


class ValueSet(Base):
    __tablename__ = "value_set"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    display = Column(String, nullable=False)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    concepts = relationship("Concept", back_populates="value_set")


class Concept(Base):
    __tablename__ = "concept"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    display = Column(String, nullable=False)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_updated_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    value_set_id = Column(
        UUID(as_uuid=True),
        ForeignKey("value_set.id"),
        primary_key=True,
    )
    value_set = relationship("ValueSet", back_populates="standard_maxes")
