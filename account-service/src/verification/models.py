import uuid
from datetime import datetime

from sqlalchemy import Index, Float, ForeignKey, CheckConstraint, DateTime, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base import Base

class UserVerification(Base):
    __tablename__="id_verifications"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    student_number: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(16), server_default="pending"
    )

    #id verification
    match_score: Mapped[float | None] = mapped_column(Float)
    reject_reason: Mapped[str | None] = mapped_column(String(50))
    provider: Mapped[str] = mapped_column(String(30))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name="status_valid",
        ),
        CheckConstraint(
            "match_score IS NULL OR match_score BETWEEN 0 AND 100",
            name="match_score_range",
        ),
        CheckConstraint(
            r"student_number ~ '^[0-9]{2}-[0-9]{5}$'", name="student_number_format"
            ),
        Index("ix_id_verification_user_id_created_at", "user_id", "created_at")
)