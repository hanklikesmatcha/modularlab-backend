from uuid import UUID, uuid4

from pydantic import BaseModel


class ItemBase(BaseModel):
    category: str
    description: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID
    user_id: UUID = "0a837e3a-11ce-47c0-a411-489693a2b06b"

    class Config:
        orm_mode = True
