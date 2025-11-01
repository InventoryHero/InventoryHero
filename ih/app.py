from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from ih.core.jobs.scheduler import setup_scheduler
from ih.core.config import get_app_settings
from ih.core.logging.logger import get_logger
from ih.routes import router

# TODO merge all raise HTTPException to raise InventoryHeroAPIException

settings = get_app_settings()
logger = get_logger()

@asynccontextmanager
async def lifespan(ih_app: FastAPI):
    from ih.db.init_db import init_db
    init_db()
    logger.info("database configured")
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
    # Serve all static assets under /assets, etc.
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="spa")






