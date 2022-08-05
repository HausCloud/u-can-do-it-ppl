from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class WorkoutBase(BaseModel):
    weight: int
    sets: int
    repetitions: int
    created_date: datetime
    notes: str | None = None


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: UUID
    user_id: UUID
    standard_id: UUID

    class Config:
        orm_mode = True


class UserMaxBase(BaseModel):
    weight: int


class UserMaxBaseCreate(UserMaxBase):
    pass


class UserMax(BaseModel):
    id: UUID
    user_id: UUID
    standard_id: UUID

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str
    is_active: bool
    birth_date: datetime | None = None
    created_date: datetime
    last_updated_date: datetime


class UserCreate(UserBase):
    is_active: bool = True
    created_date: datetime | None = None
    last_updated_date: datetime | None = None


class User(UserBase):
    id: UUID
    user_workouts: list[Workout] = []
    user_maxes: list[UserMax] = []

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    access_token: str
    token_type: str
    scopes: list[str] = []


class TokenCreate(TokenBase):
    pass


class TokenData(TokenBase):
    username: str
    access_token: str | None = None
    token_type: str | None = None
    scopes: list[str]
