from contextlib import asynccontextmanager
from http.client import HTTPException

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path

from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from ih.core.jobs.scheduler import setup_scheduler
from ih.core.config import get_app_settings
from ih.core.logging.logger import get_logger
from ih.routes import router

from ih import __version__

print(__version__)

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

# Define a subclass of StaticFiles to create a custom static file handler
# that supports client-side routing in Single Page Applications (SPAs).
class SPAStaticFiles(StaticFiles):
    # Override the get_response method, which is responsible for retrieving
    # static file responses for given paths.
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex
        except Exception as ex:
            print(ex)

app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.IH_SECRET_KEY)
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
    app.mount("/", SPAStaticFiles(directory=dist_path, html=True), name="spa")
    #app.mount("/", StaticFiles(directory=dist_path, html=True), name="spa")






