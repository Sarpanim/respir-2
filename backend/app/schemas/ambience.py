from typing import Optional

from sqlmodel import SQLModel


class AmbienceBase(SQLModel):
    name: str
    description: Optional[str] = None
    audio_url: Optional[str] = None


class AmbienceCreate(AmbienceBase):
    pass


class AmbienceRead(AmbienceBase):
    id: int

    class Config:
        orm_mode = True


class AmbienceUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    audio_url: Optional[str] = None
