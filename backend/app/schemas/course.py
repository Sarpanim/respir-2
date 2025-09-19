from typing import List, Optional

from sqlmodel import SQLModel

from .ambience import AmbienceRead
from .category import CategoryRead
from .level import LevelRead
from .session import CourseSessionRead


class CourseBase(SQLModel):
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    ambience_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    ambience_id: Optional[int] = None


class CourseRead(CourseBase):
    id: int
    category: Optional[CategoryRead] = None
    level: Optional[LevelRead] = None
    ambience: Optional[AmbienceRead] = None
    sessions: List[CourseSessionRead] = []

    class Config:
        orm_mode = True
