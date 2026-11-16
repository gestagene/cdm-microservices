from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import func, select

from src.verification.models import UserVerification
MAX_ATTEMPTS_PER_DAY = 3

async def enfore_verification_attempt_limit(session, user_id):
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    attempts = await session.scalar(
        select(func.count()).select_from(UserVerification).where(
            UserVerification.user_id == user_id,
            UserVerification.created_at >= since
        )
    )
    if attempts >= MAX_ATTEMPTS_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail="Too many verification attempts. Try again tomorow."
        )