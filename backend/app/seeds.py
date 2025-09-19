"""Utility helpers to populate the database with demonstration content."""

from datetime import datetime
from typing import Dict, Iterable

from sqlmodel import Session, select

from .database import engine
from .models.entities import Ambience, Category, Course, CourseSession, Level


def _get_or_create(
    session: Session,
    model,
    defaults: Dict,
    /,
    **filters,
):
    instance = session.exec(select(model).filter_by(**filters)).one_or_none()
    if instance:
        return instance
    params = {**defaults, **filters}
    instance = model(**params)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def seed_demo_data() -> None:
    """Populate the database with seed data for development and demos."""

    with Session(engine) as session:
        breathwork = _get_or_create(session, Category, {"description": "Techniques de respiration"}, name="Respiration")
        meditation = _get_or_create(session, Category, {"description": "Séances guidées"}, name="Méditation guidée")

        beginner = _get_or_create(session, Level, {"description": "Accessible à tous", "order": 1}, name="Débutant")
        intermediate = _get_or_create(
            session,
            Level,
            {"description": "Pour aller plus loin", "order": 2},
            name="Intermédiaire",
        )

        ocean = _get_or_create(
            session,
            Ambience,
            {"description": "Sons marins relaxants", "audio_url": "https://cdn.example.com/ambiances/ocean"},
            name="Mer calme",
        )
        forest = _get_or_create(
            session,
            Ambience,
            {"description": "Ambiance forêt et oiseaux", "audio_url": "https://cdn.example.com/ambiances/forest"},
            name="Forêt matinale",
        )

        courses_payload = [
            {
                "title": "Routine Respiration Matinale",
                "description": "Activez votre énergie avec une routine de respiration consciente.",
                "duration_minutes": 15,
                "category": breathwork,
                "level": beginner,
                "ambience": ocean,
                "sessions": [
                    {
                        "title": "Respiration en carré",
                        "description": "Un cycle de respiration équilibré pour démarrer la journée.",
                        "order": 1,
                        "duration_minutes": 5,
                    },
                    {
                        "title": "Cohérence cardiaque",
                        "description": "Stabilisez votre rythme cardiaque avant vos activités.",
                        "order": 2,
                        "duration_minutes": 10,
                    },
                ],
            },
            {
                "title": "Exploration méditative du soir",
                "description": "Relâchez les tensions avec une méditation guidée immersive.",
                "duration_minutes": 20,
                "category": meditation,
                "level": intermediate,
                "ambience": forest,
                "sessions": [
                    {
                        "title": "Ancrage corporel",
                        "description": "Reconnectez-vous à vos sensations physiques.",
                        "order": 1,
                        "duration_minutes": 8,
                    },
                    {
                        "title": "Balayage des pensées",
                        "description": "Laissez passer les pensées en douceur.",
                        "order": 2,
                        "duration_minutes": 12,
                    },
                ],
            },
        ]

        for payload in courses_payload:
            existing = session.exec(select(Course).where(Course.title == payload["title"]))
            course = existing.one_or_none()
            if course:
                continue
            course = Course(
                title=payload["title"],
                description=payload["description"],
                duration_minutes=payload["duration_minutes"],
                category_id=payload["category"].id,
                level_id=payload["level"].id,
                ambience_id=payload["ambience"].id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(course)
            session.flush()
            sessions_payload: Iterable[Dict] = payload["sessions"]
            for order_payload in sessions_payload:
                course_session = CourseSession(course_id=course.id, **order_payload)
                session.add(course_session)
            session.commit()


if __name__ == "__main__":
    seed_demo_data()
