from typing import Union
from uuid import uuid4, UUID
from schemas.item_schema import Item

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    items: list[Item] = []

    class Config:
        orm_mode = True