from contextlib import asynccontextmanager
from http.client import HTTPException

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from ih.core.jobs.scheduler import setup_scheduler
from ih.core.config import get_app_settings
from ih.routes import router

import smtplib
from email.mime.text import MIMEText

from ih.services.email.email import send_confirmation_email

settings = get_app_settings()


# Start periodic background tasks
@repeat_every(seconds=10)  # every hour
async def scheduled_invite_cleanup_task() -> None:
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    from ih.db.init_db import init_db
    print("HIII")
    init_db()
    # TODO PROPER LOGGING AND SMTP SENDING
    print("database init finished")
    if settings.IH_SMTP_ENABLED:
        send_confirmation_email("test@test.com", "mytest", "https://google.at")

    setup_scheduler()
    # You can add more startup code here if needed...
    yield
    # (Optional) Cleanup code on shutdown here

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if not settings.PRODUCTION:
    allowed_origins = [settings.IH_APP_URL]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.PRODUCTION:
    dist_path = Path(__file__).resolve().parent / "frontend"
    print(dist_path)
    # Serve all static assets under /assets, etc.
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="spa")






