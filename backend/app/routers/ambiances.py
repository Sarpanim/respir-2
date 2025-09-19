from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..dependencies import require_admin
from ..models.entities import Ambience
from ..schemas.ambience import AmbienceCreate, AmbienceRead, AmbienceUpdate

router = APIRouter(prefix="/ambiances", tags=["ambiances"])


@router.get("/", response_model=List[AmbienceRead])
def list_ambiances(session: Session = Depends(get_session)) -> List[Ambience]:
    statement = select(Ambience).order_by(Ambience.name)
    return session.exec(statement).all()


@router.get("/{ambience_id}", response_model=AmbienceRead)
def get_ambience(ambience_id: int, session: Session = Depends(get_session)) -> Ambience:
    ambience = session.get(Ambience, ambience_id)
    if not ambience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ambience not found")
    return ambience


@router.post("/", response_model=AmbienceRead, status_code=status.HTTP_201_CREATED)
def create_ambience(
    payload: AmbienceCreate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> Ambience:
    ambience = Ambience(**payload.dict())
    session.add(ambience)
    session.commit()
    session.refresh(ambience)
    return ambience


@router.put("/{ambience_id}", response_model=AmbienceRead)
def update_ambience(
    ambience_id: int,
    payload: AmbienceUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> Ambience:
    ambience = session.get(Ambience, ambience_id)
    if not ambience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ambience not found")
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ambience, key, value)
    ambience.updated_at = datetime.utcnow()
    session.add(ambience)
    session.commit()
    session.refresh(ambience)
    return ambience


@router.delete("/{ambience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ambience(
    ambience_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(require_admin),
) -> None:
    ambience = session.get(Ambience, ambience_id)
    if not ambience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ambience not found")
    session.delete(ambience)
    session.commit()
