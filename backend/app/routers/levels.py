from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..dependencies import require_admin
from ..models.entities import Level
from ..schemas.level import LevelCreate, LevelRead, LevelUpdate

router = APIRouter(prefix="/levels", tags=["levels"])


@router.get("/", response_model=List[LevelRead])
def list_levels(session: Session = Depends(get_session)) -> List[Level]:
    statement = select(Level).order_by(Level.order, Level.name)
    return session.exec(statement).all()


@router.get("/{level_id}", response_model=LevelRead)
def get_level(level_id: int, session: Session = Depends(get_session)) -> Level:
    level = session.get(Level, level_id)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return level


@router.post("/", response_model=LevelRead, status_code=status.HTTP_201_CREATED)
def create_level(
    payload: LevelCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> Level:
    level = Level(**payload.dict())
    session.add(level)
    session.commit()
    session.refresh(level)
    return level


@router.put("/{level_id}", response_model=LevelRead)
def update_level(
    level_id: int,
    payload: LevelUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> Level:
    level = session.get(Level, level_id)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(level, key, value)
    level.updated_at = datetime.utcnow()
    session.add(level)
    session.commit()
    session.refresh(level)
    return level


@router.delete("/{level_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_level(
    level_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> None:
    level = session.get(Level, level_id)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    session.delete(level)
    session.commit()
