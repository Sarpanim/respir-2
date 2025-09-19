from typing import Optional

from sqlmodel import SQLModel


class CourseSessionBase(SQLModel):
    title: str
    description: Optional[str] = None
    order: Optional[int] = None
    duration_minutes: Optional[int] = None


class CourseSessionRead(CourseSessionBase):
    id: int

    class Config:
        orm_mode = True


class CourseSessionCreate(CourseSessionBase):
    course_id: Optional[int] = None


class CourseSessionUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    duration_minutes: Optional[int] = None
