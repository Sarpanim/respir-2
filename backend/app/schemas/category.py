from typing import Optional

from sqlmodel import SQLModel


class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
