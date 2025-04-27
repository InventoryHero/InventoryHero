from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware

from ih.core.jobs.scheduler import setup_scheduler
from ih.core.config import get_app_settings
from ih.routes import router

settings = get_app_settings()

# Start periodic background tasks
@repeat_every(seconds=10)  # every hour
async def scheduled_invite_cleanup_task() -> None:
    pass



@asynccontextmanager
async def lifespan(app: FastAPI):

    setup_scheduler()
    # You can add more startup code here if needed...

    yield

    # (Optional) Cleanup code on shutdown here

app = FastAPI(lifespan=lifespan)


if not settings.PRODUCTION:
    allowed_origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.PRODUCTION:
    # TODO MOUNT SPA
    pass




app.include_router(router)

