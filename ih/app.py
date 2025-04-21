import uvicorn
from fastapi import Depends, FastAPI, Query
from sqlmodel import  Session, select
from fastapi.middleware.cors import CORSMiddleware

from ih.core.config import get_app_settings
from ih.db.db_setup import get_session
from ih.routes import router

settings = get_app_settings()

app = FastAPI()


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


@app.get("/")
def read_root():
    return {"hello": "world"}
