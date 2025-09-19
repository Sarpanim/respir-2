from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlmodel import Session, select

from ..database import get_session
from ..dependencies import get_current_user
from ..models.entities import Course, ProgressStatus, User, UserProgress
from ..schemas.progress import ProgressComplete, ProgressLog, ProgressRead, ProgressStart

router = APIRouter(prefix="/progress", tags=["progress"])


def _progress_select() -> Select:
    return (
        select(UserProgress)
        .options(
            selectinload(UserProgress.user),
            selectinload(UserProgress.course).selectinload(Course.sessions),
            selectinload(UserProgress.course).selectinload(Course.category),
            selectinload(UserProgress.course).selectinload(Course.level),
            selectinload(UserProgress.course).selectinload(Course.ambience),
        )
        .order_by(UserProgress.updated_at.desc())
    )


def _load_progress(session: Session, progress_id: int) -> UserProgress:
    statement = _progress_select().where(UserProgress.id == progress_id)
    progress = session.exec(statement).unique().one_or_none()
    if not progress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress not found")
    return progress


@router.get("/me", response_model=List[ProgressRead])
def list_my_progress(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> List[UserProgress]:
    statement = _progress_select().where(UserProgress.user_id == user.id)
    progresses = session.exec(statement).unique().all()
    return progresses


@router.get("/{progress_id}", response_model=ProgressRead)
def get_progress(
    progress_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> UserProgress:
    progress = _load_progress(session, progress_id)
    if progress.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return progress


@router.post("/start", response_model=ProgressRead, status_code=status.HTTP_201_CREATED)
def start_course(
    payload: ProgressStart,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> UserProgress:
    course = session.get(Course, payload.course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    statement = select(UserProgress).where(
        UserProgress.user_id == user.id, UserProgress.course_id == course.id
    )
    progress = session.exec(statement).one_or_none()
    now = datetime.utcnow()
    if progress is None:
        progress = UserProgress(
            user_id=user.id,
            course_id=course.id,
            status=ProgressStatus.IN_PROGRESS,
            started_at=now,
            updated_at=now,
        )
        session.add(progress)
    else:
        progress.status = ProgressStatus.IN_PROGRESS
        if not progress.started_at:
            progress.started_at = now
        progress.updated_at = now
        session.add(progress)
    session.commit()
    return _load_progress(session, progress.id)


@router.post("/{progress_id}/log", response_model=ProgressRead)
def log_listening(
    progress_id: int,
    payload: ProgressLog,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> UserProgress:
    progress = session.get(UserProgress, progress_id)
    if not progress or progress.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress not found")
    progress.total_listened_seconds += payload.listened_seconds
    if progress.status == ProgressStatus.NOT_STARTED:
        progress.status = ProgressStatus.IN_PROGRESS
        if not progress.started_at:
            progress.started_at = datetime.utcnow()
    progress.updated_at = datetime.utcnow()
    session.add(progress)
    session.commit()
    return _load_progress(session, progress.id)


@router.post("/{progress_id}/complete", response_model=ProgressRead)
def complete_course(
    progress_id: int,
    payload: ProgressComplete,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> UserProgress:
    progress = session.get(UserProgress, progress_id)
    if not progress or progress.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress not found")
    if payload.listened_seconds:
        progress.total_listened_seconds += payload.listened_seconds
    now = datetime.utcnow()
    progress.status = ProgressStatus.COMPLETED
    if not progress.started_at:
        progress.started_at = now
    progress.completed_at = now
    progress.updated_at = now
    session.add(progress)
    session.commit()
    return _load_progress(session, progress.id)
