from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column, String, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


class TimestampMixin(SQLModel):
    """Mixin adding timestamp columns to tables."""

    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CategoryBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)


class Category(CategoryBase, TimestampMixin, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)

    courses: List["Course"] = Relationship(back_populates="category")


class LevelBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)
    order: Optional[int] = Field(default=None, description="Display ordering for levels")


class Level(LevelBase, TimestampMixin, table=True):
    __tablename__ = "levels"

    id: Optional[int] = Field(default=None, primary_key=True)

    courses: List["Course"] = Relationship(back_populates="level")


class AmbienceBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)
    audio_url: Optional[str] = Field(default=None, description="Reference to the ambience playlist")


class Ambience(AmbienceBase, TimestampMixin, table=True):
    __tablename__ = "ambiances"

    id: Optional[int] = Field(default=None, primary_key=True)

    courses: List["Course"] = Relationship(back_populates="ambience")


class CourseBase(SQLModel):
    title: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2048)
    duration_minutes: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    level_id: Optional[int] = Field(default=None, foreign_key="levels.id")
    ambience_id: Optional[int] = Field(default=None, foreign_key="ambiances.id")


class Course(CourseBase, TimestampMixin, table=True):
    __tablename__ = "courses"
    __table_args__ = (UniqueConstraint("title", name="uq_courses_title"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    category: Optional[Category] = Relationship(back_populates="courses")
    level: Optional[Level] = Relationship(back_populates="courses")
    ambience: Optional[Ambience] = Relationship(back_populates="courses")
    sessions: List["CourseSession"] = Relationship(back_populates="course", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    progresses: List["UserProgress"] = Relationship(back_populates="course")


class CourseSessionBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=2048)
    order: Optional[int] = Field(default=None, description="Ordering inside a course")
    duration_minutes: Optional[int] = Field(default=None, ge=0)


class CourseSession(CourseSessionBase, TimestampMixin, table=True):
    __tablename__ = "course_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id")

    course: Course = Relationship(back_populates="sessions")


class UserBase(SQLModel):
    email: str = Field(sa_column=Column(String(255), unique=True, index=True))
    full_name: Optional[str] = Field(default=None, max_length=255)


class User(UserBase, TimestampMixin, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    progresses: List["UserProgress"] = Relationship(back_populates="user")


class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class UserProgressBase(SQLModel):
    total_listened_seconds: int = Field(default=0, ge=0)
    status: ProgressStatus = Field(default=ProgressStatus.NOT_STARTED)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)


class UserProgress(UserProgressBase, TimestampMixin, table=True):
    __tablename__ = "user_progress"
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_progress_user_course"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    course_id: int = Field(foreign_key="courses.id")

    user: User = Relationship(back_populates="progresses")
    course: Course = Relationship(back_populates="progresses")
