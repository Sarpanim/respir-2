from datetime import datetime
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session, select

from .config import settings
from .database import get_session
from .models.entities import User


async def require_admin(x_admin_token: str = Header(..., alias="X-Admin-Token")) -> None:
    """Ensure the caller is an administrator."""

    if x_admin_token != settings.admin_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


def _update_user_timestamp(user: User) -> None:
    user.updated_at = datetime.utcnow()


async def get_current_user(
    session: Session = Depends(get_session),
    x_user_email: str = Header(..., alias="X-User-Email"),
    x_user_name: Optional[str] = Header(None, alias="X-User-Name"),
) -> User:
    """Retrieve the current user based on request headers."""

    statement = select(User).where(User.email == x_user_email)
    user = session.exec(statement).first()
    if user is None:
        user = User(email=x_user_email, full_name=x_user_name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    updated = False
    if x_user_name and user.full_name != x_user_name:
        user.full_name = x_user_name
        updated = True

    if updated:
        _update_user_timestamp(user)
        session.add(user)
        session.commit()
        session.refresh(user)

    return user
