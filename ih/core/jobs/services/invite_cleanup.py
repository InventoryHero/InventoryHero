from datetime import datetime

from sqlalchemy import delete

from ih.core.logging.logger import get_logger
from ih.db.db_setup import get_session
from ih.db.models.households import HouseholdInvite


async def cleanup_invites():
    logger = get_logger("ih.scheduled_tasks.invite_cleanup")
    now = datetime.now()
    try:
        session_generator = get_session()
        session = next(session_generator)

        stmt = (
            delete(HouseholdInvite)
            .where(
                HouseholdInvite.expires_at < now,
                HouseholdInvite.accepted == False
            )
        )
        result = session.exec(stmt)
        session.commit()
        logger.info(f"Deleted {result.rowcount} rows from HouseholdInvite")
        session.close()
    except Exception as e:
        logger.error(e)