# ih/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from ih.core.config import get_app_settings
from ih.core.jobs.services.invite_cleanup import cleanup_invites
from ih.core.logging.logger import get_logger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

scheduler = AsyncIOScheduler()
settings = get_app_settings()
logger = get_logger("ih.scheduler")


def scheduler_listener(event):
    job = scheduler.get_job(event.job_id)
    if job and job.next_run_time:
        logger.info(f"Next execution of scheduled job '{job.id}' at {job.next_run_time}")


def setup_scheduler():
    scheduler.start()
    # TODO MAKE CONFIGURABLE
    scheduler.add_job(
        func=cleanup_invites,
        #trigger=CronTrigger(hour=0, minute=0, timezone="UTC"),
        trigger=IntervalTrigger(seconds=3600 if settings.PRODUCTION else 300),
        id="invite_cleanup_job",
        replace_existing=True,
    )
    scheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    for job in scheduler.get_jobs():
        logger.info(f"Next execution of scheduled job '{job.id}' at {job.next_run_time}")


