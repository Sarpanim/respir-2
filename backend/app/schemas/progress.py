from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from ..models.entities import ProgressStatus
from .course import CourseRead
from .user import UserRead


class ProgressStart(SQLModel):
    course_id: int


class ProgressLog(SQLModel):
    listened_seconds: int = Field(gt=0, description="Additional seconds listened since the last update")


class ProgressComplete(SQLModel):
    listened_seconds: Optional[int] = Field(
        default=None,
        gt=0,
        description="Optional listened seconds to add before completing the course",
    )


class ProgressRead(SQLModel):
    id: int
    course_id: int
    user_id: int
    status: ProgressStatus
    total_listened_seconds: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    course: Optional[CourseRead] = None
    user: Optional[UserRead] = None

    class Config:
        orm_mode = True
