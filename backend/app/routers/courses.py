from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlmodel import Session, select

from ..database import get_session
from ..dependencies import require_admin
from ..models.entities import Course, CourseSession
from ..schemas.course import CourseCreate, CourseRead, CourseUpdate
from ..schemas.session import CourseSessionCreate, CourseSessionRead, CourseSessionUpdate

router = APIRouter(prefix="/courses", tags=["courses"])


def _course_select() -> Select:
    return (
        select(Course)
        .options(
            selectinload(Course.category),
            selectinload(Course.level),
            selectinload(Course.ambience),
            selectinload(Course.sessions),
        )
        .order_by(Course.title)
    )


def _load_course(session: Session, course_id: int) -> Course:
    statement = _course_select().where(Course.id == course_id)
    course = session.exec(statement).unique().one_or_none()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.get("/", response_model=List[CourseRead])
def list_courses(session: Session = Depends(get_session)) -> List[Course]:
    courses = session.exec(_course_select()).unique().all()
    return courses


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, session: Session = Depends(get_session)) -> Course:
    return _load_course(session, course_id)


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    payload: CourseCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> Course:
    course = Course(**payload.dict())
    session.add(course)
    session.commit()
    return _load_course(session, course.id)


@router.put("/{course_id}", response_model=CourseRead)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> Course:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)
    course.updated_at = datetime.utcnow()
    session.add(course)
    session.commit()
    return _load_course(session, course.id)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> None:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    session.delete(course)
    session.commit()


@router.post("/{course_id}/sessions", response_model=CourseSessionRead, status_code=status.HTTP_201_CREATED)
def add_course_session(
    course_id: int,
    payload: CourseSessionCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> CourseSession:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if payload.course_id and payload.course_id != course_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mismatching course identifiers")
    session_data = payload.dict(exclude_unset=True)
    session_data["course_id"] = course_id
    course_session = CourseSession(**session_data)
    session.add(course_session)
    course.updated_at = datetime.utcnow()
    session.add(course)
    session.commit()
    session.refresh(course_session)
    return course_session


@router.patch("/{course_id}/sessions/{session_id}", response_model=CourseSessionRead)
def update_course_session(
    course_id: int,
    session_id: int,
    payload: CourseSessionUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> CourseSession:
    course_session = session.get(CourseSession, session_id)
    if not course_session or course_session.course_id != course_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course_session, key, value)
    course_session.updated_at = datetime.utcnow()
    session.add(course_session)
    course = session.get(Course, course_id)
    if course:
        course.updated_at = datetime.utcnow()
        session.add(course)
    session.commit()
    session.refresh(course_session)
    return course_session


@router.delete("/{course_id}/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_session(
    course_id: int,
    session_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> None:
    course_session = session.get(CourseSession, session_id)
    if not course_session or course_session.course_id != course_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    course = session.get(Course, course_id)
    if course:
        course.updated_at = datetime.utcnow()
        session.add(course)
    session.delete(course_session)
    session.commit()
