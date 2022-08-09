from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ValueSet(BaseModel):
    id: UUID
    code: str
    display: str
    description: str | None
    created_date: datetime
    last_updated_date: datetime

    class Config:
        orm_mode = True


class Concept(BaseModel):
    id: UUID
    code: str
    display: str
    description: str | None
    created_date: datetime
    last_updated_date: datetime

    value_set_id: UUID

    class Config:
        orm_mode = True


class Standard(BaseModel):
    name: str
    human_attribute: str
    weight: int | None = None
    repetitions: int
    beginner: int
    novice: int
    intermediate: int
    advanced: int
    elite: int
    description: str
    created_date: datetime
    last_updated_date: datetime

    lift_type_id: UUID


class WorkoutBase(BaseModel):
    weight: int
    sets: int
    repetitions: int
    created_date: datetime
    notes: str | None = None

    user_id: UUID
    standard_id: UUID


class WorkoutCreate(BaseModel):
    pass


class Workout(WorkoutBase):
    id: UUID
    user_id: UUID
    standard_id: UUID

    class Config:
        orm_mode = True


class UserMaxBase(BaseModel):
    weight: int


class UserMaxBaseCreate(BaseModel):
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


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    birth_date: datetime | None = None
    is_active: bool = True
    created_date: datetime = None
    last_updated_date: datetime = None


class UserOut(BaseModel):
    id: UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    birth_date: datetime | None = None
    user_workouts: list[Workout] = []
    user_maxes: list[UserMax] = []

    class Config:
        orm_mode = True


# class TokenBase(BaseModel):
#     access_token: str
#     token_type: str
#     scopes: list[str] = []


class TokenIn(BaseModel):
    username: str
    scopes: list[str] = []

class TokenOut(BaseModel):
    access_token: str
    token_type: str
