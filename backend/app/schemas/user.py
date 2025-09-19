from typing import Optional

from sqlmodel import SQLModel


class UserBase(SQLModel):
    email: str
    full_name: Optional[str] = None


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
