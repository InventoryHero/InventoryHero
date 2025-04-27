# ih/core/logging/logging_config.py

import logging

from ih.core.config import get_app_settings

settings = get_app_settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # keeps uvicorn/error/etc
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "ih.app": {  # your app
            "handlers": ["default"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {  # Catch all other logs
        "level": "INFO",
        "handlers": ["default"],
    },
}
