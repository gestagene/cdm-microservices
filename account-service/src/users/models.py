import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, Computed, DateTime, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=text("gen_random_uuid()")
    )
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    phone_number: Mapped[str] = mapped_column(Text, unique=True)

    # id verification
    student_number: Mapped[str | None] = mapped_column(Text, unique=True)
    id_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # school email
    school_email: Mapped[str | None] = mapped_column(Text, unique=True)
    school_email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    verification_level: Mapped[str] = mapped_column(
        Text,
        Computed(
            "CASE "
            "WHEN id_verified_at IS NOT NULL AND school_email_verified_at IS NOT NULL THEN 'fully_verified' "
            "WHEN id_verified_at IS NOT NULL OR school_email_verified_at IS NOT NULL THEN 'basic' "
            "ELSE 'unverified' END",
            persisted=True,
        ),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )

    __table_args__ = (
        CheckConstraint(r"username ~ '^[a-z0-9_]{3,20}$'", name="username_format"),
        CheckConstraint(r"phone_number ~ '^\+639[0-9]{9}$'", name="phone_format"),
        CheckConstraint(r"student_number ~ '^[0-9]{2}-[0-9]{5}$'", name="student_number_format"),
        CheckConstraint(r"school_email ~ '^[a-z0-9._-]+@pnm\.edu\.ph$'", name="school_email_format"),
        CheckConstraint(
            "id_verified_at IS NULL OR student_number IS NOT NULL",
            name="id_verified_requires_number",
        ),
        CheckConstraint(
            "school_email_verified_at IS NULL OR school_email IS NOT NULL",
            name="email_verified_requires_email",
        ),
    )