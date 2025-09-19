from typing import Optional

from sqlmodel import SQLModel


class LevelBase(SQLModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = None


class LevelCreate(LevelBase):
    pass


class LevelRead(LevelBase):
    id: int

    class Config:
        orm_mode = True


class LevelUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
