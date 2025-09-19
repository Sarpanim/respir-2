from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routers import ambiances, categories, courses, levels, progress
from .seeds import seed_demo_data

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize the database and optionally load seed data."""

    init_db()
    if settings.auto_seed:
        seed_demo_data()


app.include_router(categories.router)
app.include_router(levels.router)
app.include_router(ambiances.router)
app.include_router(courses.router)
app.include_router(progress.router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    """Simple endpoint used to monitor the API."""

    return {"status": "ok"}
